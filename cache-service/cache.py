import os
import json
from pymongo import MongoClient
import redis


def main():
    
    mongo_uri = os.getenv("MONGO_URI", "mongodb://mongo:27017")
    redis_host = os.getenv("REDIS_HOST", "redis")
    redis_port = int(os.getenv("REDIS_PORT", 6379))
    ttl_static = int(os.getenv("STATIC_TTL", 300))

    
    client = MongoClient(mongo_uri)
    db = client["waze_db"]
    coll = db["events_raw"]

    r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

    print(f"Conectado a MongoDB: {mongo_uri}")
    print(f"Conectado a Redis: {redis_host}:{redis_port}")

    static_streets = [
        "Av. Libertador Bernardo O'Higgins",
        "Longitudinal",
        "Av. Independencia",
        "Av. Américo Vespucio",
    ]

    total_guardados = 0

    for street in static_streets:
        events = coll.find({"street": street}).limit(500)
        count = 0
        for event in events:
            event_id = str(event["_id"])
            event["_id"] = event_id
            event_json = json.dumps(event)
            r.set(f"event:{event_id}", event_json)
            if ttl_static > 0:
                r.expire(f"event:{event_id}", ttl_static)
            count += 1
            total_guardados += 1

        print(f"Guardados {count} eventos para calle '{street}'.")

    print(f"\n Total de eventos guardados en Redis: {total_guardados}")


if __name__ == "__main__":
    main()
