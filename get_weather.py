import requests, time, datetime, sys


def get_weather(message):
    message.pop(0)
    *country, city = message
    key = '3f67c853294f2b1b8823a1ddf2de888a'
    response = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?q={city},{country}&exclude=current&appid={key}').json()
    if response['cod'] == 200:
        i = response
        lon, lat = i['coord']['lon'], i['coord']['lat']
        sunrise, sunset = i['sys']['sunrise'], i['sys']['sunset']
        name = i['name']
        country = i['sys']['country'].capitalize()
        feels_like = i['main']['feels_like'] - 273.15
        description = i['weather'][0]['description']
        sunrise = str(datetime.datetime.strptime(time.ctime(sunrise), "%a %b %d %H:%M:%S %Y")).split()[1]
        sunset = str(datetime.datetime.strptime(time.ctime(sunset), "%a %b %d %H:%M:%S %Y")).split()[1]
        t = i['timezone'] // 3600
        date, now = str(datetime.datetime.utcnow() + datetime.timedelta(hours=t)).split()
        t = f'UTC {"+" * (t > 0)}{t}'
        return (f'Высота: {lon}, Широта: {lat}\n'
                f'Название города: {name}, {country}\n'
                f'Время восхода солнца: {sunrise} \n'
                f'Время заката солнца: {sunset}\n'
                f'Температура: {round(feels_like, 2)}°C\n'
                f'Состояние: {description}\n'
                f'Временная зона: {t}\n'
                f'Время: {now[:9]}\n'
                f'Дата: {date}')
    else:
        try:
            message.append('')
            message[-2] = message[-2] + ' ' + message[-1]
            message.pop(-1)
            get_weather(message)
        except Exception:
            return f'Не удалось ничего найти по Вашему запросу'


print(get_weather(sys.argv))
