# Telegram Weather Bot

A Telegram bot that provides real-time weather updates. It fetches the latest weather information based on user input and responds in chat

## Features

### Get Current Weather:

Receive up to date weather details for any viable location provided by the user in the chat

### Location Support:

Responds to city names shared in the chat using a city api to validate those names

### Instant replies:

Bot delivers weather info in realtime instantly

## Getting Started

### Prerequisites

- Python 3.9 and above installed
- A Telegram account
- A Telegram bot token (obtainable from BotFather on Telegram)
- API key from a weather data provider (OpenWeatherMap)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/AathilFelix/telegram-weather-bot.git
   cd telegram-weather-bot
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your environment:**

   Copy the example environment file and add your configuration:

   ```bash
   cp .env.example .env
   ```

   Edit the `.env` file and add your API keys:

   ```env
   TELEGRAM_BOT_TOKEN=your-telegram-bot-token
   WEATHER_API_KEY=your-weather-api-key
   ```

4. **Run the bot:**
   ```bash
   python main.py
   ```

## Configuration

### Getting API Keys

1. **Telegram Bot Token:**

   - Message [@BotFather](https://t.me/botfather) on Telegram
   - Create a new bot with `/newbot`
   - Follow the instructions to get your bot token

2. **Weather API Key:**
   - Sign up at [OpenWeatherMap](https://openweathermap.org/api)
   - Get your free API key from the dashboard

## Usage

Once the bot is running:

1. Start a chat with your bot on Telegram
2. Send any city name to get weather information
3. The bot will validate the city and return current weather data

## Project Structure

```
telegram-weather-bot/
├── main.py           # Main bot application
├── telegram_api.py   # Telegram Bot API integration
├── weather_api.py    # OpenWeatherMap API integration
├── city_api.py       # City validation API
├── config.py         # Configuration management
├── requirements.txt  # Python dependencies
├── .env.example      # Environment variables template
└── README.md         # Project documentation
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).
