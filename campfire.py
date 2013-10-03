import urllib2
import json
import time
# https://github.com/codedance/Retaliation
import retaliation

# campfire api connection details
user = 'YOUR_CAMPFIRE_API_TOKEN'
password = 'X'
url = 'YOUR_CAMPFIRE_ROOM/recent.json'
last_checked_message = False;

def encodeUserData(user, password):
    return "Basic " + (user + ":" +password).encode("base64").rstrip()

while True:
    # only retrieve messages that have not yet been checked to avoid accidential missile strikes
    if (last_checked_message):
        request = urllib2.Request(url + '?since_message_id=' + last_checked_message)
    else:
        request = urllib2.Request(url + '?limit=1')

    request.add_header('Authorization', encodeUserData(user, password))

    response = urllib2.urlopen(request)
    messages = response.read()
    json_data = json.loads(messages)

    time.sleep(15)
    
    # check latest messages in campfire if any exist
    if json_data["messages"]:
        if json_data["messages"][-1]["id"] != last_checked_message:
            print "last message was: " + json_data["messages"][-1]["body"]
            last_checked_message = str(json_data["messages"][-1]["id"])
    else:
        print "nothing to see here... yet"

    # fire missile if launch codes exist
    if messages.find("/shoot ") != -1:
        print "launch sequence initiated."
        retaliation.main([0,"brian"])
        print "missile has been launched."