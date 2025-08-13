# Chat API with CDK and Container-based Lambda

This project creates an AWS API Gateway with a chat endpoint using AWS CDK and a container-based Lambda function with Python 3.12, featuring **working** integration with strands-agents and a specialized Harry Potter Knowledge Base.

## 🎉 Current Status: FULLY WORKING

- ✅ **API Endpoints**: Both `/health` and `/chat` are responding correctly
- ✅ **AI Integration**: Claude 3 Sonnet via Amazon Bedrock is working perfectly
- ✅ **Knowledge Base**: Harry Potter Knowledge Base integration is enabled and functional
- ✅ **No Import Errors**: All dependency and import issues have been resolved
- ✅ **Container Deployment**: Docker-based Lambda is working correctly

## Architecture

- **API Gateway**: REST API with CORS enabled
- **Lambda Function**: Container-based Python 3.12 runtime handling chat requests
- **AI Integration**: **WORKING** strands-agents integration with Claude 3 Sonnet via Amazon Bedrock
- **Knowledge Base**: **WORKING** Amazon Bedrock Knowledge Base for Harry Potter books and lore
- **Endpoints**:
  - `POST /chat` - Chat endpoint for sending messages with Knowledge Base access ✅
  - `GET /health` - Health check endpoint ✅

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
python -c "import strands; print('strands-agents installed successfully')"
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

**Option 1: Use the provided setup script**
```bash
# Run the setup script
./setup_env.sh

# Edit the .env file with your actual Knowledge Base IDs
nano .env
```

**Option 2: Set environment variables manually**
```bash
# Set your actual Knowledge Base IDs
export KNOWLEDGE_BASE_ID="your-actual-kb-id"
export KNOWLEDGE_BASE_ID="your-actual-ds-id"
export REGION_NAME="us-east-1"
export MODEL_ID="anthropic.claude-3-sonnet-20240229-v1:0"
```

**Option 3: Update app.py directly**
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

