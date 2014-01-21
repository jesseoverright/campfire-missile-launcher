import urllib2
import json
import time
# https://github.com/codedance/Retaliation
import retaliation

# campfire api connection details
user = 'YOUR_CAMPFIRE_API_TOKEN'
password = 'X'
url = 'YOUR_CAMPFIRE_ROOM/recent.json'

TARGETS = {
    "door" : (
        ("led", 1),
        ("right",3600),
        ("up", 540),
        ("fire",1),
        ("led",0),
        ("zero", 0),
    ),
    "brian" : (
        ("led", 1),
        ("right",600),
        ("up",300),
        ("fire",1),
        ("led",0),
        ("zero",0)
    ),
    "chair" : (
        ("led", 1),
        ("right",2250),
        ("up", 150),
        ("fire", 4),
        ("led", 0),
        ("zero", 0)
    ),
    "jesse" : (
        ("led", 1),
        ("right", 6000),
        ("up",400),
        ("fire",1),
        ("led", 0),
        ("zero", 0)
    ),
    "breakingbad" : (
        ("led",1),
        ("up",500),
        ("right",2300),
        ("fire",1),
        ("right",300),
        ("fire",1),
        ("right",300),
        ("fire",1),
        ("right",300),
        ("fire",1),
        ("led",0),
        ("zero", 0),
    ),
}

def encodeUserData(user, password):
    return "Basic " + (user + ":" +password).encode("base64").rstrip()

def watch_camp():
    retaliation.setup_usb()
    print "missle launcher armed!"

    last_checked_message = False

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

        # check latest messages in campfire if any exist
        if json_data["messages"]:
            if json_data["messages"][-1]["id"] != last_checked_message:
                print "last message was: " + str(json_data["messages"][-1]["body"])
                last_checked_message = str(json_data["messages"][-1]["id"])
        else:
            print "nothing to see here... yet"

        for target, position in TARGETS.items():
            campfire_trigger = "/shoot %s" % target

            # fire missile if launch codes exist in chat
            if campfire_trigger in messages:
                print "launch sequence '%s' initiated" % target
                retaliation.run_command_set(TARGETS[target])
                print "missile has been launched. target destroyed."

        time.sleep(15)

if __name__ == '__main__':
    watch_camp()