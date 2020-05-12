import falcon
from wsgiref import simple_server
import json, cv2, base64
from textblob import TextBlob

class Resource(object):

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        print('here')
        with open('index.html', 'r') as f:
            resp.body = f.read()

    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200
        text = req.params['textblob']
        expression = TextBlob(text).sentiment
        total = expression.polarity

        with open('Figure_1.png', mode='rb') as file:
            image = file.read()

        reply = {
            'text': text,
            'polarity': total,
            'image': base64.encodebytes(image).decode("utf-8")
        }
        resp.body = json.dumps(reply)

app = api = falcon.API()
app.req_options.auto_parse_form_urlencoded = True
api.add_route('/', Resource())

if __name__ == '__main__':
    print('server started...')
    http = simple_server.make_server('127.0.0.1', 8000, app)
    http.serve_forever()
