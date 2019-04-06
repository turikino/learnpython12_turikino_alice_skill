# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals
import logging

from branch_poems import poems
from utils import get_suggests, search_poet, get_text

logging.basicConfig(level=logging.DEBUG)

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

    # Пустой запрос.
    if req['request']['original_utterance'].lower() == '':
        res['response']['text'] = 'Вы ничего не назвали. Давайте попробуем еще раз?'
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

    if req['request']['original_utterance'].lower() in [
        "по автору"
    ]:
        res['response']['text'] = 'Назовите автора:'
        res['session']['branch'] = 'poem_author'
        return

    if req['request']['original_utterance'].lower() in [
        "по названию"
    ]:
        res['response']['text'] = 'Назовите стихотворение:'
        res['session']['branch'] = 'poem_name'
        return


    # Вариант поиска стихов по автору.
    if req['session']['branch'] == 'poem_author':
        author = req['request']['original_utterance'].lower()
        poem_name = search_poet(author)
        res['response']['text'] = 'Могу предложить стихотворение: {}'.format(poem_name)
        res['session']['branch'] = 'start'
        res['session']['poem_name'] = poem_name
        return


    # Вариант поиска стихов по названию.
    if req['session']['branch'] == 'poem_name':
        poem_name = req['request']['original_utterance'].lower()
        poem_author = search_poet(poem_name)
        res['response']['text'] = 'Это стихотворение поэта {}?'.format(poem_author)
        res['session']['branch'] = 'start'
        res['session']['poem_name'] = poem_name
        return

    # Запуск работы.
    if req['session']['branch'] == 'start':
        if req['request']['original_utterance'].lower() in [
            "да",
            "правильно",
            "ага"
        ]:
            res['response']['text'] = 'Начинайте!'
            res['session']['branch'] = 'learn'
        return

    # Работа со стихотворением.
    if req['session']['branch'] == 'learn':
        text = get_text(req['session']['poem_name'])
        res['response']['text'] = text
        res['session']['branch'] = 'learn'
        return


    # Если не можем найти в нашей базе, то пробуем создать новый запрос
    res['response']['text'] = 'Не могу найти {}. Давайте попробуем выучить что-нибудь другое?'.format(
        req['request']['original_utterance']
    )
    res['response']['buttons'] = get_suggests(user_id)

    # logging.info('poem_name: %r', req['session']['poem_name'])

