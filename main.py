import os
import requests
import xml.etree.ElementTree as ET

def fetch_security_data(url):
    response = requests.get(url)
    return response.text

def fetch_and_save_images(xml_str, save_folder):
    # Убедимся, что папка для сохранения существует
    os.makedirs(save_folder, exist_ok=True)
    
    # Парсим XML данные
    root = ET.fromstring(xml_str)
    
    # Проходим по всем элементам с тегом 'row' и извлекаем SECID
    for row in root.iter('row'):
        secid = row.attrib.get('SECID')
        if secid:
            # Формируем URL картинки
            image_url = f"https://storage.yandexcloud.net/snowball-data/asset-logos/{secid}-MCX-RUB-custom.png"
            
            # Загружаем картинку
            image_response = requests.get(image_url)

            if image_response.status_code == 200:
                # Сохраняем картинку
                image_path = os.path.join(save_folder, f"{secid}.png")
                with open(image_path, 'wb') as file:
                    file.write(image_response.content)
                print(f"Downloaded and saved: {image_path}")
            else:
                print(f"Failed to download image for SECID: {secid}")

# Определяем источники как и раньше
sources = [
    ("SHARES/boards/TQBR", "акции"),
    ("SHARES/boards/TQTF", "ETF"),
    ("BONDS/boards/TQOB", "ОФЗ"),
    ("BONDS/boards/TQCB", "корпоративных облигации")
]

# Папка для сохранения изображений
save_folder = "images"

# Загружаем и обрабатываем данные
for url, key in sources:
    xml_data = fetch_security_data(
        f"https://iss.moex.com/iss/engines/stock/markets/{url}/securities.xml?iss.meta=off&iss.only=securities&securities.columns=SECID,PREVPRICE"
    )
    fetch_and_save_images(xml_data, save_folder)