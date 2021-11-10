import os
import json

from app.settings import EVENTS_TABLE_PATTERN, EVENTS_CHANNEL_PATTERN, MONGO_HOST, MONGO_PORT, REDIS_HOST, REDIS_PORT

from flask import Flask, request
from pymongo import MongoClient
import redis


app = Flask(__name__)
# TOOD: Use consts from settings from environment variabless
db = MongoClient(host=MONGO_HOST, port=MONGO_PORT).mongodb
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
supported_services = {
  "github": "X-Github-Event",
}


def _store_and_publish(service_name: str, event: dict) -> None:
  # Store
  events_table = db[EVENTS_TABLE_PATTERN.format(service_name=service_name)]

  # Need to copy the event, because it's being modified inside the function
  events_table.insert_one(event.copy())

  # Publish
  redis_client.publish(channel=EVENTS_CHANNEL_PATTERN.format(service_name=service_name), message=json.dumps(event))


@app.route('/<service_name>', methods=['POST']) 
def webhook_listner(service_name):
  if service_name not in supported_services:
    return "Not found", 404
  
  # Get event type from http headers
  event_type = request.headers[supported_services[service_name]]
  
  request.json["event_type"] = event_type

  _store_and_publish(
    service_name=service_name,
    event=request.json,
  )
  
  return "OK"



if __name__ == '__main__':
  app.run(debug=True, port=3000)