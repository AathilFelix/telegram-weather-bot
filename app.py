from flask import Flask, request, jsonify
import telegram_api
import weather_api
import city_api
import config
import requests
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    """Root endpoint that confirms the bot is running"""
    return "✅ Telegram Weather Bot is running! Your webhook is active."

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming updates from Telegram"""
    try:
        # Get the update from Telegram
        update = request.get_json()
        logger.info(f"Received update: {update}")
        
        # Extract message and chat ID
        message_text = None
        chat_id = None
        
        if "message" in update:
            message = update.get("message", {})
            message_text = message.get("text")
            chat_id = message.get("chat", {}).get("id")
        
        if not message_text or not chat_id:
            return jsonify({"status": "ok", "message": "No message text or chat ID found"})
        
        logger.info(f"Received message: '{message_text}' from chat ID: {chat_id}")
        
        # Check for commands
        if message_text == '/start':
            welcome_message = """👋 Welcome to Weather Bot!

🌤️ Simply send me the name of any city, and I'll provide you with the current weather information.

Try it now! Send a city name like "London" or "New York".
"""
            telegram_api.send_message(chat_id, welcome_message)
            return jsonify({"status": "ok"})
        
        if message_text == '/help':
            help_message = """🌤️ **Weather Bot Help**

**Usage:**
Just send me any city name, and I'll tell you the current weather there!

**Examples:**
• London
• New York
• Tokyo
• Sydney

**Commands:**
• /start - Start the bot
• /help - Show this help message
"""
            telegram_api.send_message(chat_id, help_message)
            return jsonify({"status": "ok"})
        
        # Check if it's a valid city
        if city_api.get_valid(message_text):
            try:
                # Get weather data for the city
                weather_data = weather_api.get_weather_data(message_text.strip())
                telegram_api.send_message(chat_id, weather_data)
            except Exception as e:
                logger.error(f"Error getting weather data: {e}")
                telegram_api.send_message(chat_id, "Sorry, I couldn't fetch weather data. Please try again later.")
        else:
            telegram_api.send_message(
                chat_id, "Invalid City Name/City Not enlisted in our database"
            )
        
        return jsonify({"status": "ok"})
    
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/set-webhook', methods=['GET'])
def set_webhook():
    """Set the Telegram webhook to this server"""
    url = request.args.get('url')
    if not url:
        # Try to get URL from environment variable
        url = os.environ.get('RENDER_EXTERNAL_URL')
        if not url:
            return jsonify({"error": "No URL provided"}), 400
    
    webhook_url = f"{url}/webhook"
    logger.info(f"Setting webhook to: {webhook_url}")
    
    # Set the webhook with Telegram
    telegram_url = f"https://api.telegram.org/bot{config.bot_token}/setWebhook"
    payload = {"url": webhook_url}
    
    try:
        response = requests.post(telegram_url, json=payload)
        result = response.json()
        logger.info(f"Set webhook response: {result}")
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error setting webhook: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "telegram-weather-bot",
        "version": "1.0.0"
    })

if __name__ == "__main__":
    # Get port from environment (Render sets this)
    port = int(os.environ.get("PORT", 4999))
    
    # Auto-set webhook if we're running in Render
    render_url = os.environ.get('RENDER_EXTERNAL_URL')
    if render_url:
        requests.get(f"{render_url}/set-webhook?url={render_url}")
        logger.info(f"Automatically set webhook to {render_url}/webhook")
    
    app.run(host="0.0.0.0", port=port)
