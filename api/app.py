#!/usr/bin/env python
import web
import json
import datetime
import requests

urls = (
    '/', 'insert',
    '/location/?', 'location',
)
app = web.application(urls, globals())

#web.config.debug = False

GET_KEYS = set(['locationId', 'apikey', 'limit'])
MIN_KEYS = set(['locationId', 'apikey', 'appUserId'])
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

class insert:
    def POST(self):
        'Query string like ?doc={saoehaostnoeau:asoetusoaestn,soe:soe} '
        try:
            doc = json.loads(web.data())

            # Test this
            # doc['locationId']

            # Minimum keys
            if not MIN_KEYS.issubset(doc.keys()):
                raise ValueError('locationId, apikey and appUserId are required.')
            elif MAX_KEYS.issuperset(doc.keys()):
                raise ValueError('one of the keys you entered isn\'t allowed')
            elif doc.keys().issubset(MIN_KEYS):
                raise ValueError('must include at least one of time[1-3], timediff[21,31,32]')

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

class location:
    def GET(self):
        try:
            apprequest = json.loads(web.data())
            if set(apprequest.keys()) != set(GET_KEYS):
                raise ValueError('You need to send these and only these keys: %s' % ', '.join(list(GET_KEYS)))

            return requests.get(
                'https://waittimes.iriscouch.com/waittimes/_design/all/_view/all?key={locationId}&limit={limit}'.format(**apprequest)
            ).text
        except Exception, msg:
            return json.dumps({"ok": False, "message": unicode(msg)})

    PUT = POST

if __name__ == "__main__":
    app.run()
