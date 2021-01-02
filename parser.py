import requests
from bs4 import BeautifulSoup as BS
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import KFC, Burgerking, Mcdonalds,  Base

engine = create_engine('sqlite:///K_F_M.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

headers = {
  'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
  'accept-encoding':'gzip, deflate, br',
  'accept-language':'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
  'cache-control':'no-cache',
  'dnt': '1',
  'pragma': 'no-cache',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'none',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
  "Content-Type": "application/json; charset=UTF-8"
   }


client = requests.Session()


def burgerking(control):
    
    counter = 1
    c_real = 1

    while (counter - c_real) < control:

        try:    
            url = f'https://burgerking.ru/map-markers-info?storeId={counter}&lat=&lon='

            r = client.get(url,  headers=headers)

            html = r.text
            soup = BS(html, "html.parser")

            if html != 'К сожалению, произошла ошибка.':

                rest = soup.find_all('p')
                
                company = str(url).replace('/', ' ').split(' ')[2]
                city = str(rest[0]).replace('<', ' ').replace('>', ' ').split(' ')[3]
                address = str(rest[1]).replace('<', '-').replace('>', '-').split('-')[2]
                working_hours = str(rest[3]).replace('<', '*').replace('>', '*').split('*')[4]
                phone = str(rest[4]).replace('<', '*').replace('>', '*').split('*')[4]
                
#                 print(counter)
                print(c_real)
                print('company:', company)
                print('city:', city)
                print('address:', address)
                print('working_hours:', working_hours)
                print('phone:', phone)
                
                b_k = Burgerking(company=company, city=city, address=address, working_hours=working_hours, phone=phone) 
                session.add(b_k) 
                session.commit()

                c_real += 1

            counter += 1

        except:
            counter += 1

def kfc(control):
    
    counter = 0
    c_real = 0

    while (counter - c_real) < control:

        try:    
            url = f'https://www.kfc.ru/restaurants/{counter}'

            r = client.get(url,  headers=headers)

            html = r.text
            soup = BS(html, "html.parser")
            
            c_a = soup.find_all('div', class_="PBUVEowteA t-m-sm mt-16")
            w_h = soup.find_all('div', class_="_3GFeMiI42b t-m-sm mt-8")
            company = soup.find('div', class_="_86RRSm5-kp t-m-xl condensed")
            
            company = str(company).replace('<', '*').replace('>', '*').split('*')[2].split(' ')[0]
            city = str(c_a).replace('<', '*').replace('>', '*').split('*')[8].split(',')[1]
            address = str(c_a).replace('<', '*').replace('>', '*').split('*')[8]
            working_hours = str(w_h[1]).replace('<', '*').replace('>', '*').split('*')[8]
            phone = str(w_h[0]).replace('<', '*').replace('>', '*').split('*')[8]

            print('company:', company)
            print('city:', city)
            print('address:', address)
            print('working_hours:', working_hours)
            print('phone:', phone)
            
            k_f_c = KFC(company=company, city=city, address=address, working_hours=working_hours, phone=phone) 
            session.add(k_f_c) 
            session.commit()
            
            c_real += 1
            
            counter += 1
            
#             print(counter)
            print(c_real)
            
        except:
            counter += 1
            
            
        
def mcdonalds(control):
    
    counter = 0
    c_real = 0

    while (counter - c_real) < control:

        try:    
            url = f'https://mcdonalds.ru/api/restaurant/{counter}'

            r = client.get(url,  headers=headers)
            
#             time.sleep(0.5)

            html = r.json
    
            city = html()['restaurant']['city']
            
            if city == '':
                city = html()['restaurant']['address'].split(',')[0]
            
            try:
                address = html()['restaurant']['address']
            except:
                address = None
                
            try:
                working_hours = html()['restaurant']['lobbyOpeningHours']['monday'][0]['name']
            except:
                working_hours = None
                
            try:
                phone = html()['restaurant']['phone']
            except:
                phone = None
            company = 'Mcdonalds'  
            
            print('city:', city)
            print('address:', address)
            print('working_hours:', working_hours) 
            print('phone:', phone)
            print('company:', company)
            
            md = Mcdonalds(company=company, city=city, address=address, working_hours=working_hours, phone=phone) 
            session.add(md) 
            session.commit()
            
            c_real += 1
            
            counter += 1
            
#             print(counter)
            print(c_real)
            
        except:
            counter += 1
            
burgerking(500)
kfc(700)
mcdonalds(100)
