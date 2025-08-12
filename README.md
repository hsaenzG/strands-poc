# Chat API with CDK and Container-based Lambda

This project creates an AWS API Gateway with a chat endpoint using AWS CDK and a container-based Lambda function with Python 3.12, featuring integration capabilities for strands-agents.

## Architecture

- **API Gateway**: REST API with CORS enabled
- **Lambda Function**: Container-based Python 3.12 runtime handling chat requests
- **AI Integration**: Ready for strands-agents integration with Claude 3 Sonnet via Amazon Bedrock
- **Endpoints**:
  - `POST /chat` - Chat endpoint for sending messages
  - `GET /health` - Health check endpoint

## Prerequisites

- **Python 3.12** (required for strands-agents compatibility)
- **Docker** (required for building Lambda container)
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

### 6. Bootstrap CDK

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

#### Chat Endpoint
```bash
curl -X POST "https://your-api-id.execute-api.region.amazonaws.com/prod/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, world!", "user_id": "test_user"}'
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
├── requirements.txt     # Python dependencies (including strands-agents)
├── Dockerfile           # Container configuration for Lambda
├── lambda/              # Lambda function code
│   ├── __init__.py
│   ├── requirements.txt # Lambda-specific dependencies
│   └── chat_handler.py  # Lambda handler
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

## strands-agents Integration

This project is set up to work with strands-agents for AI-powered chat functionality. The current implementation includes:

- **Basic chat endpoint** with echo functionality
- **strands-agents ready** - all dependencies installed
- **Python 3.12 runtime** - compatible with latest strands-agents versions
- **Amazon Bedrock integration** - ready for Claude 3 Sonnet

### AI Model Configuration

The Lambda function is configured with:
- **Model ID**: `anthropic.claude-3-sonnet-20240229-v1:0`
- **Service**: Amazon Bedrock
- **Region**: `us-east-1` (configurable)

### Next Steps for AI Integration

To integrate with actual AI models:

1. **Configure environment variables** for your AI service
2. **Update the Lambda function** to use strands-agents
3. **Add authentication** for your AI service
4. **Implement conversation memory** if needed

## Customization

- Modify `lambda/chat_handler.py` to implement your chat logic
- Update `app.py` to add more resources or modify configuration
- Add environment variables in the Lambda function configuration
- Integrate with strands-agents for AI-powered responses
- Modify `Dockerfile` to add additional system packages if needed

## Security Notes

- The current setup allows CORS from any origin (`*`) - restrict this in production
- Consider adding authentication and authorization
- Review IAM permissions and follow least privilege principle
- Secure your AI service credentials properly
- Container images are stored in ECR - ensure proper access controls

## Troubleshooting

### Common Issues

1. **Container build failures**: Ensure Docker is running and you have sufficient disk space
2. **Platform compatibility**: The Dockerfile uses `--platform=linux/amd64` for Lambda compatibility
3. **Dependency conflicts**: Check `lambda/requirements.txt` for version conflicts
4. **Memory limits**: Lambda is configured with 512MB memory - adjust if needed

### Debugging

- Check CloudWatch logs for Lambda function errors
- Use `cdk diff` to see what changes will be deployed
- Verify container build with `docker build -t test .`
