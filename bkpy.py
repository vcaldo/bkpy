#! /usr/bin/env python
import rclone
import logging
import os
import json
import time

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(name)s [%(levelname)s]: %(message)s")
cfg = open(os.environ["HOME"] + "/.config/rclone/rclone.conf")
cfg = cfg.read()
if not os.path.exists("state/"):
    os.mkdir("state/")


def do_bkp(name, params):
    result = rclone.with_config(cfg).sync(
        params["source"], params["provider"] + ":" + params["dest"])
    if result["code"] == 0:
        if not os.path.exists("state/" + name):
            os.mkdir("state/" + name)
        lastrun = open("state/" + name + "/bkpy.lastrun.txt", "w+")
        lastrun.write(str(time.time()))
        lastrun.close()
        copylastrun = rclone.with_config(cfg).copy(
            lastrun.name, params["provider"] + ":" + params["dest"])
        if copylastrun == 0:
            print("backup ok, lastrun ok")
        else:
            print(copylastrun["error"])
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


with open("sourcelist.json") as srcpath:
    source = json.loads(srcpath.read())

for k, v in source.items():
    msg = "Checking backup age for {}.".format(k)
    print(msg)
    check = check_age(k, v)
    if check:
        print("Starting backup for " + k)
        bkp = do_bkp(k, v)
    else:
        print("Backup is up to date")
