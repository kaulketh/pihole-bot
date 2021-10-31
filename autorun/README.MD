# Autorun at boot up as _systemd_ service

A possibility to enable run at boot up is to use the _systemd_ files. _systemd_ provides a standard process for controlling what programs run when a Linux system boots up.<br>
Note that _systemd_ is available only from the Jessie versions of Raspbian OS.

### Use service files included or create unit file

`sudo nano /lib/systemd/system/<service name>.service`

```ini
[Unit]
Description = <short description of service>
After = multi-user.target

[Service]
Type = idle
Restart=on-failure
RestartSec=5s
ExecStart = /usr/bin/python3 <path to/of Python script>

[Install]
WantedBy = multi-user.target
```

`sudo chmod 644 /lib/systemd/system/<service name>.service`

### Configure systemd

`sudo systemctl daemon-reload`

`sudo systemctl enable <service name>.service`

`sudo reboot` OR `sudo systemctl start <service name>.service`

### Starting, stopping, and querying systemd services
- Reload service daemon: `sudo systemctl daemon-reload`
- Enable a service to be started on boot: `sudo systemctl enable <service name>.service`
- Disable a service to not start during boot: `sudo systemctl disable <service name>.service`
- Check if a service is enabled or not: `sudo systemctl is-enabled <service name>`
- Start service manually: `sudo systemctl start <service name>`
- Stop service manually: `sudo systemctl stop <service name>`
- Restart service manually: `sudo systemctl restart <service name>`
- Show the status of a service including, whether it is running or not: `sudo systemctl status <service name>`
- Systemd services can be modified using `sudo systemctl edit <service name>.service`

### Helpful links
- https://docs.fedoraproject.org/en-US/quick-docs/understanding-and-administering-systemd/
- https://www.freedesktop.org/software/systemd/man/systemd.unit.html
- https://ma.ttias.be/auto-restart-crashed-service-systemd/
- https://unix.stackexchange.com/questions/397853/how-to-set-a-systemd-unit-to-start-after-loading-the-desktop
- https://serverfault.com/questions/736624/systemd-service-automatic-restart-after-startlimitinterval