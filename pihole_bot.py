#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------
# pihole_bot
# created 26.09.2021
# Thomas Kaulke, kaulketh@gmail.com
# https://github.com/kaulketh
# -----------------------------------------------------------

# implemented as service to run at boot
# pihole_bot.service

from resources import bot

if __name__ == '__main__':
    bot.main()
