# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

from branch_poems import poems
from suggests import get_suggests

# Хранилище данных о сессиях.
sessionStorage = {}


# Функция для непосредственной обработки диалога.
def dialog_handler(req, res):
    """
    :param req: request from user (json)
    :param res: response from Alice (json)
    :return:
    """
    user_id = req['session']['user_id']

    if req['session']['new']:
        # Это новый пользователь.
        res['response']['text'] = 'Здравствуйте! Я помогаю запоминать текст. Что бы вы хотели выучить наизусть?'
        res['response']['buttons'] = get_suggests(user_id)
        return

    # Ветка поэзия.
    if req['request']['original_utterance'].lower() in [
        "стихи",
        "поэма"
    ]:
        res['response']['text'] = 'Выберите как искать текст: по названию или по автору?'
        buttons = [
            "По названию",
            "По автору"
        ]
        res['session']['branch'] = 'poems'
        res['response']['buttons'] = get_suggests(user_id, buttons)
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
        res['response']['buttons'] = get_suggests(user_id, buttons)
        return

    # Перехват функции поэзия.
    if res['session']['branch'] == 'poems':
        poems(req, res)
        return

    # Перехват функции математики.
    if res['session']['branch'] == 'math':
        math(req, res)
        return

    # Перехват функции русский язык.
    if res['session']['branch'] == 'language':
        language(req, res)
        return

    # Если не можем найти в нашей базе, то пробуем создать новый запрос
    res['response']['text'] = 'Не могу найти {}. Давайте попробуем выучить что-нибудь другое?'.format(
        req['request']['original_utterance']
    )
    res['response']['buttons'] = get_suggests(user_id)
