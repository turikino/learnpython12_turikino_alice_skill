# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals


import os
import json
import argparse

def create_parser():
    parser = argparse.ArgumentParser(description='Переводит стихотворение в list по строчкам.')
    parser.add_argument('-f','--file', help='Файл с текстом')
    parser.add_argument('-id', '--id', help='Номер стихотворения')
    return parser

def text2list(filename, id):
    with open(filename, mode='r') as f:
        name = os.path.basename(filename).split('.')[0]
        work_list = [line.strip('\n') for line in f.readlines() if line != '\n']
        author = work_list[:1]
        text = work_list[1:]
        poem = {
            "poem_id": "poem_{}".format(id),
            "author": author,
            "name": name,
            "text": text
        }
    return poem


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    filename = args.file
    id = args.id
    print(text2list(filename, id))
