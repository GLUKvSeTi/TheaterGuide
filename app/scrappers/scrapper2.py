import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from app.backend.db import SessionLocal, engine
from app.models import Event


def parse_tuz_afisha():
    with Session(autoflush=False, bind=engine) as db:
        events = []

        for i in range(1, 5):
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

                db.add(new_event)
                db.commit()
                events.append({
                    'title': title,
                    'description': description,
                    'date': date,
                    'time': time
                })
        db.close()
        return events


events = parse_tuz_afisha()
for event in events:
    print(event)
