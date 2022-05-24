# Install service
```bash
mkdir /var/log/rent_bot

cp rent_bot.service /etc/systemd/system/
systemctl daemon-reload
sudo service rent_bot restart
sudo service rent_bot status

journalctl -e -u rent_bot.service
```

# Logs' rotation
```bash
nano /etc/logrotate.d/rent_bot
```
With the following content
```bash
/var/log/rent_bot/log {
    monthly
    missingok
    rotate 12
    notifempty
}
```
