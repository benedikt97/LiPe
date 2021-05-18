#!/usr/bin/python3

from flask import Flask
from flask import request
from flask import render_template
import LiPeDB as lpd
import LiPe as lp
import LiPeOPC as lpo


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/api', methods=['GET'])
def api():
    c = request.args.get('c')
    p1 = request.args.get('p1')
    p2 = request.args.get('p2')
    try:
# OPC Commands
        if (c == "initopc"):
            opccon.initOpc(lp.loadopcconfig(), lp.loadnodes())
            return "done"
        if (c == "stopopc"):
            opccon.stopOpc()
            return "done"
        elif (c == "opcstatus"):
            if opccon.getStatus():
                return "Running"
            else:
                return "Not Running"
# Server Command
        elif (c == "deleteserverlog"):
            dbcon.deleteLog()
            return "done"
#DB Commands            
        elif (c == "getopclogs"):
            result = dbcon.getTables()
            return result
        elif (c == "getlogs"):
            result = dbcon.getLog()
            return result
        elif (c == "getopcconfig"):
            result = lp.loadopcconfig()
            return result
        elif (c == "getactvalues"):
            result = opccon.getActValues()
            return result
        elif (c == "getstaticvalues"):
            result = opccon.getStaticValues()
            return result
        elif (c == "gettablelastx"):
            result = dbcon.getLastXTableRows(p1, p2)
            return result
        elif (c == "getnodes"):
            result = lp.loadnodes()
            result = result["cyclic"]
            return result
        

        

        return c + " Parameter not Vaild"
    except Exception as e:
        result = str(e)
        return result



@app.route('/test')
def test():
    result = dbcon.Test()
    return result
    


if __name__ == '__main__':
    dbcon = lpd.dbcon("LiPe", "127.0.0.1", "LiPeUser", "LiPePWD320")
    opccon = lpo.opccon()
    configjs = lp.loadserverconfig()
    app.run(configjs['IP'], configjs['Port'])
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
