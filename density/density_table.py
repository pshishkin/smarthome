__author__ = 'shish'

import requests, json, re, numpy, time, sys

from data_points_x5 import *
from html.parser import HTMLParser
from math import atan2, pi

h = HTMLParser()

degree_len_vert = 111.3
degree_len_horiz = 63.8

moscow_x = 37.629888
moscow_y = 55.738465


def km_by_degrees(x1, y1, x2, y2):
    return (((x1 - x2) * degree_len_horiz) ** 2 + ((y1-y2) * degree_len_vert) ** 2) ** 0.5


def get_radians_by_delta(dx, dy):
    return atan2(dy * degree_len_vert, dx * degree_len_horiz)


def get_sector_by(dx, dy):
    degrees = get_radians_by_delta(dx, dy) / pi * 180.
    degrees = (degrees + 180 + 22.5)
    if degrees >= 360:
        degrees -= 360
    assert 0 <= degrees <= 360
    return [u'З', u'ЮЗ', u'Ю', u'ЮВ', u'В', u'СВ', u'С', u'СЗ'][int(degrees / 360 * 8)]


def check_area(x, y, distance_delta=0.25):
    dx = distance_delta / degree_len_horiz
    dy = distance_delta / degree_len_vert
    while True:
        r = requests.get('http://api.wikimapia.org/?key=D41FD90C-6FA25B91-98DA8E66-71B18354-C95DEA1F-F3058086-4722869E-EC293839&function=place.getbyarea&coordsby=bbox&bbox={}%2C{}%2C{}%2C{}&format=json&category=44865&data_blocks=main&page=1&count=100'.format(x-dx, y-dy, x+dx, y+dy))
        data = json.loads(r.content.decode('utf8'))
        if 'debug' in data and data['debug'].get('code', 0) == 1004:
            time.sleep(60)
        else:
            break

    # print(data)
    # print(json.dumps(data, indent=4))
    build_dates = []

    for d in data.get('places', []):
        local_dates = []
        for found_date in re.finditer(r' (\d\d\d\d)($|[^\d])', d.get('description', '')):
            local_dates.append(int(found_date.group(1)))
        local_dates = [l for l in local_dates if 2020 > l > 1900]
        if local_dates:
            build_dates.append(min(local_dates))
        # print(d.get('description', ''))
        # print('---------------------')
    if distance_delta == 0.25 and len(build_dates) < 2:
        return check_area(x, y, 1.0)
    return {'build_dates': build_dates}

# print(pyaterochkas[1][1], pyaterochkas[1][2])
# print('hi')

# print(len(pyaterochkas))

for store in perekrestok + pyaterochka + azbuka + ya_lubimiy + bahetle + viktoriya + karusel + kontinent + magnoliya + vkusvill + nash + aliye_parusa:
    km_from_center = km_by_degrees(moscow_x, moscow_y, store[2], store[1])
    sector = get_sector_by(store[2] - moscow_x, store[1] - moscow_y)
    if km_from_center < 30:
        ans = check_area(store[2], store[1])
        print('\t'.join([str(store[0]), str(int(numpy.average(ans['build_dates']) if ans['build_dates'] else 0)), str(len(ans['build_dates'])), h.unescape(store[4]), str(int(km_from_center)), str(sector), h.unescape(store[6]).replace(r'\"', r'"')]))
        sys.stdout.flush()
