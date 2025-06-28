import os
import json
import time
from pymongo import MongoClient
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.options import Options


MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["waze_db"]
collection = db["events_selenium"]


uuids_existentes = set(doc["uuid"] for doc in collection.find({}, {"uuid": 1}))


options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

print("🚦 Abriendo Waze...")
driver.get("https://www.waze.com/es-419/live-map/")
print("🕹️ Puedes mover el mapa. El script capturará georss automáticamente.")

try:
    while True:
        nuevos_requests = [
            req for req in driver.requests if req.response and "/georss?" in req.url
        ]

        for request in nuevos_requests:
            try:
                body = request.response.body.decode("utf-8")
                data = json.loads(body)
                alerts = data.get("alerts", [])

                nuevos = [a for a in alerts if a["uuid"] not in uuids_existentes]

                if nuevos:
                    print(f"🟢 {len(nuevos)} eventos nuevos desde: {request.url}")
                    collection.insert_many(nuevos)
                    uuids_existentes.update(a["uuid"] for a in nuevos)
                else:
                    print(f"🔁 Solo eventos repetidos desde: {request.url}")
            except Exception as e:
                print(f"⚠️ Error procesando {request.url}: {e}")

        driver.requests.clear() 
        time.sleep(2)

except KeyboardInterrupt:
    print("⛔ Captura interrumpida por el usuario.")
finally:
    try:
        driver.quit()
    except Exception as e:
        print(f"⚠️ Error al cerrar navegador: {e}")
