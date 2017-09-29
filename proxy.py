from flask import Flask, jsonify, Response, request, redirect
import requests
import re


app = Flask(__name__)
HABR_URL = 'https://habrahabr.ru/'


@app.route('/', methods=['GET', 'POST'])
@app.route('/<path:url>', methods=['GET', 'POST'])
def proxy(url=''):
    headers = dict(request.headers)
    cookies = dict(request.cookies)
    del headers['Host']
    if request.method == 'POST':
        data = request.get_data()
        page = requests.post(HABR_URL + url,
                             data, headers=headers, cookies=cookies, allow_redirects=False)
    else:
        page = requests.get(HABR_URL + url,
                            headers=headers, cookies=cookies, allow_redirects=False)
    content = page.content.decode()
    if request.base_url.endswith('/'):
        content = content.replace(HABR_URL, request.url_root)
        content = re.sub('([\s>])([A-Za-zА-Яа-я0-9]{6})([<\s])', r'\1\2™\3', content)
    resp_headers = dict(page.headers)
    if 'Content-Encoding' in resp_headers:
        del resp_headers['Content-Encoding']
    response = Response(response=content, status=page.status_code, headers=resp_headers)
    return response


if __name__ == '__main__':
    app.run(port=8099)
