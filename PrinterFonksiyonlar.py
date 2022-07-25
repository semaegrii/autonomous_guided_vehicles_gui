from PIL import Image, ImageDraw, ImageFont
import time
import os
import codecs
from datetime import datetime



def load_dict_from_file8bit(file):
    f = open(file, 'r')
    data = f.read()
    f.close()
    return eval(data)


def load_dict_from_file16bit(file):
    f = codecs.open(file, "r", "utf-16")
    data = f.read()
    f.close()
    return eval(data)


def save_dict_to_file(dic, file):
    f = open(file, 'w')
    f.write(str(dic))
    f.close()


def seperate_content(contents):
    try:
        result1 = []
        result2 = []
        for content in contents:
            sayi = int(content[0])
            if sayi % 2 == 0:
                result2.append(content)
            else:
                result1.append(content)

        return result1, result2
    except Exception as e:
        print(e)

