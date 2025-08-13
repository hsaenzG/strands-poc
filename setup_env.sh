#!/bin/bash

# Setup script for Harry Potter Knowledge Base environment variables
# This script will help you create and configure your .env file

echo "🚀 Setting up Environment Variables for Harry Potter Knowledge Base"
echo "=================================================================="
echo ""

# Check if .env already exists
if [ -f ".env" ]; then
    echo "⚠️  .env file already exists. Backing up to .env.backup"
    cp .env .env.backup
fi

# Create .env file from template
echo "📝 Creating .env file from template..."
cp env.template .env

echo ""
echo "✅ .env file created successfully!"
echo ""
echo "🔧 Next steps:"
echo "1. Edit the .env file and replace the placeholder values:"
echo "   - KNOWLEDGE_BASE_ID: Your actual Knowledge Base ID"
echo "   - KNOWLEDGE_BASE_DATA_SOURCE_ID: Your actual Data Source ID"
echo ""
echo "2. Set your Knowledge Base IDs:"
echo "   - Go to Amazon Bedrock Console: https://console.aws.amazon.com/bedrock/"
echo "   - Navigate to 'Knowledge bases'"
echo "   - Note down your Knowledge Base ID and Data Source ID"
echo ""
echo "3. Update the .env file with your actual values"
echo ""
echo "4. Source the environment variables:"
echo "   source .env"
echo ""
echo "5. Deploy your stack:"
echo "   cdk deploy --profile dev-personal"
echo ""

# Make the script executable
chmod +x setup_env.sh

echo "🎯 Environment setup complete! Edit .env with your actual values."
