# Render Deployment Instructions

This document provides instructions for deploying the Telegram Weather Bot on Render's free tier.

## One-Click Deploy to Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## Manual Deployment Steps

1. Create a new Web Service on Render
2. Connect your GitHub/GitLab repository
3. Use the following settings:
   - **Name**: `telegram-weather-bot` (or any name you prefer)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
4. Add the following environment variables:
   - `TELEGRAM_BOT_TOKEN`: Your Telegram Bot Token
   - `WEATHER_API_KEY`: Your OpenWeatherMap API Key
5. Deploy the service
6. After deployment, set up the webhook by visiting:
   ```
   https://YOUR-RENDER-URL.onrender.com/set-webhook?url=https://YOUR-RENDER-URL.onrender.com
   ```
7. Your bot should now be active and responding to messages!

## Important Notes

- **Free tier limitations**: Instances sleep after 15 minutes of inactivity
- **Cold start**: First request after inactivity may take 30-60 seconds
- **Usage limit**: 750 hours/month free usage
