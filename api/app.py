import web
import json

urls = (
    '/.*', 'everything'
)
app = web.application(urls, globals())

class everything:
    def GET(self):
        'Query string like ?doc={saoehaostnoeau:asoetusoaestn,soe:soe} '
        data = web.input()
        doc = json.loads(data['doc'])

        # Test this
        # doc['locationId']


        # Minimum keys
        if not set(['locationId', 'apikey', 'userId']).issubset(doc.keys()):
            raise ValueError('locationId, apikey and userId are required.')
        elif 

        # Hack
        doc['appId'] = doc['apikey']
        del(doc['apikey'])

    def POST(self, 

    PUT = POST

if __name__ == "__main__":
    app.run()
