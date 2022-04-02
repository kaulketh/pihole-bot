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

from resources.constants import HELP, LED_DISABLED, LED_ENABLED, PRIVATE, \
    RESTART_ALL, RESTART_REPS, RESTART_ROUTER, START, \
    TELEGRAM_COMMANDS, WRONG, RESTART_DNS
from resources.led import pwr_led_off, pwr_led_on
from resources.reboot import reboot_box, reboot_repeaters, restart_all
from resources.secret import LIST_OF_ADMINS, TOKEN


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
        self.__send(_execute_os_cmd(TELEGRAM_COMMANDS.get("/status")))
        pwr_led_off()
        self.__send(LED_DISABLED)

        while True:
            try:
                signal.pause()
            except KeyboardInterrupt:
                msg = "Program interrupted"
                sys.stderr.write(f"\n{msg}\n")
                self.__send(msg)
                exit()
            except Exception as e:
                msg = "Any error or exception occurred!"
                self.__send(msg)
                sys.stderr.write(f"{msg}\n")
                sys.stderr.write(f"{e}\n")
                exit()

    def __handle(self, msg):
        chat_id = msg['chat']['id']
        command = msg['text']
        name = f"{msg['chat']['first_name']}' '{msg['chat']['last_name']}"
        alias = msg['chat']['username']

        if chat_id == self.__admin:
            sys.stdout.write(f"Got '{command}' from {name}.\n")
            # start
            if command == "/start":
                self.__send(START)
            # help
            elif command == "/help":
                self.__send(HELP)
            # restart dns (to avoid "Bad Request: message text is empty...")
            elif command == "/restart_dns":
                _execute_os_cmd(TELEGRAM_COMMANDS.get("/restart_dns"))
                self.__send(RESTART_DNS)
            # info (chronometer shorten)
            elif command == "/info":
                m = _execute_os_cmd(TELEGRAM_COMMANDS.get(command))
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
            elif any(c for c in TELEGRAM_COMMANDS if (command == c)):
                self.__send(_execute_os_cmd(TELEGRAM_COMMANDS.get(command)))
            # wrong command
            else:
                self.__send(WRONG)
        else:
            sys.stdout.write(f"Got command from {name}, "
                             f"has wrong ID:{chat_id}!\n")
            self.__send(PRIVATE.format(name, alias, chat_id))


def run():
    Bot(TOKEN, LIST_OF_ADMINS[0]).start()


if __name__ == '__main__':
    pass
