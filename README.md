# Chat API with CDK

This project creates an AWS API Gateway with a chat endpoint using AWS CDK and Python 3.12, with integration capabilities for strands-agents.

## Architecture

- **API Gateway**: REST API with CORS enabled
- **Lambda Function**: Python 3.12 runtime handling chat requests
- **AI Integration**: Ready for strands-agents integration
- **Endpoints**:
  - `POST /chat` - Chat endpoint for sending messages
  - `GET /health` - Health check endpoint

## Prerequisites

- **Python 3.12** (required for strands-agents compatibility)
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

### 2. Create Virtual Environment

```bash
# Create virtual environment with Python 3.12
python3.12 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Verify Python version
python --version  # Should show Python 3.12.x
```

### 3. Install Dependencies

```bash
# Install project dependencies
pip install -r requirements.txt

# Verify strands-agents installation
python test_strands.py
```

### 4. Install AWS CDK CLI

```bash
npm install -g aws-cdk
```

### 5. Bootstrap CDK

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

### Local Testing

Before deploying, test the Lambda function locally:

```bash
# Test basic Lambda functionality
python test_local.py

# Test strands-agents integration
python test_strands.py
```

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

## Project Structure

```
.
├── app.py                 # Main CDK application
├── cdk.json             # CDK configuration
├── requirements.txt     # Python dependencies (including strands-agents)
├── lambda/              # Lambda function code
│   ├── __init__.py
│   └── chat_handler.py  # Lambda handler
├── test_local.py        # Local testing script
├── test_strands.py      # strands-agents testing script
├── venv/                # Python 3.12 virtual environment
└── README.md            # This file
```

## strands-agents Integration

This project is set up to work with strands-agents for AI-powered chat functionality. The current implementation includes:

- **Basic chat endpoint** with echo functionality
- **strands-agents ready** - all dependencies installed
- **Python 3.12 runtime** - compatible with latest strands-agents versions

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

## Security Notes

- The current setup allows CORS from any origin (`*`) - restrict this in production
- Consider adding authentication and authorization
- Review IAM permissions and follow least privilege principle
- Secure your AI service credentials properly
