# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

from suggests import get_suggests

# Функция работает с базой стихов
def poems(req, res):
    user_id = req['session']['user_id']
    if req['request']['original_utterance'].lower() in [
        "по",
        "автору"
    ]:
        res['response']['text'] = 'Назовите автора:'
        res['session']['branch'] = 'author'
        return

    if req['request']['original_utterance'].lower() in [
        "по",
        "названию"
    ]:
        res['response']['text'] = 'Назовите стихотворение:'
        res['session']['branch'] = 'name'
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
