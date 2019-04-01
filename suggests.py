# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Инициализируем сессию и поприветствуем его.
buttons_def = [
        "Стихи",
        "Правило русского языка",
        "Теорему"
    ]

# Функция возвращает подсказки для ответа.
def get_suggests(user_id, buttons=buttons_def):
    # session = sessionStorage[user_id]

    # Выбираем подсказки из массива.
    suggests = [
        {'title': button, 'hide': True}
        for button in buttons
    ]

    # Если осталась только одна подсказка, предлагаем подсказку
    # со ссылкой на Яндекс.
    if len(suggests) < 2:
        suggests.append({
            "title": "Поищем на Яндексе?",
            "url": "https://yandex.ru/search?text={}".format(req['request']['original_utterance']),
            "hide": True
        })

    return suggests