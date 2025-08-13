import json
import logging
import os
from typing import Dict, Any, List

import boto3
from strands.models import BedrockModel
from strands import Agent
from strands.tools import tool

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Debug: Force redeployment to test layer accessibility
logger.info("Lambda function starting with strands integration and Knowledge Base tools")

# Configuration - these will be set as environment variables in the Lambda
REGION_NAME = os.environ.get("REGION_NAME", "us-east-1")
MODEL_ID = os.environ.get("MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0")
KNOWLEDGE_BASE_ID = os.environ.get("KNOWLEDGE_BASE_ID", "")
KNOWLEDGE_BASE_DATA_SOURCE_ID = os.environ.get("KNOWLEDGE_BASE_DATA_SOURCE_ID", "")

# System prompt for the AI assistant with Harry Potter specialization
SYSTEM_PROMPT = """You are a helpful, friendly, and knowledgeable AI assistant specialized in Harry Potter books and lore, powered by Claude 3 Sonnet. 

You have access to a comprehensive Knowledge Base containing detailed information about the Harry Potter series, including:
- All seven books: Philosopher's Stone, Chamber of Secrets, Prisoner of Azkaban, Goblet of Fire, Order of Phoenix, Half-Blood Prince, and Deathly Hallows
- Character information, relationships, and development
- Magical creatures, spells, and potions
- Hogwarts houses, locations, and history
- Plot details, themes, and literary analysis
- Author information and series background

When users ask questions about Harry Potter, use the Knowledge Base search tool to find accurate, detailed information. Always cite your sources and provide comprehensive answers based on the books.

You provide clear, accurate, and helpful responses to user questions about Harry Potter and general topics.
Always be polite and professional in your interactions.
If you're not sure about something, say so rather than making things up.
You can use various tools and capabilities to help users with their requests."""

# Initialize Bedrock session and model (reused across invocations)
_boto_session = None
_bedrock_model = None
_agent = None
_bedrock_agent_client = None

def _get_bedrock_session():
    """Get or create a Bedrock session"""
    global _boto_session
    if _boto_session is None:
        _boto_session = boto3.Session(region_name=REGION_NAME)
    return _boto_session

def _get_bedrock_model():
    """Get or create a Bedrock model instance"""
    global _bedrock_model
    if _bedrock_model is None:
        session = _get_bedrock_session()
        _bedrock_model = BedrockModel(
            model_id=MODEL_ID,
            boto_session=session,
            streaming=False
        )
    return _bedrock_model

def _get_bedrock_agent_client():
    """Get or create a Bedrock Agent Runtime client"""
    global _bedrock_agent_client
    if _bedrock_agent_client is None:
        session = _get_bedrock_session()
        _bedrock_agent_client = session.client('bedrock-agent-runtime')
    return _bedrock_agent_client

@tool(name="search_harry_potter_knowledge", description="Search the Harry Potter Knowledge Base for detailed information about characters, plot, spells, creatures, and lore from the books")
def search_knowledge_base(query: str) -> str:
    """
    Search the Amazon Knowledge Base for Harry Potter information
    
    Args:
        query (str): The search query about Harry Potter
        
    Returns:
        str: Search results and relevant information
    """
    try:
        if not KNOWLEDGE_BASE_ID or not KNOWLEDGE_BASE_DATA_SOURCE_ID:
            return "Knowledge Base not configured. Please set KNOWLEDGE_BASE_ID and KNOWLEDGE_BASE_DATA_SOURCE_ID environment variables."
        
        client = _get_bedrock_agent_client()
        
        # Search the knowledge base
        response = client.retrieve(
            knowledgeBaseId=KNOWLEDGE_BASE_ID,
            retrievalQuery={
                'text': query
            },
            retrievalConfiguration={
                'vectorSearchConfiguration': {
                    'numberOfResults': 5
                }
            }
        )
        
        # Extract and format the results
        results = []
        for retrieval_result in response.get('retrievalResults', []):
            content = retrieval_result.get('content', {})
            text = content.get('text', '')
            metadata = content.get('metadata', {})
            
            # Extract source information
            source = metadata.get('source', 'Unknown source')
            title = metadata.get('title', 'No title')
            
            results.append(f"Source: {source}\nTitle: {title}\nContent: {text}\n")
        
        if results:
            return f"Found {len(results)} relevant results for your query about Harry Potter:\n\n" + "\n---\n".join(results)
        else:
            return "No specific information found in the Knowledge Base for your query. I can still help with general Harry Potter knowledge based on my training."
            
    except Exception as e:
        logger.error(f"Error searching Knowledge Base: {str(e)}")
        return f"Error searching the Knowledge Base: {str(e)}. I can still help with general Harry Potter knowledge based on my training."

