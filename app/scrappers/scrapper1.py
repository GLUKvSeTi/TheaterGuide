import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy import insert, select, update

from app.backend.db_depends import get_db
from app.schemas import CreateEvent
from app.models import Event
from app.backend.db import SessionLocal, engine


def parse_tt_afisha():
    with Session(autoflush=False, bind=engine) as db:
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
                    #duration = event.find('div', class_='performances-card__time-duration').get_text(strip=True)
                    #price = event.find('div', class_='afisha__price')  # Цена билета
                    description = event.find('div', class_='performances-card__description').get_text(strip=True)
                    #link = event.find('a', class_='btn performances-card__buy btn--buy')
                    new_event = Event(theater_name='Театр-театр', title=title, date=date, time=time,
                                      description=description)

                    db.add(new_event)
                    events.append({
                        'title': title,
                        'date': date,
                        'time': time,
                        #'price': price
                        #'duration': duration,
                        'description': description,
                        #'link': link
                    })

                except AttributeError as e:
                    print(f'Ошибка при извлечении данных для одного из концертов: {e}')
        db.commit()
        db.close()
        return events


