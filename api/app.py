#!/usr/bin/env python
import web
import json
import datetime
import requests

urls = (
    '/.*', 'everything'
)
app = web.application(urls, globals())

#web.config.debug = False

MIN_KEYS = set(['locationId', 'apikey', 'userId'])
MAX_KEYS = set([
    "locationId",
    "appId",
    "appUserId",
    "time1",
    "time2",
    "time3",
    "timediff21",
    "timediff31",
    "timediff32",
    "appspecific",
])

class everything:
    def POST(self):
        'Query string like ?doc={saoehaostnoeau:asoetusoaestn,soe:soe} '
        try:
            doc = json.loads(web.data())

            # Test this
            # doc['locationId']

            # Minimum keys
            if not MIN_KEYS.issubset(doc.keys()):
                raise ValueError('locationId, apikey and userId are required.')
            elif MAX_KEYS.issuperset(doc.keys()):
                raise ValueError('one of the keys you entered isn\'t allowed')

            # Validate times, but not now
            doc["timeReceived"] = datetime.datetime.now().isoformat()

            # Hack
            doc['appId'] = doc['apikey']
            del(doc['apikey'])

            docs = json.dumps({"docs":[doc]})
            dbresponse = requests.post(
                'http://waittimes.iriscouch.com/waittimes/_bulk_docs',
                docs,
                headers = {
                    'Content-Type': "application/json; charset=utf-8"
                }
            )
            return dbresponse.text[1:-1] #Remove brackets from JSON list
        except Exception, msg:
            return json.dumps({"ok": False, "message": unicode(msg)})

    GET = POST
    PUT = POST

if __name__ == "__main__":
    app.run()
