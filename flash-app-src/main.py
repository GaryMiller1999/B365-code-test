from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from common.check_ip_addresses import IPChecker
from urllib import parse as url_parse
import os


port = int(os.environ.get('PORT', 5000))
app = Flask(__name__)




@app.route('/checkip')
def checkip():


    
    args = request.args.get("ips")


    if args == None or args == "":
        return "please supply data via the query value \"ips\""
    # parser = reqparse.RequestParser()
    # parser.add_argument('ip')

    # args = parser.parse_args()

    ipchecker = IPChecker(args.split(","))
    return str(ipchecker.fetch())
    #return IPChecker(args.ipaddresses.split(","))






if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)