def _get_agent():
    """Get or create a Strands Agent instance with Knowledge Base tools"""
    global _agent
    if _agent is None:
        model = _get_bedrock_model()
        
        # Create tools for the agent - the @tool decorator automatically creates the tool
        tools = [search_knowledge_base]
        
        _agent = Agent(
            system_prompt=SYSTEM_PROMPT,
            tools=tools,
            model=model
        )
    return _agent

def _chat_with_claude(message: str) -> str:
    """Send a message to Claude via Strands Agent and return the response"""
    try:
        agent = _get_agent()
        logger.info(f"Sending message to Claude via Strands: {message[:100]}...")
        
        # Use the agent to get a response
        result = agent(message)
        
        # Extract the text content from the response
        if hasattr(result, 'message') and result.message:
            if isinstance(result.message, dict) and 'content' in result.message:
                content = result.message['content']
                if isinstance(content, list) and len(content) > 0:
                    if 'text' in content[0]:
                        return str(content[0]['text'])
                    elif 'type' in content[0] and content[0]['type'] == 'text':
                        return str(content[0].get('text', ''))
                elif isinstance(content, str):
                    return content
            elif isinstance(result.message, str):
                return result.message
        
        # Fallback: try to get response as string
        response_str = str(result)
        logger.info(f"Claude response via Strands: {response_str[:200]}...")
        return response_str
        
    except Exception as e:
        logger.error(f"Error calling Claude via Strands: {str(e)}")
        # Return a friendly error message
        return f"I apologize, but I encountered an error while processing your request: {str(e)}. Please try again."

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda function handler for chat API endpoints
    """
    try:
        # Get HTTP method and path from REST API Gateway event
        http_method = event.get('httpMethod', '')
        path = event.get('path', '')
        
        logger.info(f"Received {http_method} request to {path}")
        
        # Handle different endpoints
        if path == '/health' and http_method == 'GET':
            return health_check(context)
        elif path == '/chat' and http_method == 'POST':
            return handle_chat(event, context)
        else:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'POST, GET, OPTIONS'
                },
                'body': json.dumps({
                    'error': 'Endpoint not found',
                    'message': f'Path {path} with method {http_method} is not supported'
                })
            }
            
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS'
            },
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e)
            })
        }

def health_check(context: Any) -> Dict[str, Any]:
    """
    Health check endpoint
    """
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS'
        },
        'body': json.dumps({
            'status': 'healthy',
            'message': 'Chat API is running with Claude integration via Strands and Harry Potter Knowledge Base',
            'model': MODEL_ID,
            'region': REGION_NAME,
            'framework': 'strands-agents',
            'knowledge_base_configured': bool(KNOWLEDGE_BASE_ID and KNOWLEDGE_BASE_DATA_SOURCE_ID),
            'timestamp': context.get_remaining_time_in_millis() if context else None
        })
    }

def handle_chat(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Handle chat POST requests with Claude AI integration via Strands and Knowledge Base
    """
    try:
        # Parse request body
        body = event.get('body', '{}')
        if isinstance(body, str):
            body = json.loads(body)
        
        # Extract message from request
        message = body.get('message', '')
        user_id = body.get('user_id', 'anonymous')
        
        if not message:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'POST, GET, OPTIONS'
                },
                'body': json.dumps({
                    'error': 'Bad request',
                    'message': 'Message field is required'
                })
            }
        
        logger.info(f"Chat request from user {user_id}: {message[:100]}...")
        
        # Get AI response from Claude via Strands with Knowledge Base access
        ai_response = _chat_with_claude(message)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS'
            },
            'body': json.dumps({
                'response': ai_response,
                'user_id': user_id,
                'model': MODEL_ID,
                'framework': 'strands-agents',
                'knowledge_base_enabled': bool(KNOWLEDGE_BASE_ID and KNOWLEDGE_BASE_DATA_SOURCE_ID),
                'timestamp': context.get_remaining_time_in_millis() if context else None
            })
        }
        
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS'
            },
            'body': json.dumps({
                'error': 'Bad request',
                'message': 'Invalid JSON in request body'
            })
        }
