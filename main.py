#coding:utf-8

from flask import Flask, render_template,request
import util


app = Flask(__name__)

@app.route('/')
def index():

    setting_json = util.json_read()

    wait_now     = setting_json['wait']
    release_now  = setting_json['release']
    interval_now = setting_json['interval']

    return render_template('index.html',wait=wait_now,release=release_now,interval=interval_now)


@app.route('/setting', methods=['POST'])
def setting():
    wait_upd     = request.form['wait']
    release_upd  = request.form['release']
    interval_upd = request.form['interval']

    setting_json = util.json_read()

    setting_json['wait']     = wait_upd
    setting_json['release']  = release_upd
    setting_json['interval'] = interval_upd

    util.json_write(setting_json)

    util.systemd_control('stop')
    util.GPIO_init()
    util.systemd_control('start')
    
    return render_template('index.html',wait=wait_upd,release=release_upd,interval=interval_upd)

@app.route('/start', methods=['POST'])
def start():
    util.systemd_control('start')

    setting_json = util.json_read()

    wait_now     = setting_json['wait']
    release_now  = setting_json['release']
    interval_now = setting_json['interval']

    return render_template('index.html',wait=wait_now,release=release_now,interval=interval_now)

@app.route('/stop', methods=['POST'])
def stop():
    util.systemd_control('stop')
    util.GPIO_init()

    setting_json = util.json_read()

    wait_now     = setting_json['wait']
    release_now  = setting_json['release']
    interval_now = setting_json['interval']

    return render_template('index.html',wait=wait_now,release=release_now,interval=interval_now)

@app.route('/maintenance', methods=['POST'])
def maintenance():
    # 初期設定等で長時間全開にするためのモード
    wait_upd     = "0"
    release_upd  = "3600"
    interval_upd = "0"

    setting_json = util.json_read()

    setting_json['wait']     = wait_upd
    setting_json['release']  = release_upd
    setting_json['interval'] = interval_upd

    util.json_write(setting_json)

    util.systemd_control('stop')
    util.GPIO_init()
    util.systemd_control('start')

    return render_template('index.html',wait=wait_upd,release=release_upd,interval=interval_upd)

if __name__ == '__main__':
    app.run(debug=True)