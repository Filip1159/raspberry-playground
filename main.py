from gpiozero import LED
from time import sleep
from LCD import LCD
import requests
from threading import Thread

def is_wifi_connected():
    try:
        response = requests.get('http://worldtimeapi.org/api/timezone/Europe/Warsaw', timeout=5)
        return True
    except requests.ConnectionError:
        return False 

days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

red = LED(14)
lcd = LCD(2, 3, 4, 17, 27, 22)

lcd.write_string("Hello Raspberry")

while not is_wifi_connected():
    pass


r = requests.get('http://worldtimeapi.org/api/timezone/Europe/Warsaw')
datetime = r.json()['datetime']
print(datetime)
date = datetime[0:10]
time = datetime[11:19]
print(date)
print(time)
year = int(date[0:4])
month = int(date[5:7])
day = int(date[8:10])
hour = int(time[0:2])
minute = int(time[3:5])
second = int(time[6:8])
lcd.setCursor(1, 0)
lcd.write_string(f'{date} {time}')

def updateClock():
    global second, minute, hour, day, month, year
    while (True):
        sleep(1)
        second += 1
        if (second == 60):
            second = 0
            minute += 1
            if (minute == 60):
                minute = 0
                hour += 1
                if (hour == 24):
                    hour = 0
                    day += 1
                    if (day == days_per_month[month]):
                        day = 0
                        month += 1
                        if (month == 13):
                            year += 1
        lcd.setCursor(1, 0)
        lcd.write_string(f'{year}-{month}-{day} {hour}:{minute}:{second}')

daemon = Thread(target=updateClock, daemon=True, name='updateClock')
daemon.start()

while True:
    red.on()
    sleep(0.2)
    red.off()
    sleep(0.2)
