import json
import subprocess
import os
import RPi.GPIO as GPIO

JSON_PATH = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = JSON_PATH + '/setting.json'

def json_read():
    # 設定JSONの読み込み
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        setting_json = json.load(f)

    return(setting_json)


def json_write(upd_json):
    # 設定JSONの書き込み
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        f.write(json.dumps(upd_json))

    return


def systemd_control(command):
    # オイラーサービスの制御
    cmd = 'systemctl ' + command + ' raspberry_oiler'

    try:
        subprocess.check_call(cmd, shell=True)
    except:
        print(cmd + ' failed')
    
    return

def GPIO_init():
    # サービス停止のタイミングによってはGPIOが通電したままになるため、初期化
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.OUT)
    
    GPIO.output(4, False)

    GPIO.cleanup()

    return
