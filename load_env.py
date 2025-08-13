#!/usr/bin/env python3
"""
Environment Variables Loader for Harry Potter Knowledge Base

This script helps load and validate environment variables from your .env file.
Run this script to check if your environment is properly configured.
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

def load_environment() -> Dict[str, Any]:
    """Load environment variables from .env file"""
    # Load .env file if it exists
    if os.path.exists('.env'):
        load_dotenv('.env')
        print("✅ .env file loaded successfully")
    else:
        print("⚠️  .env file not found. Using system environment variables.")
    
    # Define required environment variables
    required_vars = {
        'REGION_NAME': 'AWS region for your resources',
        'MODEL_ID': 'Bedrock model ID for Claude',
        'KNOWLEDGE_BASE_ID': 'Your Amazon Knowledge Base ID',
        'KNOWLEDGE_BASE_DATA_SOURCE_ID': 'Your Knowledge Base Data Source ID'
    }
    
    # Define optional environment variables
    optional_vars = {
        'AWS_PROFILE': 'AWS profile for local development',
        'LAMBDA_TIMEOUT': 'Lambda function timeout in seconds',
        'LAMBDA_MEMORY': 'Lambda function memory in MB',
        'CORS_ORIGIN': 'CORS origin for API Gateway',
        'API_STAGE': 'API Gateway stage name',
        'LOG_LEVEL': 'Logging level'
    }
    
    # Check required variables
    print("\n🔍 Checking Required Environment Variables:")
    print("=" * 50)
    
    missing_vars = []
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value and value != f"YOUR_{var}_HERE":
            print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: Not set or using placeholder value")
            missing_vars.append(var)
    
    # Check optional variables
    print("\n🔍 Checking Optional Environment Variables:")
    print("=" * 50)
    
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {value}")
        else:
            print(f"⚪ {var}: Not set (optional)")
    
    # Summary
    print("\n📊 Summary:")
    print("=" * 50)
    
    if missing_vars:
        print(f"❌ {len(missing_vars)} required variables are missing or using placeholder values:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n🔧 To fix this:")
        print("1. Edit your .env file")
        print("2. Replace placeholder values with actual values")
        print("3. Run this script again to verify")
        return False
    else:
        print("✅ All required environment variables are properly configured!")
        print("\n🚀 You're ready to deploy your stack!")
        return True

def validate_knowledge_base_config() -> bool:
    """Validate Knowledge Base configuration"""
    kb_id = os.getenv('KNOWLEDGE_BASE_ID')
    ds_id = os.getenv('KNOWLEDGE_BASE_DATA_SOURCE_ID')
    
    if not kb_id or kb_id == "YOUR_KNOWLEDGE_BASE_ID_HERE":
        print("\n❌ Knowledge Base ID not configured")
        return False
    
    if not ds_id or ds_id == "YOUR_DATA_SOURCE_ID_HERE":
        print("\n❌ Knowledge Base Data Source ID not configured")
        return False
    
    print(f"\n✅ Knowledge Base configured:")
    print(f"   - Knowledge Base ID: {kb_id}")
    print(f"   - Data Source ID: {ds_id}")
    return True

def main():
    """Main function"""
    print("🚀 Harry Potter Knowledge Base Environment Checker")
    print("=" * 60)
    
    # Load environment
    env_loaded = load_environment()
    
    if env_loaded:
        # Validate Knowledge Base config
        kb_valid = validate_knowledge_base_config()
        
        if kb_valid:
            print("\n🎉 All systems are go! You can now deploy your stack.")
            print("\n📝 Next steps:")
            print("1. Deploy your stack: cdk deploy --profile dev-personal")
            print("2. Test your API endpoints")
            print("3. Ask Harry Potter questions!")
        else:
            print("\n⚠️  Knowledge Base not properly configured.")
            print("Please update your .env file with actual Knowledge Base IDs.")
    else:
        print("\n⚠️  Environment not properly configured.")
        print("Please fix the missing variables before proceeding.")

if __name__ == "__main__":
    main()
