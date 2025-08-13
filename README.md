# Chat API with CDK and Container-based Lambda

This project creates an AWS API Gateway with a chat endpoint using AWS CDK and a container-based Lambda function with Python 3.12, featuring integration capabilities for strands-agents and a specialized Harry Potter Knowledge Base.

## Architecture

- **API Gateway**: REST API with CORS enabled
- **Lambda Function**: Container-based Python 3.12 runtime handling chat requests
- **AI Integration**: Ready for strands-agents integration with Claude 3 Sonnet via Amazon Bedrock
- **Knowledge Base**: Amazon Bedrock Knowledge Base for Harry Potter books and lore
- **Endpoints**:
  - `POST /chat` - Chat endpoint for sending messages with Knowledge Base access
  - `GET /health` - Health check endpoint

## Prerequisites

- **Python 3.12** (required for strands-agents compatibility)
- **Docker** (required for building Lambda container)
- **Amazon Bedrock Access** (required for Knowledge Base integration)
- AWS CLI configured with appropriate credentials
- AWS CDK CLI installed globally
- Homebrew (for Python 3.12 installation on macOS)

## Setup

### 1. Install Python 3.12

If you don't have Python 3.12, install it using Homebrew:

```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Add Homebrew to PATH
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"

# Install Python 3.12
brew install python@3.12

# Add Python 3.12 to PATH
export PATH="/opt/homebrew/bin:$PATH"
```

### 2. Install Docker

Ensure Docker Desktop is installed and running:

```bash
# Install Docker Desktop (if not already installed)
brew install --cask docker

# Start Docker Desktop
open /Applications/Docker.app
```

### 3. Create Virtual Environment

```bash
# Create virtual environment with Python 3.12
python3.12 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Verify Python version
python --version  # Should show Python 3.12.x
```

### 4. Install Dependencies

```bash
# Install project dependencies
pip install -r requirements.txt

# Verify strands-agents installation
python -c "import strands_agents; print('strands-agents installed successfully')"
```

### 5. Install AWS CDK CLI

```bash
npm install -g aws-cdk
```

### 6. Set up Amazon Knowledge Base

Before deploying, you need to set up your Harry Potter Knowledge Base:

```bash
# View setup instructions
python config.py
```

