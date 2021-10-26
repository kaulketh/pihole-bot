#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------
# pihole_bot
# created 26.09.2021
# Thomas Kaulke, kaulketh@gmail.com
# https://github.com/kaulketh
# -----------------------------------------------------------

import os
import signal
import sys

import telepot
from telepot.exception import TelegramError
from telepot.loop import MessageLoop

from resources \
    import PI_HOLE_COMMANDS, HELP, WRONG, START, TMP, LIST_OF_ADMINS, TOKEN, \
    RESTART_DNS, RESTART_REPS, RESTART_ROUTER, RESTART_ALL, \
    reboot_box, reboot_repeaters, restart_all, LED_ENABLED, LED_DISABLED, \
    pwr_led_on, pwr_led_off

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
    except TelegramError as te:
        error = f"{type(te)}\n{te.error_code}\n{te}\n"
        sys.stderr.write(error)
        bot.sendMessage(chat_id, error)


def _handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    name = msg['chat']['first_name'] + ' ' + msg['chat']['last_name']
    alias = msg['chat']['username']

    if chat_id == ADMIN:
        sys.stdout.write(f"Got '{command}' from {name}.\n")
        # start
        if command == "/start":
            _send_msg(START)
        # help
        elif command == "/help":
            _send_msg(HELP)
        # restart dns
        elif command == "/pi_restart":
            _execute_os_cmd(PI_HOLE_COMMANDS.get("/pi_restart"))
            _send_msg(RESTART_DNS)
        # control
        elif command == "/router_restart":
            reboot_box()
            _send_msg(RESTART_ROUTER)
        elif command == "/repeaters_restart":
            reboot_repeaters()
            _send_msg(RESTART_REPS)
        elif command == "/restart_all":
            _send_msg(RESTART_ALL)
            restart_all()
        elif command == "/enable_pwr_LED":
            pwr_led_on()
            _send_msg(LED_ENABLED)
        elif command == "/disable_pwr_LED":
            pwr_led_off()
            _send_msg(LED_DISABLED)
        # any other commands
        elif any(c for c in PI_HOLE_COMMANDS if (command == c)):
            _send_msg(_execute_os_cmd(PI_HOLE_COMMANDS.get(command)))
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
    BOT.sendPhoto(ADMIN, open("/home/pi/bot/resources/pihole.png", "rb"))
    _send_msg(START)
    _send_msg(_execute_os_cmd(PI_HOLE_COMMANDS.get("/pi_status")))

    while True:
        try:
            signal.pause()
        except KeyboardInterrupt:
            sys.stderr.write("\nProgram interrupted\n")
            exit()
        except Exception as e:
            sys.stderr.write("Other error or exception occurred!\n")
            sys.stderr.write(f"{e}\n")
