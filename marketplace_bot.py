import requests
from bs4 import BeautifulSoup
import time

# Tu bot de Telegram
TOKEN = "8201323882:AAHM3f4p8esBCXUrGI11rvaUgZ674r2lGzA"
CHAT_ID = "7713445488"

# Tus palabras clave
keywords = ["MacBook", "iPad", "PlayStation 5", "Camara Canon", "Camara Nikon",
            "Xbox", "PC gamer", "Portátil", "Portátil gamer", "Laptop gamer", "Lapto"]

# Guardar publicaciones ya enviadas
enviadas = set()

def enviar_telegram(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": texto})

def buscar_marketplace():
    for palabra in keywords:
        url_busqueda = f"https://www.facebook.com/marketplace/mexico/search/?query={palabra}"
        res = requests.get(url_busqueda, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(res.text, "html.parser")
        links = soup.find_all("a", href=True)
        for link in links:
            if "/marketplace/item/" in link["href"]:
                url_completa = "https://www.facebook.com" + link["href"]
                if url_completa not in enviadas:
                    enviadas.add(url_completa)
                    enviar_telegram(f"📢 Nueva publicación encontrada ({palabra}): {url_completa}")

def mensaje_prueba():
    enviar_telegram("✅ ¡Bot funcionando correctamente! Este es un mensaje de prueba.")

# Llamada de prueba inmediata
mensaje_prueba()

# Loop cada 5 minutos
while True:
    buscar_marketplace()
    time.sleep(300)