**Quick Setup Steps:**
1. Go to [Amazon Bedrock Console](https://console.aws.amazon.com/bedrock/)
2. Navigate to "Knowledge bases" in the left sidebar
3. Click "Create knowledge base"
4. Choose a name (e.g., "Harry-Potter-Books")
5. Select your preferred embedding model
6. Create a data source with your Harry Potter content
7. Note down the Knowledge Base ID and Data Source ID

### 7. Configure Environment Variables

Set your Knowledge Base configuration:

```bash
# Set your actual Knowledge Base IDs
export KNOWLEDGE_BASE_ID="your-actual-kb-id"
export KNOWLEDGE_BASE_DATA_SOURCE_ID="your-actual-ds-id"
export REGION_NAME="us-east-1"
export MODEL_ID="anthropic.claude-3-sonnet-20240229-v1:0"
```

**Or update `app.py` directly:**
```python
environment={
    "REGION_NAME": "us-east-1",
    "MODEL_ID": "anthropic.claude-3-sonnet-20240229-v1:0",
    "KNOWLEDGE_BASE_ID": "your-actual-kb-id",
    "KNOWLEDGE_BASE_DATA_SOURCE_ID": "your-actual-ds-id",
}
```

### 8. Bootstrap CDK

```bash
cdk bootstrap --profile dev-personal
```

## Deployment

1. **Deploy the stack**:
   ```bash
   cdk deploy --profile dev-personal
   ```

2. **Deploy with specific profile** (if using multiple AWS profiles):
   ```bash
   cdk deploy --profile dev-personal
   ```

## Testing

### API Testing

After deployment, test the endpoints:

#### Health Check
```bash
curl -X GET "https://your-api-id.execute-api.region.amazonaws.com/prod/health"
```

#### Chat Endpoint with Harry Potter Questions
```bash
# Ask about Harry Potter characters
curl -X POST "https://your-api-id.execute-api.region.amazonaws.com/prod/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about Harry Potter and his relationship with Dumbledore", "user_id": "test_user"}'

# Ask about magical creatures
curl -X POST "https://your-api-id.execute-api.region.amazonaws.com/prod/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the different houses at Hogwarts and their characteristics?", "user_id": "test_user"}'

# Ask about plot details
curl -X POST "https://your-api-id.execute-api.region.amazonaws.com/prod/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What happens in the Chamber of Secrets?", "user_id": "test_user"}'
```

## Development

- **Local development**: Use `cdk synth` to generate CloudFormation template
- **Watch mode**: Use `cdk watch` for automatic deployment on changes
- **Destroy stack**: Use `cdk destroy --profile dev-personal` to remove all resources
- **View differences**: Use `cdk diff --profile dev-personal` to see changes before deployment

## Project Structure

```
.
├── app.py                 # Main CDK application
├── cdk.json             # CDK configuration
├── config.py             # Knowledge Base configuration and setup instructions
├── requirements.txt     # Python dependencies (including strands-agents)
├── Dockerfile           # Container configuration for Lambda
├── lambda/              # Lambda function code
│   ├── __init__.py
│   ├── requirements.txt # Lambda-specific dependencies
│   └── chat_handler.py  # Lambda handler with Knowledge Base integration
├── .venv/               # Python 3.12 virtual environment
└── README.md            # This file
```

## Container-based Lambda

This project uses a container-based Lambda function for better dependency management:

- **Docker-based deployment**: All dependencies are packaged in the container
- **Platform compatibility**: Built for Linux/AMD64 (Lambda runtime)
- **Dependency isolation**: No need for Lambda layers or complex packaging
- **Consistent environment**: Same runtime environment locally and in AWS

### Container Features

- **Base Image**: `public.ecr.aws/lambda/python:3.12`
- **Platform**: Linux/AMD64 (compatible with Lambda)
- **Dependencies**: Automatically installed from `lambda/requirements.txt`
- **Handler**: `chat_handler.lambda_handler`

## Harry Potter Knowledge Base Integration

This project includes a specialized Knowledge Base for Harry Potter books and lore:

### Knowledge Base Features

- **Comprehensive Coverage**: All seven Harry Potter books
- **Structured Information**: Characters, plot, spells, creatures, locations
- **Source Attribution**: Always cites sources from the Knowledge Base
- **Intelligent Search**: Vector-based retrieval for relevant information
- **Fallback Support**: Uses general knowledge when specific info isn't found

### Available Information

- **Book Summaries**: All seven books with detailed plot information
- **Character Profiles**: Main and supporting characters with relationships
- **Magical Elements**: Spells, potions, creatures, and artifacts
- **Locations**: Hogwarts, Diagon Alley, and other magical places
- **Plot Details**: Chapter summaries, key events, themes, and analysis

### How It Works

1. **User Query**: User asks a question about Harry Potter
2. **Knowledge Base Search**: Agent searches the Knowledge Base using vector similarity
3. **Information Retrieval**: Relevant passages and metadata are retrieved
4. **AI Response**: Claude generates a comprehensive answer using the retrieved information
5. **Source Citation**: Response includes source information from the Knowledge Base

## strands-agents Integration

This project is set up to work with strands-agents for AI-powered chat functionality. The current implementation includes:

- **Basic chat endpoint** with Knowledge Base integration
- **strands-agents ready** - all dependencies installed
- **Python 3.12 runtime** - compatible with latest strands-agents versions
- **Amazon Bedrock integration** - ready for Claude 3 Sonnet
- **Knowledge Base tools** - specialized tools for Harry Potter information

### AI Model Configuration

The Lambda function is configured with:
- **Model ID**: `anthropic.claude-3-sonnet-20240229-v1:0`
- **Service**: Amazon Bedrock
- **Region**: `us-east-1` (configurable)
- **Knowledge Base**: Harry Potter books and lore

### Next Steps for AI Integration

To enhance the AI integration:

1. **Add conversation memory** for multi-turn conversations
2. **Implement user authentication** for personalized experiences
3. **Add more specialized tools** for different types of queries
4. **Integrate with additional data sources** for expanded knowledge

## Customization

- Modify `lambda/chat_handler.py` to implement your chat logic
- Update `app.py` to add more resources or modify configuration
- Add environment variables in the Lambda function configuration
- Integrate with strands-agents for AI-powered responses
- Modify `Dockerfile` to add additional system packages if needed
- Customize the Knowledge Base content for different topics

## Security Notes

- The current setup allows CORS from any origin (`*`) - restrict this in production
- Consider adding authentication and authorization
- Review IAM permissions and follow least privilege principle
- Secure your AI service credentials properly
- Container images are stored in ECR - ensure proper access controls
- Knowledge Base access is restricted to your Lambda function

## Troubleshooting

### Common Issues

1. **Container build failures**: Ensure Docker is running and you have sufficient disk space
2. **Platform compatibility**: The Dockerfile uses `--platform=linux/amd64` for Lambda compatibility
3. **Dependency conflicts**: Check `lambda/requirements.txt` for version conflicts
4. **Memory limits**: Lambda is configured with 512MB memory - adjust if needed
5. **Knowledge Base access**: Verify IAM permissions and Knowledge Base configuration
6. **Environment variables**: Ensure Knowledge Base IDs are properly set

### Debugging

- Check CloudWatch logs for Lambda function errors
- Use `cdk diff` to see what changes will be deployed
- Verify container build with `docker build -t test .`
- Test Knowledge Base access with `python config.py`
- Verify environment variables are set correctly

### Knowledge Base Issues

- **Access denied**: Check IAM permissions for `bedrock:Retrieve` and `bedrock:RetrieveAndGenerate`
- **No results**: Verify Knowledge Base content is properly indexed
- **Configuration errors**: Ensure Knowledge Base ID and Data Source ID are correct
- **Region mismatch**: Verify Knowledge Base is in the same region as your Lambda
