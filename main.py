# main.py

import requests as rq
import city_api
import weather_api
import telegram_api
import time


while True:
    try:
        # Get new updates only (not previously processed ones)
        data = telegram_api.get_updates(offset=telegram_api.get_next_offset(), limit=1, timeout=30)
        
        if data and data.get('result'):
            for update in data['result']:
                chat_id = telegram_api.get_chatid_from_update(update)
                message_text = telegram_api.get_message_from_update(update)
                update_id = update.get('update_id')
                
                if chat_id is None or message_text is None:
                    # Still update the offset to avoid reprocessing this update
                    telegram_api.update_highest_update_id(update_id)
                    continue

                if city_api.get_valid(message_text):
                    try:
                        weather_data = weather_api.get_weather_data(message_text)
                        telegram_api.send_message(chat_id, weather_data)
                    except Exception as e:
                        print(f"Error getting weather data: {e}")
                        telegram_api.send_message(chat_id, "Sorry, couldn't fetch weather data. Please try again.")
                else:
                    telegram_api.send_message(
                        chat_id, "Invalid City Name/City Not enlisted in our database"
                    )
                
                # Mark this update as processed
                telegram_api.update_highest_update_id(update_id)
        else:
            # No new updates, just wait
            time.sleep(1)
            
    except Exception as e:
        print(f"Error in main loop: {e}")
        time.sleep(5)
