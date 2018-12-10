#!/usr/bin/env python

import os
import sys
import time
import util
import RPi.GPIO as GPIO

def main():
    # GPIO初期化
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.OUT)

    # 設定読み込み
    setting_json = util.json_read()

    wait     = float(setting_json['wait'])
    release  = float(setting_json['release'])
    interval = float(setting_json['interval'])

    # 指定秒だけウェイト
    time.sleep(wait)

    # メインループ
    while True:
        time.sleep(interval)
        GPIO.output(4, True)
        time.sleep(release)
        GPIO.output(4, False)

def daemonize():
    pid = os.fork()
    # 親プロセス
    if pid > 0:
        pid_file = open('/var/run/chainoiler.pid','w')
        pid_file.write(str(pid)+"\n")
        pid_file.close()
        sys.exit()
    # 子プロセス
    if pid == 0:
        main()

if __name__ == '__main__':
    while True:
        daemonize()
