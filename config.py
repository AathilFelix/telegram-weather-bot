import os
from dotenv import load_dotenv

print(f"Current directory: {os.getcwd()}")
# Load environment variables from .env file
print("Loading .env file...")
load_dotenv()

# Get API keys from environment variables
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
api_key = os.getenv('WEATHER_API_KEY')

print("Environment variables:")
for key, value in os.environ.items():
    if key in ["TELEGRAM_BOT_TOKEN", "WEATHER_API_KEY"]:
        print(f"{key}: {'*' * len(value)}")  # Don't print actual secrets

# Validate that required environment variables are set
if not bot_token:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")
if not api_key:
    raise ValueError("WEATHER_API_KEY environment variable is required")
