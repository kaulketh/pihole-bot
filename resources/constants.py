#!/usr/bin/python3
# -*- coding: utf-8 -*-

# -----------------------------------------------------------
# pihole_constants
# created 27.09.2021
# Thomas Kaulke, kaulketh@gmail.com
# https://github.com/kaulketh
# -----------------------------------------------------------

# message texts
HELP = """
Usage and possible commands:
/help - this info

PiHole control
/status - status of pihole
/disable - disable pihole
/enable - enable pihole
/restart_dns - restart dns service
/version - show installed versions of pi-hole, console, FTL
/info - output stats
/uptime - last start time of the RBPi
/update - force update
/list_update - update the list of ad-serving domains

/enable_pwr_LED - turn LED on
/disable_pwr_LED - turn LED off
/RESTART - force reboot of PiHole

Network control
/router_restart - force reboot of router
/repeaters_restart - force reboot of all repeaters
/restart_all - force reboot of all network devices"""

START = """
Bot is ready!
Use /help for additional info."""

WRONG = """
Unknown command.
Please use /help for more information."""

PRIVATE = "Hello {}, alias {}, this is a private bot.\n" \
          "Your Chat ID \'{}\' was blocked!"

RESTART_DNS = """
[✓] Restarted DNS server"""
RESTART_ROUTER = """
[✓] Router is restarting..."""
RESTART_REPS = """
[✓] Repeaters are restarting..."""
RESTART_ALL = """
[✓] Restarting all network devices..."""
LED_ENABLED = """
[✓] Power LED enabled"""
LED_DISABLED = """
[✗] Power LED disabled"""

# commands
TELEGRAM_COMMANDS = {
    "/RESTART": "sudo reboot",
    "/list_update": "pihole -g",
    "/info": "pihole -c -e",
    "/version": "pihole version",
    "/status": "pihole status",
    "/update": "pihole -up",
    "/restart_dns": "pihole restartdns",
    "/enable": "pihole enable",
    "/disable": "pihole disable",
    "/uptime": "uptime"
}

# durations
SECOND = 1
MINUTE = 60
HOUR = 3_600
DAY = 216_000
WEEK = 1_512_000

# week days
ISO_WEEK_EN = {
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday",
    7: "Sunday"
}

# noinspection SpellCheckingInspection
ISO_WEEK_DE = {
    1: "Montag",
    2: "Dienstag",
    3: "Mittwoch",
    4: "Donnerstag",
    5: "Freitag",
    6: "Samstag",
    7: "Sonntag"
}
