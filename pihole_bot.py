#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------
# pihole_bot
# created 26.09.2021
# Thomas Kaulke, kaulketh@gmail.com
# https://github.com/kaulketh
# -----------------------------------------------------------

import os
import sys
import time

import telepot
from telepot.exception import TelegramError
from telepot.loop import MessageLoop

from resources \
    import COMMANDS, HELP, WRONG, START, TMP, LIST_OF_ADMINS, TOKEN, \
    RESTART_DNS

BOT = telepot.Bot(TOKEN)
ADMIN = LIST_OF_ADMINS[0]


def _execute_os_cmd(cmd):
    """
    Executes os command and gets response data
    """

    os.system(f"{cmd} > {TMP} 2>&1")
    data = ""
    file = open(f"{TMP}", "r")
    data = file.read()
    file.close()
    if os.path.exists(f"{TMP}"):
        os.remove(f"{TMP}")
    return data


def _send_msg(msg, bot=BOT, chat_id=ADMIN):
    """
    Send message to defined API chat client
    """
    try:
        bot.sendMessage(chat_id, msg)
        sys.stdout.write(f"{msg}\n")
    except TelegramError as e:
        error = f"{type(e)}\n{e.error_code}\n{e}\n"
        sys.stderr.write(error)
        bot.sendMessage(chat_id, error)


def _handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    name = msg['chat']['first_name'] + ' ' + msg['chat']['last_name']
    alias = msg['chat']['username']

    if chat_id in LIST_OF_ADMINS:
        sys.stdout.write(f"Got '{command}' from {name}.\n")
        # start
        if command == "/start":
            _send_msg(START)
        # help
        elif command == "/help":
            _send_msg(HELP)
        # restart dns
        elif command == "/pi_restart":
            _execute_os_cmd(COMMANDS.get("/pi_restart"))
            _send_msg(RESTART_DNS)

        # any other commands
        elif any(c for c in COMMANDS if (command == c)):
            _send_msg(_execute_os_cmd(COMMANDS.get(command)))
        # wrong command
        else:
            _send_msg(WRONG)
    else:
        sys.stdout.write(f"Got command from {name}, has wrong ID:{chat_id}!\n")
        _send_msg(
            f"Hello {name}, alias {alias}, this is a private bot.\n"
            f"Your Chat ID \'{chat_id}\' was blocked!")


if __name__ == '__main__':
    MessageLoop(BOT, _handle).run_as_thread()
    sys.stdout.write("I am listening...\n")
    BOT.sendPhoto(ADMIN, open("resources/pihole.png", "rb"))
    _send_msg(START)
    while True:
        try:
            time.sleep(10)
        except KeyboardInterrupt:
            sys.stderr.write("Program interrupted\n")
            exit()
        except Exception as e:
            sys.stderr.write("Other error or exception occurred!\n")
            sys.stderr.write(f"{e}\n")