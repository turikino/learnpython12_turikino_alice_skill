# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request

# Импортируем функции из handlers.py
from handlers import greet_user, poems, math, language

app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)



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

    greet_user(request.json, response)

    poems(request.json, response)

    math(request.json, response)

    language(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)