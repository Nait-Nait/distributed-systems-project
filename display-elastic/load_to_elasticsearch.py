import csv
import requests
import time

ELASTIC_URL = "http://elasticsearch:9200"

for i in range(60):
    try:
        r = requests.get(ELASTIC_URL)
        if r.status_code == 200:
            print("Elasticsearch está disponible.")
            break
    except requests.exceptions.ConnectionError:
        print("Esperando a que Elasticsearch esté disponible...")
        time.sleep(1)
else:
    print("Elasticsearch no respondió a tiempo.")
    exit(1)

reportes = [
    {
        "csv_path": "/data/reporte_tipos.csv/part-r-00000",
        "index": "reporte_tipos",
        "field_name": "tipo",
    },
    {
        "csv_path": "/data/reporte_calles.csv/part-r-00000",
        "index": "reporte_calles",
        "field_name": "calle",
    },
    {
        "csv_path": "/data/reporte_fechas.csv/part-r-00000",
        "index": "reporte_fechas",
        "field_name": "fecha",
    },
    {
        "csv_path": "/data/reporte_city.csv/part-r-00000",
        "index": "reporte_city",
        "field_name": "city",
    },
    {
        "csv_path": "/data/reporte_subtipos.csv/part-r-00000",
        "index": "reporte_subtipos",
        "field_name": "subtipo",
    },
]

for reporte in reportes:
    index = reporte["index"]
    path = reporte["csv_path"]
    campo = reporte["field_name"]

    print(f"Cargando {path} en índice '{index}'...")

    requests.delete(f"{ELASTIC_URL}/{index}")
    requests.put(
        f"{ELASTIC_URL}/{index}",
        json={
            "mappings": {
                "properties": {
                    campo: {"type": "keyword"},
                    "cantidad": {"type": "integer"},
                }
            }
        },
    )

    with open(path, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) != 2:
                continue
            doc = {campo: row[0], "cantidad": int(row[1])}
            res = requests.post(f"{ELASTIC_URL}/{index}/_doc", json=doc)
            if res.status_code not in [200, 201]:
                print(f"Error al subir: {res.text}")

    print(f"Reporte '{index}' cargado correctamente.")
