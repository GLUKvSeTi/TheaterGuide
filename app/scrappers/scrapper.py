import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy import insert, select, update, func

from app.backend.db_depends import get_db
from app.schemas import CreateEvent
from app.models import Event
from app.backend.db import SessionLocal, engine
import datetime
def parse_tuz_afisha():
    with Session(autoflush=False, bind=engine) as db:
        events = []

        for i in range(1, 8):
            url = 'https://permtuz.ru/afisha/?PAGEN_1=' + str(i)
            response = requests.get(url)
            if response.status_code != 200:
                print(f'Не удалось загрузить страницу, код ответа: {response.status_code}')
                return []
            soup = BeautifulSoup(response.content, 'html.parser')
            event_cards = soup.find_all('div', class_='row afisha-list-item')

            for event in event_cards:
                title = event.find('a', class_='name').get_text(strip=True)
                description = event.find('div', class_='mark').get_text(strip=True)
                if not description:
                    description = ""
                date_time_tag = event.find('div', class_='date col-md-3')
                date, time = "", ""
                if date_time_tag:
                    date_text = date_time_tag.get_text(strip=True)
                    date_parts = date_text.split('|')
                    if len(date_parts) > 1:
                        date = (str(date_parts[0])[0: -5]).strip()
                        time = str(date_parts[1]).strip()
                new_event = Event(theater_name='ТЮЗ', title=title, date=date, time=time,
                                  description=description)
                months = {
                    "января": 1,
                    "февраля": 2,
                    "марта": 3,
                    "апреля": 4,
                    "мая": 5,
                    "июня": 6,
                    "июля": 7,
                    "августа": 8,
                    "сентября": 9,
                    "октября": 10,
                    "ноября": 11,
                    "декабря": 12
                }
                if months[date.split()[1]] != datetime.datetime.now().month or  (int(date[0:2]) > datetime.datetime.now().day and  months[date.split()[1]] == datetime.datetime.now().month):
                    db.add(new_event)
                    events.append({
                        'title': title,
                        'description': description,
                        'date': date,
                        'time': time
                    })
        db.commit()
        db.close()
        return events

def parse_tt_afisha():
    with Session(autoflush=False, bind=engine) as db:

        db.query(Event).delete()
        db.commit()
        events = []
        for i in range(1, 21):
            url = 'https://teatr-teatr.com/afisha/?PAGEN_2' +'=' + str(i)
            response = requests.get(url)
            if response.status_code != 200:
                print(f'Не удалось загрузить страницу, код ответа: {response.status_code}')
                return []
            soup = BeautifulSoup(response.content, 'html.parser')
            event_cards = soup.find_all('div', class_='afisha__item')
            if (i == 1):
                event_cards.pop(0)
            for event in event_cards:
                try:
                    title = event.find('div', class_='performances-card__name').get_text(strip=True)
                    date = event.find('div', class_='afisha__item-date').get_text(strip=True)  # Дата концерта
                    time = event.find('div', class_='performances-card__time-event').get_text(strip=True)  # Время концерта
                    description = event.find('div', class_='performances-card__description').get_text(strip=True)
                    new_event = Event(theater_name='Театр-театр', title=title, date=date, time=time,
                                      description=description)
                    months = {
                        "января": 1,
                        "февраля": 2,
                        "марта": 3,
                        "апреля": 4,
                        "мая": 5,
                        "июня": 6,
                        "июля": 7,
                        "августа": 8,
                        "сентября": 9,
                        "октября": 10,
                        "ноября": 11,
                        "декабря": 12
                    }

                    if months[date[3:]] != datetime.datetime.now().month or  (int(date[0:2]) > datetime.datetime.now().day and  months[date[3:]] == datetime.datetime.now().month):
                        db.add(new_event)
                        events.append({
                            'title': title,
                            'date': date,
                            'time': time,
                            'description': description,
                        })

                except AttributeError as e:
                    print(f'Ошибка при извлечении данных для одного из концертов: {e}')
        db.commit()
        parse_tuz_afisha()
        db.close()
        return events


