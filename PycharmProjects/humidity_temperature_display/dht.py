#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------
# dht.py
# created 30.04.2021
# Thomas Kaulke, kaulketh@gmail.com
# https://github.com/kaulketh
# -----------------------------------------------------------
# from sys import stdout, stderr

import Adafruit_DHT

sensor = Adafruit_DHT.DHT22
pin = 24
temp_format = '{:04.1f}°C'
hum_format = '{:05.2f}%'
space = " "


def get_values():
    temp_str = space
    hum_str = space
    ret_str = space
    # stdout.write('Get temperature and humidity values.')
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    if humidity is not None and temperature is not None:
        temp_str = str(temperature).format(temp_format)
        hum_str = str(humidity).format(hum_format)
        ret_str = f"({temp_str}{space}{hum_str}"
        # stdout.write(ret_str)
    else:
        # stderr.write(
        #    'Failed to get temperature and humidity values. Set to \'0\'!')
        humidity = 0
        temperature = 0
    return hum_str, temp_str, ret_str, humidity, temperature


if __name__ == '__main__':
    pass
