#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re

text1 = "This game is one of the very best. games ive  played. the  ;pictures? " \
        "cant describe the real graphics in the game."
def compute_cosine(text_a):
    words = text_a.split(' ')
    #words_dict = {}
    for word in words:
        word = re.sub('[^a-zA-Z]', '', word)
        if word != '':
            print(word)


if __name__ == '__main__':
    compute_cosine(text1)