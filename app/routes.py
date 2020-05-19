from app import app
from flask import render_template, request, abort, send_from_directory, make_response
import argparse, os, json
from .book import Book

__version__ = 0.1

configPath = os.path.expanduser('~/.pyPub.json')
parser = argparse.ArgumentParser(description = 'A simple ebook reader by Grzegorz Koperwas', prog = 'tinyPub', epilog = 'Configuration and reading progress is stored in ~/.tinypub.json', allow_abbrev = True)
parser.add_argument('file', type = str, help = 'Path to .epub file.', metavar = 'file_path')
parser.add_argument('--config', dest='config', type = str, help = 'Path to alternative config file', default = configPath, metavar = 'PATH')
parser.add_argument('--version', action='version', version = __version__)
args = parser.parse_args()
try:
    with open(args.config) as f:
        config = json.loads(f.read())
except FileNotFoundError as e:
    config = {
        'name': 'pyPub v.2',
        'books': {},
        'lineLength': 78,
        'keybinds': {
            'h': 'prev',
            'j': 'down',
            'k': 'up',
            'l': 'next'
        }
    }
book = Book(args.file)


@app.route('/<int:num>')
def index(num, link = None):
    url = book.id_to_href[book.content_spine_ids[num]]
    if book.is_valid_chapter(num - 1):
        prev = num - 1
    else:
        prev = -1 # because template adds 1 to prev and if result is = 0 than it hides the buttone
    if book.is_valid_chapter(num + 1):
        next_ = num + 1
    else:
        next_ = None
    return render_template('index.html', contentUrl = url, prev = prev, next = next_, num = num, total = len(book.content_spine_ids), link = link)

@app.route('/<path:path>')
def item(path):
    try:
        res = book.get_href(path)
        if res.get_id() in book.content_spine_ids and request.args.get('raw_html') != 'yes':
            return index(book.content_spine_ids.index(res.get_id()), link = True)
        else:
            response = make_response(res.content, 200)
            response.headers['Content-Type'] = res.media_type
            return response
    except Exception as e:
        print(e)
        abort(404)