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

PiHole control
/pi_status - status of pihole
/pi_disable - disable pihole
/pi_enable - enable pihole
/pi_restart - restart dns service
/pi_version - show installed versions of pi-hole, console, FTL
/pi_info - output stats
/uptime - last start time of the RBPi
/pi_update - force update
/pi_list_update - update the list of ad-serving domains

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

PI_HOLE_COMMANDS = {
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
RESTART_ROUTER = """
[✓] Restarted router"""
RESTART_REPS = """
[✓] Restarted repeaters"""
RESTART_ALL = """
[✓] Restarting all network devices..."""
LED_ENABLED = """
[✓] Enabled power LED"""
LED_DISABLED = """
[i] Disabled power LED"""

# duration constants in seconds
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
