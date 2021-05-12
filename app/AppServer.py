#!/usr/bin/python3

from flask import Flask
from flask import request
from flask import render_template
import LiPeDB as lpd
import LiPe as lp
import LiPeOPC as lpo
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get', methods=['GET'])
def get():
    r = request.args.get('e')
    try:
        if (r == "tables"):
            result = dbcon.getTables()
            return result
        elif (r == "logs"):
            result = dbcon.getLog()
            return result
        elif (r == "opcconfig"):
            result = lp.loadopcconfig()
            return result
        elif (r == "actvalues"):
            result = opccon.getActValues()
            return result
        return r + " Parameter not Vaild"
    except:
        result = "Error: No Parameters"
        return result


@app.route('/cmd/db', methods=['GET'])
def cmddb():
    r = request.args.get('e')
    try:
        if (r == "deletelog"):
            dbcon.deleteLog()
            return "done"
        return r + " Parameter not Vaild"
    except Exception as e:
        result = str(e)
        return result

@app.route('/cmd/opc', methods=['GET'])
def cmdopc():
    r = request.args.get('e')
    try:
        if (r == "initOpc"):
            opccon.initopc(lp.loadopcconfig(), lp.loadnodes())
            return "done"
        elif (r == "startOpc"):
            opccon.collect(True)
            return "done"
        return r + " Parameter not Vaild"
    except Exception as e:
        result = str(e)
        return result


@app.route('api', methods=['GET'])
def api():
    c = request.args.get('c')
    try:
        if (r == "initOpc"):
            opccon.initopc(lp.loadopcconfig(), lp.loadnodes())
            return "done"
        elif (r == "startOpc"):
            opccon.collect(True)
            return "done"
        return r + " Parameter not Vaild"
    except Exception as e:
        result = str(e)
        return result



@app.route('/test')
def test():
    result = dbcon.Test()
    return result
    


if __name__ == '__main__':
    dbcon = lpd.dbcon("LiPe", "127.0.0.1", "LiPeUser", "LiPePWD320")
    opccon = lpo.opccon(lp.loadopcconfig(), lp.loadnodes())
    configjs = lp.loadserverconfig()
    app.run(configjs['IP'], configjs['Port'])
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
