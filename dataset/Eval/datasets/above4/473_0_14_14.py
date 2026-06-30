# -*- coding: utf-8 -*-
# is instruction English
def is_english_simple(text):
    try:
        text.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
# def bbox_2_point(bbox, dig=2):
        return True





    point = [(bbox[0]+bbox[2])/2, (bbox[1]+bbox[3])/2]
    point = [round(x,4) for x in point]
    return point