#! /usr/bin/env python
import rclone
import logging
import os
import json
import time
from telegram.ext import Updater, MessageHandler


cfg = open(os.environ["RCLONE_CONF"])
cfg = cfg.read()
if not os.path.exists("state/"):
    os.mkdir("state/")
src_file = os.environ["SRC_FILE"]
tg_token = os.environ["TG_TOKEN"]
tg_channel = os.environ["TG_CHANNEL"]


logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(name)s [%(levelname)s]: %(message)s")


def do_bkp(name, params):
    result = rclone.with_config(cfg).sync(
        params["source"], params["provider"] + ":" + params["dest"], flags=["--skip-links", "--exclude-from", "/app/exclude.txt"])
    if result["code"] == 0:
        if not os.path.exists("state/" + name):
            os.mkdir("state/" + name)
        lastrun = open("state/" + name + "/bkpy.lastrun.txt", "w+")
        lastrun.write(str(time.time()))
        lastrun.close()
        copylastrun = rclone.with_config(cfg).copy(
            lastrun.name, params["provider"] + ":" + params["dest"])
        if not copylastrun == 0:
            result = copylastrun
    else:
        print(result["error"])
    return result


def check_age(name, params):
    getlast = rclone.with_config(cfg).copy(
        params["provider"] + ":" + params["dest"] + "bkpy.lastrun.txt", "state/" + name)
    if getlast["code"] == 0:
        checklast = open("state/" + name + "/bkpy.lastrun.txt", "r")
        lastrun = float(checklast.read())
        nextrun = time.time() - params["age"]*86400
        return nextrun > lastrun
    else:
        return True


def send_msg(name, params, bkp_time):
    msg = "Backup {} completed in {} minutes.\nNext backup in {} days.".format(
        name, int(bkp_time/60), params["age"])
    print(msg)
    updater = Updater(token=tg_token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.bot.send_message(chat_id=tg_channel, text=msg)


with open(src_file) as srcpath:
    source = json.loads(srcpath.read())


for k, v in source.items():
    start_time = time.time()
    msg = "Checking backup age for {}.".format(k)
    check = check_age(k, v)
    if check:
        print("Starting backup for " + k)
        bkp = do_bkp(k, v)
        total_time = time.time() - start_time
        if bkp['code'] == 0: send_msg(k, v, total_time)
        print("Backup done for " + k)
    else:
        print("Backup is up to date")
        