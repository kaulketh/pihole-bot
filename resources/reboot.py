#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------
# reboot
# created 24.10.2021
# Thomas Kaulke, kaulketh@gmail.com
# https://github.com/kaulketh
# -----------------------------------------------------------

import os
import sys
import time
import traceback
from datetime import timedelta
from subprocess import call

from .constants import MINUTE
from .secret import BOX_IP, BOX_USER_PW, \
    REP_IP_1, REP_PW, REP_IP_2, BOX_USER


class RebootFritzDevice:
    def __init__(self, ip4, password, user=None):
        self.__ip4 = ip4
        self.__usr = "" if user is None else user
        self.__pwd = password

        self.__return_value = None

        # noinspection SpellCheckingInspection,HttpUrlsUsage
        self.__curl = f"curl -k -m 5 --anyauth " \
                      f"-u \"{self.__usr}:{self.__pwd}\" " \
                      f"http://{self.__ip4}:49000/upnp/control/deviceconfig " \
                      f"-H 'Content-Type: text/xml; charset=\"utf-8\"' " \
                      f"-H \"SoapAction:" \
                      f"urn:dslforum-org:service:DeviceConfig:1#Reboot\" " \
                      f"-d \"<?xml version='1.0' encoding='utf-8'?>" \
                      f"<s:Envelope s:encodingStyle=" \
                      f"'http://schemas.xmlsoap.org/soap/encoding/' " \
                      f"xmlns:s='http://schemas.xmlsoap.org/soap/envelope/'>" \
                      f"<s:Body><u:Reboot xmlns:" \
                      f"u='urn:dslforum-org:service:DeviceConfig:1'>" \
                      f"</u:Reboot></s:Body></s:Envelope>\" " \
                      f"-s > /dev/null"

        # noinspection PyBroadException
        # TODO: Exception handling properly
        try:
            self.__return_value = call(self.__curl, shell=True)
        except Exception as e:
            # traceback.print_exc()
            sys.stderr.write(f"Problem while executing cURL request: {e}\n")


def repeat(func, *args,
           weeks=0,
           days=0,
           hours=0,
           minutes=0,
           seconds=0,
           milliseconds=0,
           microseconds=0
           ):
    """
    origin: https://stackoverflow.com/questions/474528/what-is-the-best-way-to-repeatedly-execute-a-function-every-x-seconds/25251804#25251804
    """

    interval = timedelta(weeks=weeks, days=days, hours=hours,
                         minutes=minutes,
                         seconds=seconds,
                         milliseconds=milliseconds,
                         microseconds=microseconds).total_seconds()
    next_time = time.time() + interval
    while True:
        sys.stdout.write(f"(Re)run {func} "
                         f"in {interval} seconds.\n")
        time.sleep(max(0.0, next_time - time.time()))
        # noinspection PyBroadException
        # TODO: Exception handling properly
        try:
            func(*args)
        except Exception as e:
            traceback.print_exc()
            sys.stderr.write(
                f"Problem while executing repetitive task: {e}\n")
        if interval != 0:
            # skip tasks if we are behind schedule:
            next_time += (time.time() - next_time) \
                         // interval * interval + interval


def reboot_box():
    RebootFritzDevice(BOX_IP, BOX_USER_PW, BOX_USER)


def reboot_repeaters():
    RebootFritzDevice(REP_IP_1, REP_PW)
    RebootFritzDevice(REP_IP_2, REP_PW)


def reboot_host():
    os.system("sudo reboot")


def restart_all(myself_too=True,
                after_router=5 * MINUTE,
                after_other_devices=3 * MINUTE):
    reboot_box()
    time.sleep(after_router)
    reboot_repeaters()
    if myself_too:
        time.sleep(after_other_devices)
        reboot_host()


if __name__ == '__main__':
    # implement call as service or cronjob or what ever
    repeat(restart_all, weeks=0, days=1, hours=0, minutes=0, seconds=0)
