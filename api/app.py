#!/usr/bin/env python
import web
import json
import datetime
import requests

urls = (
    '/location/?', 'location',
    '/.*', 'insert',
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
    def GET(self):
        'Present docs'
        return '''
<h1>Wait Time API Docs</h1>
<iframe src='http://pad.transparencycamp.org/p/waittimes?showControls=true&showChat=true&showLineNumbers=true&useMonospaceFont=false' width=100% height=80%>
        '''
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
            elif set(MIN_KEYS) == set(doc.keys()):
                raise ValueError('must include at least one of time[1-3], timediff[21,31,32]')

            # Validate times, but not now
            doc["timeReceived"] = datetime.datetime.now().isoformat()

            # Hack
            doc['appId'] = doc['apikey']
            del(doc['apikey'])


            # Stringify the locationId
            doc['locationId'] = unicode(doc['locationId'])

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

    PUT = POST

class location:
    def GET(self):
        try:
            apprequest = json.loads(web.data())
            if set(apprequest.keys()) != set(GET_KEYS):
                raise ValueError('You need to send these and only these keys: %s' % ', '.join(list(GET_KEYS)))

            return requests.get(
                'https://waittimes.iriscouch.com/waittimes/_design/all/_view/all?key=%22{locationId}%22&limit={limit}'.format(**apprequest)
            ).text
        except Exception, msg:
            return json.dumps({"ok": False, "message": unicode(msg)})

if __name__ == "__main__":
    app.run()
