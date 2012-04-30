#!/usr/bin/env python
import web
import json

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

            #"timeReceived": "2012-11-04 13:20:02 GMT-7",

            # Hack
            doc['appId'] = doc['apikey']
            del(doc['apikey'])
            return json.dumps(doc)
        except Exception, msg:
            return json.dumps({"status": "error", "message": unicode(msg)})

    GET = POST
    PUT = POST

if __name__ == "__main__":
    app.run()
