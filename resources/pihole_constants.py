#!/usr/bin/python3
# -*- coding: utf-8 -*-

# -----------------------------------------------------------
# pihole_constants
# created 27.09.2021
# Thomas Kaulke, kaulketh@gmail.com
# https://github.com/kaulketh
# -----------------------------------------------------------

TMP = "tmpfile"

HELP = """
Usage and possible commands:
/help - this info
/pi_status - status of pihole
/pi_disable - disable pihole
/pi_enable - enable pihole
/pi_restart - restart dns service
/pi_version - show installed versions of pi-hole, console, FTL
/pi_info - output stats
/uptime - last start time of the RBPi
/pi_update - force update
/pi_list_update - update the list of ad-serving domains
/RESTART - force reboot of RBPi"""

START = """
Bot is ready!
Use /help for additional info."""

WRONG = """
Unknown command.
Please use /help for more information."""

COMMANDS = {
    "/RESTART": "sudo reboot",
    "/pi_list_update": "pihole -g",
    "/pi_info": "pihole -c -e",
    "/pi_version": "pihole version",
    "/pi_status": "pihole status",
    "/pi_update": "pihole -up",
    "/pi_restart": "pihole restartdns",
    "/pi_enable": "pihole enable",
    "/pi_disable": "pihole disable",
    "/uptime": "uptime"
}

RESTART_DNS = """
[✓] Restarted DNS server"""
