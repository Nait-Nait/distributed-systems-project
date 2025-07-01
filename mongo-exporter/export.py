import csv
from pymongo import MongoClient
from datetime import datetime

MONGO_URI = "mongodb://mongo:27017"
DB_NAME = "waze_db"
COLLECTION_NAME = "events_selenium"
OUTPUT_FILE = "/data/eventos.csv"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]


def millis_to_fecha(millis):
    try:
        dt = datetime.fromtimestamp(millis / 1000)
        return dt.strftime("%Y-%m-%d"), dt.strftime("%H:%M:%S")
    except:
        return "", ""


def flatten(doc):
    fecha, hora = millis_to_fecha(doc.get("pubMillis", 0))
    return {
        "evento_id": doc.get("uuid", doc.get("id", "")),
        "tipo": doc.get("type", "").lower(),
        "subtipo": doc.get("subtype", "").lower(),
        "calle": doc.get("street", "").lower(),
        "city": doc.get("city", "").lower(),
        "lat": doc.get("location", {}).get("y", ""), 
        "lon": doc.get("location", {}).get("x", ""), 
        "timestamp": doc.get("pubMillis", ""),
        "fecha_evento": fecha,
        "hora_evento": hora,
        "fuente": "waze",
        "procesado": "false",
    }


with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = [
        "evento_id",
        "tipo",
        "subtipo",
        "calle",
        "city", 
        "lat",
        "lon",
        "timestamp",
        "fecha_evento",
        "hora_evento",
        "fuente",
        "procesado",
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for doc in collection.find():
        writer.writerow(flatten(doc))

print(f"Exportado correctamente a {OUTPUT_FILE}")
