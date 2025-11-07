"""
Test script to validate connection with Claude API.

This script performs a simple test to ensure:
1. API key is properly configured
2. Connection to Anthropic API works
3. Claude model responds correctly
4. Token usage is tracked
"""

import os
from dotenv import load_dotenv
from anthropic import Anthropic

def test_claude_api():
    """
    Test connection to Claude API with a simple prompt.

    Returns:
        bool: True if test succeeds, False otherwise
    """
    print("=" * 60)
    print("TESTING CONNECTION TO CLAUDE API")
    print("=" * 60)

    # Load environment variables
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        print("\n❌ ERROR: ANTHROPIC_API_KEY not found in environment variables")
        print("   Please ensure .env file exists and contains your API key")
        return False

    print(f"\n✓ API key found (length: {len(api_key)} chars)")

    try:
        # Initialize Anthropic client
        client = Anthropic(api_key=api_key)
        print("✓ Anthropic client initialized")

        # Make test request
        print("\n📤 Sending test message to Claude...")
        print("   Model: claude-3-5-haiku-20241022")
        print("   Prompt: 'Hello from Paper Agent! Please respond with a greeting.'")

        response = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=100,
            messages=[{
                "role": "user",
                "content": "Hello from Paper Agent! Please respond with a greeting."
            }]
        )

        # Extract response content
        response_text = response.content[0].text

        print("\n" + "=" * 60)
        print("📥 RESPONSE FROM CLAUDE")
        print("=" * 60)
        print(f"\n{response_text}\n")

        # Display token usage
        print("=" * 60)
        print("📊 TOKEN USAGE")
        print("=" * 60)
        print(f"  Input tokens:  {response.usage.input_tokens}")
        print(f"  Output tokens: {response.usage.output_tokens}")
        print(f"  Total tokens:  {response.usage.input_tokens + response.usage.output_tokens}")
        print("=" * 60)

        print("\n✅ TEST PASSED: Connection to Claude API is working!")
        return True

    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        print("\nPossible issues:")
        print("  - Invalid API key")
        print("  - Network connection problems")
        print("  - API rate limits exceeded")
        return False

if __name__ == "__main__":
    success = test_claude_api()
    exit(0 if success else 1)
