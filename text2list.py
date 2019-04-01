# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals


import os
import json
import argparse

def create_parser():
    parser = argparse.ArgumentParser(description='Переводит стихотворение в list по строчкам.')
    parser.add_argument('-f','--file', help='Файл с текстом')
    return parser

def text2list(filename):
    with open(filename, mode='r') as f:
        name = os.path.basename(filename).split('.')[0]
        work_list = [line.strip('\n') for line in f.readlines() if line != '\n']
        author = work_list[:1]
        text = work_list[1:]
        poem = {
            "author": author,
            "name": name,
            "text": text
        }
        print(poem)
    return json.dumps(poem, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    filename = args.file
    text2list(filename)
