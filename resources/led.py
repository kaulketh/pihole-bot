#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------
# led.py
# created 25.10.2021
# Thomas Kaulke, kaulketh@gmail.com
# https://github.com/kaulketh
# -----------------------------------------------------------
import os


def pwr_led_on():
    """
    Turn on power LED of Raspberry Pi
    :return:
    """
    on = """
    # exec >> /dev/null
    sudo su <<ROOT
    echo default-on > /sys/class/leds/led1/trigger
    ROOT
    """
    os.system(on)


def pwr_led_off():
    """
    Turn off power LED of Raspberry Pi
    :return:
    """
    off = """
    # exec >> /dev/null
    sudo su <<ROOT
    echo none > /sys/class/leds/led1/trigger
    ROOT
    """
    os.system(off)


if __name__ == '__main__':
    pass
