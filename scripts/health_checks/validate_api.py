"""
API validation script - Health check for Claude API connection.

This script performs a simple test to ensure:
1. API key is properly configured
2. Connection to Anthropic API works
3. Claude model responds correctly
4. Token usage and costs are tracked

This is a MANUAL validation tool for local development.
For automated tests, see tests/unit/ and tests/integration/.
"""

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT_STR = str(PROJECT_ROOT)
if PROJECT_ROOT_STR not in sys.path:
    sys.path.insert(0, PROJECT_ROOT_STR)

from scripts.common import setup_project_path

setup_project_path()

from dotenv import load_dotenv
from anthropic import Anthropic
from utils.cost_tracker import CostTracker


def validate_api_connection():
    """
    Validate connection to Claude API with a simple test.

    Returns:
        bool: True if validation succeeds, False otherwise
    """
    print("=" * 60)
    print("CLAUDE API HEALTH CHECK")
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
        model = "claude-3-5-haiku-20241022"
        print(f"\n📤 Sending test message to Claude...")
        print(f"   Model: {model}")
        print("   Prompt: 'Hello from Paper Agent! Please respond with a greeting.'")

        response = client.messages.create(
            model=model,
            max_tokens=100,
            messages=[{
                "role": "user",
                "content": "Hello from Paper Agent! Please respond with a greeting."
            }]
        )

        # Extract response content
        response_text = response.content[0].text
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        total_tokens = input_tokens + output_tokens

        print("\n" + "=" * 60)
        print("📥 RESPONSE FROM CLAUDE")
        print("=" * 60)
        print(f"\n{response_text}\n")

        # Calculate costs using CostTracker
        costs = CostTracker.calculate_cost(model, input_tokens, output_tokens)

        # Display token usage and costs
        print("=" * 60)
        print("📊 TOKEN USAGE & COST ANALYSIS")
        print("=" * 60)
        print(f"  Input tokens:  {input_tokens}")
        print(f"  Output tokens: {output_tokens}")
        print(f"  Total tokens:  {total_tokens}")
        print()
        print(f"  💰 Cost (Haiku rates):")
        print(f"     Input:  {CostTracker.format_cost(costs['input_cost'])}")
        print(f"     Output: {CostTracker.format_cost(costs['output_cost'])}")
        print(f"     Total:  {CostTracker.format_cost(costs['total_cost'])}")
        print("=" * 60)

        print("\n✅ VALIDATION PASSED: API connection is healthy!")
        print(f"   Model: {model}")
        print(f"   Cost per request: ~{CostTracker.format_cost(costs['total_cost'])}")
        return True

    except Exception as e:
        print(f"\n❌ VALIDATION FAILED: {str(e)}")
        print("\nPossible issues:")
        print("  - Invalid API key")
        print("  - Network connection problems")
        print("  - API rate limits exceeded")
        print("  - Model not available")
        return False


if __name__ == "__main__":
    success = validate_api_connection()
    exit(0 if success else 1)
