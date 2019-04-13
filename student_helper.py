# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

import string
# Импортируем модули для работы с JSON и логами.
import json
import logging

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request, render_template
from flask_pymongo import PyMongo

# Импортируем функции из handlers.py
from handlers import dialog_handler

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/student_helper"
mongo = PyMongo(app)


logging.basicConfig(level=logging.DEBUG)


@app.route('/add-new-poem', methods=['POST', 'GET'])
def new_poem():
    if request.method == 'POST':
        author = request.form.get('author')
        name = request.form.get('name')
        lines = [line for line in request.form.get('user_text').split('\n') if line != '\n']
        text = []
        for ln in lines:
            words = [word.lower().strip(string.punctuation).strip("«»?!,.-—:;.,;()_+") for word in ln.split() if word != '']
            text.append(words)
        poem = {
            "author": author,
            "name": name,
            "text": text
        }
        poem_id = mongo.db.poems.insert_one(poem).inserted_id
        logging.info(text)
    return render_template("add-new-poem.html")


@app.route('/', methods=['POST'])
def main():
    # Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    dialog_handler(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )


if __name__ == '__main__':
    app.run(debug=True, port=5000)
