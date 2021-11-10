import os

from flask import Flask, request, json

from tinydb import TinyDB, Query


app = Flask(__name__)
db_file_path = os.environ["DB_FILE_PATH"]
db = TinyDB(db_file_path)


@app. route('/github', methods=['POST']) 
def github_webhook_listner():
    db_id = db.insert(request.json)
    print(f"Added document id: {db_id}")
    return "OK"


if __name__ == '__main__':
  app.run(debug=True, port=3000)