2. **Force rebuild** (if you've made changes to dependencies):
   ```bash
   cdk deploy --profile dev-personal --force
   ```

## Testing

### API Testing

After deployment, test the endpoints:

#### Health Check
```bash
curl -X GET "https://your-api-id.execute-api.region.amazonaws.com/prod/health"
```

**Expected Response:**
```json
{
  "status": "healthy",
  "message": "Chat API is running with Claude integration via Strands and Harry Potter Knowledge Base",
  "model": "anthropic.claude-3-sonnet-20240229-v1:0",
  "region": "us-east-1",
  "framework": "strands-agents",
  "knowledge_base_configured": true,
  "timestamp": 29999
}
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

**Expected Response:**
```json
{
  "response": "Detailed Harry Potter information...",
  "user_id": "test_user",
  "model": "anthropic.claude-3-sonnet-20240229-v1:0",
  "framework": "strands-agents",
  "knowledge_base_enabled": true,
  "timestamp": 19623
}
```

## Development

- **Local development**: Use `cdk synth` to generate CloudFormation template
- **Watch mode**: Use `cdk watch` for automatic deployment on changes
- **Destroy stack**: Use `cdk destroy --profile dev-personal` to remove all resources
- **View differences**: Use `cdk diff --profile dev-personal` to see changes before deployment
- **Force rebuild**: Use `cdk deploy --profile dev-personal --force` when changing dependencies

## Project Structure

```
.
├── app.py                 # Main CDK application with Knowledge Base integration
├── cdk.json             # CDK configuration
├── config.py             # Knowledge Base configuration and setup instructions
├── requirements.txt     # Python dependencies for CDK (including strands-agents)
├── Dockerfile           # Container configuration for Lambda
├── lambda/              # Lambda function code
│   ├── __init__.py
│   ├── requirements.txt # Lambda-specific dependencies (simplified)
│   └── chat_handler.py  # Lambda handler with WORKING Knowledge Base integration
├── .env                 # Environment variables (created from env.template)
├── env.template         # Template for environment variables
├── setup_env.sh         # Script to set up environment variables
├── load_env.py          # Script to validate environment configuration
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

### Dependencies (Simplified and Working)

The Lambda function uses a minimal, working set of dependencies:
```txt
boto3>=1.26.0
strands-agents>=1.4.0
```

**Why This Works:**
- Removed conflicting packages (`strands-agents-tools`, `strands-agents-builder`)
- Uses the correct `@tool` decorator from `strands.tools`
- Simplified dependency tree prevents import conflicts

## Harry Potter Knowledge Base Integration

This project includes a **WORKING** Knowledge Base for Harry Potter books and lore:

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

### Knowledge Base Tool

The integration includes a specialized tool:
```python
@tool(name="search_harry_potter_knowledge", 
      description="Search the Harry Potter Knowledge Base for detailed information about characters, plot, spells, creatures, and lore from the books")
def search_knowledge_base(query: str) -> str:
    # Implementation using bedrock-agent-runtime client
```

## strands-agents Integration

This project is **FULLY WORKING** with strands-agents for AI-powered chat functionality:

- ✅ **Working chat endpoint** with Knowledge Base integration
- ✅ **strands-agents integration** - all dependencies working correctly
- ✅ **Python 3.12 runtime** - compatible with latest strands-agents versions
- ✅ **Amazon Bedrock integration** - working with Claude 3 Sonnet
- ✅ **Knowledge Base tools** - specialized tools for Harry Potter information

### AI Model Configuration

The Lambda function is configured with:
- **Model ID**: `anthropic.claude-3-sonnet-20240229-v1:0`
- **Service**: Amazon Bedrock
- **Region**: `us-east-1` (configurable)
- **Knowledge Base**: Harry Potter books and lore

### Working Features

1. **Tool Integration**: Uses `@tool` decorator for Knowledge Base search
2. **Agent Management**: Properly initializes Strands Agent with tools
3. **Error Handling**: Graceful fallback when Knowledge Base is unavailable
4. **Response Formatting**: Structured responses with metadata

## Environment Configuration

### Environment Variables

The project uses several configuration files for easy setup:

- **`.env`**: Your actual environment variables (created from template)
- **`env.template`**: Template with placeholder values
- **`setup_env.sh`**: Script to create and configure `.env`
- **`load_env.py`**: Script to validate your environment configuration

### Quick Environment Setup

```bash
# 1. Run the setup script
./setup_env.sh

# 2. Edit .env with your actual Knowledge Base IDs
nano .env

# 3. Validate your configuration
python load_env.py

# 4. Deploy your stack
cdk deploy --profile dev-personal
```

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

### ✅ Resolved Issues

1. **Import Error**: `cannot import name 'Tool' from 'strands.tools'` - **FIXED**
   - Solution: Use `@tool` decorator instead of non-existent `Tool` class
   - Import: `from strands.tools import tool`

2. **Dependency Conflicts**: `pydantic_core` import errors - **FIXED**
   - Solution: Simplified `lambda/requirements.txt` to essential packages only
   - Removed conflicting packages: `strands-agents-tools`, `strands-agents-builder`

3. **Container Build Issues**: Architecture mismatches - **FIXED**
   - Solution: Dockerfile uses `--platform=linux/amd64` for Lambda compatibility

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
- Use `python load_env.py` to validate your configuration

### Knowledge Base Issues

- **Access denied**: Check IAM permissions for `bedrock:Retrieve` and `bedrock:RetrieveAndGenerate`
- **No results**: Verify Knowledge Base content is properly indexed
- **Configuration errors**: Ensure Knowledge Base ID and Data Source ID are correct
- **Region mismatch**: Verify Knowledge Base is in the same region as your Lambda

## Recent Fixes and Improvements

### Version 2.0 - Working Knowledge Base Integration

- ✅ **Fixed Import Errors**: Resolved `Tool` import issues with correct `@tool` decorator
- ✅ **Simplified Dependencies**: Streamlined `lambda/requirements.txt` to prevent conflicts
- ✅ **Working Container**: Docker-based Lambda is fully functional
- ✅ **Knowledge Base Integration**: Harry Potter Knowledge Base is working correctly
- ✅ **Environment Management**: Added `.env` files and validation scripts
- ✅ **API Endpoints**: Both health and chat endpoints are responding correctly

### What Was Fixed

1. **Import Statement**: Changed from `from strands.tools import Tool` to `from strands.tools import tool`
2. **Tool Creation**: Used `@tool` decorator instead of non-existent `Tool` class
3. **Dependencies**: Removed conflicting packages and simplified requirements
4. **Container Build**: Fixed architecture and dependency issues
5. **Environment Setup**: Added comprehensive configuration management

The project is now **production-ready** with a fully working Harry Potter Knowledge Base integration! 🎉
