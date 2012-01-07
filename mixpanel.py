import subprocess
import base64
import json as simplejson

def track(event, properties=None):
                properties = {}
                token = "e18b33ca2a37a1546e29e73fa215e389";
                print "token added";
                properties["token"] = token
                params = {"event": event, "properties": properties}
                data = base64.b64encode(simplejson.dumps(params))
                request = "http://api.mixpanel.com/track/?data=" + data
                print request;
                return subprocess.Popen(("curl",request), stderr=subprocess.PIPE, stdout=subprocess.PIPE)

if __name__ == '__main__':
        print "Hello World";
        track("invite-friends", {"method": "email", "number-friends": "12", "ip": "123.123.123.123"})
