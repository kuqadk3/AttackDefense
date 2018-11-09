from flask import Flask
from flask import request
import requests

app = Flask(__name__)

def make_request(flag):
    url = 'http://monitor.ructfe.org/flags'
    response = requests.put(url, data=flag) 

    if response['status'] == "false":
        return "Denied"

@app.route('/submit-flag')
def submit_flag(self):
   """ Submit flags"""
   if request.method == 'POST':
       flag = request.args.get('flag')
       make_request(flag)


if __name__ == '__main__':
    app.run(debug=True)

