#!/usr/bin/env python3
"""Test import of chat handler"""

try:
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), 'lambda'))
    import chat_handler
    print("✅ Import successful!")
except Exception as e:
    print(f"❌ Import failed: {e}")
