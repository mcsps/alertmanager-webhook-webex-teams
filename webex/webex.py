from flask import Flask, request
#from jinja2.utils import markupsafe
#from markupsafe import Markup
from os import environ
from werkzeug.exceptions import HTTPException
import pycurl
import json

webex_token = environ.get('WEBEX_TOKEN')
webex_room = environ.get('WEBEX_ROOM')

app = Flask(__name__)

@app.route('/alertmanager', methods=['POST'])
def alertmanager():
    try:
        if request.is_json:
            post_data = json.loads(request.data)
            alert_data(post_data)
    except Exception as e:
        print("Storing alerts failed in main: %s", e)
        return {"ERROR"}, 500

    return "NOK", 200

def alert_data(data):
    if "alerts" in data:
        for i in data["alerts"]:
            try:
                alertname = "### alertname: "
                severity = "severity: "
                cluster = "## cluster: "
                instance = "instance: "
                message = "message: "
                start = "start: "
                end = "end: "
                if "alertname" in i["labels"]:
                    alertname = alertname + i["labels"]["alertname"]
                if "severity" in i["labels"]:
                    severity = severity + i["labels"]["severity"]
                if "cluster" in i["labels"]:
                    cluster = cluster + i["labels"]["cluster"]
                if "instance" in i["labels"]:
                    instance = instance + i["labels"]["instance"]
                if "message" in i["annotations"]:
                    message = message + i["annotations"]["message"]
                if i["startsAt"]:
                    start = start + i["startsAt"]
                if i["endsAt"]:
                    end = end + i["endsAt"]
                alert = cluster + "\n" + alertname + "\n" + severity + "\n" + instance + "\n" + message + "\n" + start + "\n" + end
                webex = [("roomId", webex_room), ("markdown", str(alert))]
                headers = ['Authorization: Bearer ' + webex_token ]
                crl = pycurl.Curl()
                crl.setopt(pycurl.URL, 'https://webexapis.com/v1/messages')
                crl.setopt(pycurl.HTTPHEADER, headers)
                crl.setopt(pycurl.HTTPPOST, webex)
                crl.perform()
                crl.close()
            except Exception as e:
                print("Storing alerts failed in sub: %s", e)
                return {"ERROR"}, 500

    return "OK", 200

@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

if __name__ == '__main__':

  app.run(
    host = "0.0.0.0",
    port = 9091,
    debug = 0
  )
