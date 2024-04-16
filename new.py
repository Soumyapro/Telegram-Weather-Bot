import time
import requests
import schedule

def fetch_weather_data():

    url = "https://api.openweathermap.org/data/2.5/weather"
    city = "Kolkata"
    try:
        with open('api_key.txt','r') as file:
            api_key = file.read()
    except:
        print("file could not be opened")

    params = {'q': city, 'appid': api_key}

    try:
        res = requests.get(url, params=params)
        res.raise_for_status()
        data = res.json()
    except requests.exceptions.RequestException as e:
        print("error fetching the data..",e)

    sky_cond = data['weather'][0]['main']
    temp = data['main']['temp']
    feels = data['main']['feels_like']
    weather_msg = ""

    if sky_cond=="Haze" or sky_cond=="Cloudy" or sky_cond=="Cloud" or sky_cond=="Rain" or sky_cond=="Rainy" or sky_cond=="Showers":
        print("Take an Umbrella with u")
        weather_msg = f"Today Sky looks like {sky_cond}. Please Don't forget to take an umbrella before leaving the house."

    return weather_msg

def send_telegram_message(bot_token, chat_id, message):

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {'chat_id': chat_id, 'text': message}
    response = requests.post(url, data=params)
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print("Failed to send message.")

def tele_bot():

    bot_token = '6732713022:AAHEDwJ6qHEviR50J4NMydj8DNGFG724qqw'
    chat_id = '6696755487'
    sky_cond = fetch_weather_data()
    message = "Good morning :) "+ sky_cond
    send_telegram_message(bot_token, chat_id, message)

if __name__=="__main__":
    schedule.every().day.at("07:56").do(tele_bot)

while True:
    schedule.run_pending()
    time.sleep(1)
