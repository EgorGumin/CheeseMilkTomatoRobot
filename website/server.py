import cgi
import http.server
import os
import shutil
from PIL import Image
import requests

import predict

PORT_NUMBER = 8080
number = 0
guessed = {}


def load_picture(link):
    global number
    if link == '\n':
        return None
    link = link.replace('\n', '')
    if not (link.endswith('jpg') or link.endswith('jpeg')):
        return None
    try:
        r = requests.get(link, stream=True)
        if r.status_code == 200:
            pic_name = 'pics/' + ('0' + str(number) if number < 10 else str(number)) + '.jpg'
            with open(pic_name, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)

            image = Image.open(pic_name)
            image.load()
            if image.format != 'JPEG':
                print(pic_name + ' error: no JPEG')
                image.close()
                return None
            image.close()
            number += 1
            return pic_name

    except IOError as e:
        print(e)
        print('Bad image: ' + link)
        return None


def get_photos_urls():
    lst = os.listdir('pics/')
    lst.sort(reverse=True)
    available = []
    for pic in lst:
        if 'pics/' + pic in guessed:
            available.append('pics/' + pic)
            if len(available) == 4:
                break
    return available


def get_photos_html(urls):
    block = '<div class="w3-row-padding w3-center" id="photos"> <h3>Recently guessed</h3><br>'
    for url in urls:
        block += '<div class="w3-quarter"> <img src="' + url + \
                 '"style="height:200px"><h3>' + guessed[url] + '</h3> </div> '
    block += '</div> <hr>'
    return block


def insert_photos(page):
    urls = get_photos_urls()
    if len(urls) != 0:
        page = page.replace("{photos}", get_photos_html(urls))
    else:
        page = page.replace("{photos}", '')
    return page


def insert_prediction(page, pic=None, error=False):
    if error:
        return page.replace('{prediction}', "<div class='w3-row-padding w3-center'><h3>There is an error with your image. \
                                            Don't  give up, try another one! </h3></div> <hr>")
    if pic is None:
        page = page.replace('{prediction}', '')
    else:
        block = '<div class="w3-row-padding w3-center"> <h3>Prediction for you: <b>' \
                + guessed[pic] + '</b>!</h3> <img src="' + pic + '" style="height: 200px"> </div> <hr>'
        page = page.replace('{prediction}', block)
    return page


class myHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            f = open('index.html')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(insert_prediction(insert_photos(f.read())).encode())
            f.close()
            return

        if str(self.path).startswith('/pics'):
            f = open(str(self.path).replace('/pics', 'pics'), mode='rb')
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
            return

    def do_POST(self):
        if self.path == "/predict":
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': self.headers['Content-Type'],
                         })
            link = form["link"].value

            pic = load_picture(link)


            f = open('index.html')

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            if pic is not None:
                prediction = predict.predict(pic)
                guessed[pic] = prediction
                html = insert_photos(insert_prediction(f.read(), pic=pic))
            else:
                html = insert_photos(insert_prediction(f.read(), error=True))
            self.wfile.write(html.encode())
            f.close()
            return


server = http.server.HTTPServer(('', PORT_NUMBER), myHandler)
print('Started httpserver on port ', PORT_NUMBER)
server.serve_forever()
