#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------
# pihole_bot
# created 26.09.2021
# Thomas Kaulke, kaulketh@gmail.com
# https://github.com/kaulketh
# -----------------------------------------------------------

import os
import time

import telepot

from secret import LIST_OF_ADMINS, TOKEN


def _read_cmd(cmd):
    """
    Assign default output (stdout 1 and stderr 2) to file and read in
    variable and get back
    """

    os.system(cmd + ' > tmplog 2>&1')
    data = ""
    file = open('tmplog', 'r')
    data = file.read()
    file.close()
    if os.path.exists('tmplog'):
        os.remove('tmplog')
    return data


def _send_msg(msg):
    """
    Send message to defined API chat client
    """

    os.system(
        f"curl -s -k https://api.telegram.org/bot{TOKEN}/"
        f"sendMessage -d text={msg} -d chat_id={LIST_OF_ADMINS[0]}")
    return


def _handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    name = msg['chat']['first_name'] + ' ' + msg['chat']['last_name']
    alias = msg['chat']['username']

    if chat_id in LIST_OF_ADMINS:
        print('Got command from {} : {}'.format(name, command))

        # commands
        if command == "/RESTART":
            _send_msg(_read_cmd("sudo reboot"))
        elif command == "/pi_list_update":
            _send_msg(_read_cmd("pihole -g"))
        elif command == "/pi_info":
            _send_msg(_read_cmd("pihole -c -e"))
        elif command == "/pi_version":
            _send_msg(_read_cmd("pihole version"))
        elif command == "/pi_status":
            _send_msg(_read_cmd("pihole status"))
        elif command == "/pi_update":
            _send_msg(_read_cmd("pihole -up"))
        elif command == "/pi_restart":
            _send_msg(_read_cmd("pihole restartdns"))
        elif command == "/pi_enable":
            _send_msg(_read_cmd("pihole enable"))
            time.sleep(1)
            _send_msg(_read_cmd("pihole status"))
        elif command == "/pi_disable":
            _send_msg(_read_cmd("pihole disable"))
        elif command == "/uptime":
            _send_msg(_read_cmd("uptime"))
        elif command == "/start":
            _send_msg("Bot is ready!\nUse /help for additional info.")
        elif command == "/help":
            _send_msg(
                f"Usage and possible commands:\n"
                f"/help - this info\n"
                f"/pi_info - output stats\n"
                f"/pi_version "
                f"- show installed versions of pi-hole, console, FTL\n"
                f"/uptime - last start time of the RBPi\n"
                f"/pi_status - status of pihole\n"
                f"/pi_update - force update\n"
                f"/pi_list_update - update the list of ad-serving domains\n"
                f"/pi_restart - restart dns service\n"
                f"/pi_disable - disable pihole\n"
                f"/pi_enable - enable pihole\n"
                f"/RESTART - force reboot of RBPi")
        else:
            _send_msg(
                f"Unknown command...!\n"
                f"Please use /help for more information.")
    else:
        print(f"Got command from {name}, has wrong ID:{chat_id}!")
        _send_msg(
            f"Hello {name}, alias {alias}, this is a private bot.\n"
            f"Your Chat ID \'{chat_id}\' was blocked!")


bot = telepot.Bot(TOKEN)
bot.message_loop(_handle)
print('I am listening...')

while True:
    try:
        time.sleep(10)
    except KeyboardInterrupt:
        print('\n Program interrupted')
        exit()

    except:
        print('Other error or exception occurred!')
