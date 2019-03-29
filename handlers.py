# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals


# Хранилище данных о сессиях.
sessionStorage = {}

# Функция для непосредственной обработки диалога.
def dialog_handler(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.
        sessionStorage[user_id] = {
            'suggests': [
                "Стихи",
                "Правило русского языка",
                "Теорему"
            ]
        }

        res['response']['text'] = 'Здравствуйте! Я помогаю запоминать текст. Что бы вы хотели выучить наизусть?'
        res['response']['buttons'] = get_suggests(user_id)
        return

    # Ветка поэзия.
    if req['request']['original_utterance'].lower() in [
        "стихи",
        "поэма"
    ]:
        res['response']['text'] = 'Назовите стихотворение или поэта.'
        res['session']['branch'] = 'poems'
        return

    # Ветка теоремы.
    if req['request']['original_utterance'].lower() in [
        "теорема",
        "закон"
    ]:
       res['response']['text'] = 'Назовите теорему, закон или имя ученого.'
       res['session']['branch'] = 'math'
       return

    # Ветка русский язык.
    if req['request']['original_utterance'].lower() in [
        "правило",
        "русского",
        "языка"
    ]:
        res['response']['text'] = 'Назовите правило русского языка.'
        res['session']['branch'] = 'language'
        return

    # Пустой запрос.
    if req['request']['original_utterance'].lower() == '':
        res['response']['text'] = 'Вы ничего не назвали. Давайте попробуем еще раз?'
        res['response']['buttons'] = get_suggests(user_id)
        return

    # Если не можем найти в нашей базе, то пробуем создать новый запрос
    res['response']['text'] = 'Не могу найти {}. Давайте попробуем выучить что-нибудь другое?'.format(
        req['request']['original_utterance']
    )
    res['response']['buttons'] = get_suggests(user_id)

# Функция работает с базой стихов
def poems(req, res):

    return

# Функция работает с базой теорем и законов
def math(req, res):

    return

# Функция работает с базой правил языка
def language(req, res):

    return


# Функция возвращает две подсказки для ответа.
def get_suggests(user_id):
    session = sessionStorage[user_id]

    # Выбираем подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests']
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