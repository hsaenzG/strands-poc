"""
Configuration file for Harry Potter Knowledge Base integration

This file contains the configuration settings and instructions for setting up
your Amazon Knowledge Base with Harry Potter books information.
"""

# Knowledge Base Configuration
# Replace these placeholder values with your actual Knowledge Base IDs
KNOWLEDGE_BASE_CONFIG = {
    "KNOWLEDGE_BASE_ID": "YOUR_KNOWLEDGE_BASE_ID_HERE",
    "KNOWLEDGE_BASE_DATA_SOURCE_ID": "YOUR_DATA_SOURCE_ID_HERE",
    "REGION": "us-east-1"
}

# Instructions for setting up your Knowledge Base:
KNOWLEDGE_BASE_SETUP_INSTRUCTIONS = """
To set up your Harry Potter Knowledge Base:

1. Go to Amazon Bedrock Console: https://console.aws.amazon.com/bedrock/
2. Navigate to "Knowledge bases" in the left sidebar
3. Click "Create knowledge base"
4. Choose a name (e.g., "Harry-Potter-Books")
5. Select your preferred embedding model
6. Create a data source:
   - Choose "S3" as the data source type
   - Upload your Harry Potter books content (PDF, TXT, etc.)
   - Or use existing S3 bucket with Harry Potter content
7. After creation, note down:
   - Knowledge Base ID (found in the Knowledge Base details)
   - Data Source ID (found in the Data Sources tab)

Then update the environment variables in app.py:
- KNOWLEDGE_BASE_ID: Your Knowledge Base ID
- KNOWLEDGE_BASE_DATA_SOURCE_ID: Your Data Source ID

Or set them as environment variables before deployment:
export KNOWLEDGE_BASE_ID="your-kb-id"
export KNOWLEDGE_BASE_DATA_SOURCE_ID="your-ds-id"
"""

# Example Harry Potter content structure for Knowledge Base
EXAMPLE_CONTENT_STRUCTURE = """
Recommended content structure for your Knowledge Base:

1. Book Summaries:
   - Harry Potter and the Philosopher's Stone
   - Harry Potter and the Chamber of Secrets
   - Harry Potter and the Prisoner of Azkaban
   - Harry Potter and the Goblet of Fire
   - Harry Potter and the Order of Phoenix
   - Harry Potter and the Half-Blood Prince
   - Harry Potter and the Deathly Hallows

2. Character Profiles:
   - Main characters (Harry, Ron, Hermione, etc.)
   - Supporting characters
   - Villains and antagonists
   - Character relationships and development

3. Magical Elements:
   - Spells and incantations
   - Potions and ingredients
   - Magical creatures
   - Magical objects and artifacts

4. Locations:
   - Hogwarts School of Witchcraft and Wizardry
   - Diagon Alley
   - Platform 9¾
   - Various magical locations

5. Plot Details:
   - Chapter summaries
   - Key events and plot points
   - Themes and motifs
   - Literary analysis
"""

# Environment variable setup script
ENV_SETUP_SCRIPT = """
# Add this to your shell profile or run before deployment
export KNOWLEDGE_BASE_ID="your-actual-kb-id"
export KNOWLEDGE_BASE_DATA_SOURCE_ID="your-actual-ds-id"
export REGION_NAME="us-east-1"
export MODEL_ID="anthropic.claude-3-sonnet-20240229-v1:0"
"""

if __name__ == "__main__":
    print("Harry Potter Knowledge Base Configuration")
    print("=" * 50)
    print(KNOWLEDGE_BASE_SETUP_INSTRUCTIONS)
    print("\n" + "=" * 50)
    print("Example Content Structure:")
    print(EXAMPLE_CONTENT_STRUCTURE)
    print("\n" + "=" * 50)
    print("Environment Variables Setup:")
    print(ENV_SETUP_SCRIPT)
