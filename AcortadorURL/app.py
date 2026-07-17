import secrets
from flask import Flask, render_template, request, redirect, abort

app = Flask(__name__)

short_urls = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['URLusuario']
        short_id = secrets.token_urlsafe(4)
        short_urls[short_id] = url
        short_url = request.host_url.rstrip('/') + '/' + short_id
        return render_template('index.html', short_url=short_url, original_url=url)
    return render_template('index.html')

@app.route('/<short_id>')
def redirect_short_url(short_id):
    if short_id in short_urls:
        return redirect(short_urls[short_id])
    return abort(404)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
