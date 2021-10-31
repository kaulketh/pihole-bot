#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------
# fritz
# created 30.10.2021
# Thomas Kaulke, kaulketh@gmail.com
# https://github.com/kaulketh
# -----------------------------------------------------------

# implemented as service to run at boot
# fritz_restart.service

from resources import reboot

if __name__ == '__main__':
    reboot.schedule_as_cronjob()
