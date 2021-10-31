#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------
# bot.py
# created 28.10.2021
# Thomas Kaulke, kaulketh@gmail.com
# https://github.com/kaulketh
# -----------------------------------------------------------
import signal
import subprocess
import sys

import telepot
from telepot.exception import TelegramError
from telepot.loop import MessageLoop

from resources.constants import START, PI_HOLE_COMMANDS, HELP, RESTART_DNS, \
    RESTART_ROUTER, RESTART_REPS, RESTART_ALL, LED_ENABLED, LED_DISABLED, WRONG
from resources.leds import pwr_led_off, pwr_led_on
from resources.reboot import restart_all, reboot_repeaters, reboot_box
from resources.secret import TOKEN, LIST_OF_ADMINS


def _execute_os_cmd(cmd):
    sp = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    out = sp.communicate()[0]
    sp.wait()
    return out.decode()


class Bot:
    """ Bot class using telepot framework
        (https://telepot.readthedocs.io),
        Python >= 3
    """

    def __init__(self, token, admin):
        self.__token = token
        self.__admin = admin
        self.__bot = telepot.Bot(self.__token)

    def __send(self, msg):
        """
        Send message to defined API chat client
        """
        try:
            self.__bot.sendMessage(self.__admin, msg)
            sys.stdout.write(f"{msg}\n")
        except TelegramError as te:
            error = f"{type(te)}\n{te.error_code}\n{te}\n"
            sys.stderr.write(error)
            self.__bot.sendMessage(self.__admin, error)

    def start(self):
        MessageLoop(self.__bot, self.__handle).run_as_thread()
        sys.stdout.write("I am listening...\n")
        self.__send(START)
        self.__send(_execute_os_cmd(PI_HOLE_COMMANDS.get("/pi_status")))

        while True:
            try:
                signal.pause()
            except KeyboardInterrupt:
                sys.stderr.write("\nProgram interrupted\n")
                exit()
            except Exception as e:
                sys.stderr.write("Other error or exception occurred!\n")
                sys.stderr.write(f"{e}\n")

    def __handle(self, msg):
        chat_id = msg['chat']['id']
        command = msg['text']
        name = msg['chat']['first_name'] + ' ' + msg['chat']['last_name']
        alias = msg['chat']['username']

        if chat_id == self.__admin:
            sys.stdout.write(f"Got '{command}' from {name}.\n")
            # start
            if command == "/start":
                self.__send(START)
            # help
            elif command == "/help":
                self.__send(HELP)
            # restart dns
            elif command == "/pi_restart":
                _execute_os_cmd(PI_HOLE_COMMANDS.get("/pi_restart"))
                self.__send(RESTART_DNS)
            # info (chronometer)
            elif command == "/pi_info":
                m = _execute_os_cmd(PI_HOLE_COMMANDS.get(command))
                i = m.rfind("Hostname")
                self.__send(m[i:])
            # control
            elif command == "/router_restart":
                reboot_box()
                self.__send(RESTART_ROUTER)
            elif command == "/repeaters_restart":
                reboot_repeaters()
                self.__send(RESTART_REPS)
            elif command == "/restart_all":
                self.__send(RESTART_ALL)
                restart_all()
            elif command == "/enable_pwr_LED":
                pwr_led_on()
                self.__send(LED_ENABLED)
            elif command == "/disable_pwr_LED":
                pwr_led_off()
                self.__send(LED_DISABLED)
            # any other commands
            elif any(c for c in PI_HOLE_COMMANDS if (command == c)):
                self.__send(_execute_os_cmd(PI_HOLE_COMMANDS.get(command)))
            # wrong command
            else:
                self.__send(WRONG)
        else:
            sys.stdout.write(f"Got command from {name}, "
                             f"has wrong ID:{chat_id}!\n")
            self.__send(
                f"Hello {name}, alias {alias}, this is a private bot.\n"
                f"Your Chat ID \'{chat_id}\' was blocked!")


def run():
    Bot(TOKEN, LIST_OF_ADMINS[0]).start()


if __name__ == '__main__':
    pass
