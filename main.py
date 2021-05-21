import requests
from bs4 import BeautifulSoup
import csv

CSV = 'cards.csv' 
HOST = 'https://www.kivano.kg/'
URL = 'https://www.kivano.kg/mobilnye-telefony'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    'user-agent''Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
}

def get_html(url, params=''): #параметры в адресной строке page2, 3
    response = requests.get(url, headers=HEADERS, params=params) # параметры которые мы получаем от params # запрос на страницу
    return response

def get_content(html): # это функция которая будет забирать по указонному url, params html, т.е будет получать глобальный html (будет получать контент)
    soup = BeautifulSoup(html, 'html.parser') # вытягивает определенные данные
    items = soup.find_all('div', class_='item product_listbox oh')
    cards = []
    
  # будет работать с одной страницей, т.е парсить одну строницу
    for item in items:
        cards.append(
            {
                'title':item.find('div', class_='listbox_title oh').find('strong').text,
                'price': item.find('div', class_='listbox_price text-center').find('strong').text,
                'card_img': HOST + item.find('div', class_='listbox_img pull-left').find('img').get('src')
            }
        )

    return cards

def save_doc(items, path): # то, что мы хотим сохрнить. второй параметр - куда мы хотим сохранить
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название продукта', 'Цена', 'Изображение карты'])
        for item in items:
            writer.writerow([item['title'], item['price'], item['card_img']])

# будет парсить всю страницу 
def parser():
    PAGENATION = input('Укажите количество страниц для парсинга: ')
    PAGENATION = int(PAGENATION.strip())
    html=get_html(URL)
    if html.status_code == 200:
        cards = [] # всю страницу собираем сюда в один список
        for page in range(1, PAGENATION): # цикл пройдет от 1 до указывания пользователя
            print(f'Парсим страницу: {page}')
            html = get_html(URL, params = {'page': page})
            cards.extend(get_content(html.text))
            save_doc(cards, CSV)
        pass
    else:
        print('Error')


parser()




    