# BKPy 
A backup script writen in Python using Rclone and [python-rclone](https://github.com/ddragosd/python-rclone) library. It requires a preconfigured `rclone.conf` with all remotes to be backup, a Telegram bot token and a Telegram channel handle or ID to send it's report messages.

## Configuration and Build Instructions
Before building the image create or update the following files:

```
app\exclude.txt
.env
rclone.conf
ssh\id_rsa
ssh\id_rsa.pub
sourcelist.json
```
The `app\exclude.txt` should have the files and paths to be excluded from the backup. Check [Rclone filtering](https://rclone.org/filtering/) documentation for usage.

The `.env` file must have two vars:

```
TG_TOKEN="your_telegram_bot_token"
TG_CHANNEL="@your_telegram_report_channel"
```



The `rclone.conf` must be pre generated or copied from a previous installation and must have all the sources and destionation remotes configured (eg: your Google Drive account and your desktop as a SSH remote).

After create and update all the files build the image:

```
docker build -t bkpy .
```
