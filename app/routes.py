from app import app
from flask import render_template, request, abort, send_from_directory, make_response, jsonify
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
        'fontsize': '100%'
    }
    
book = Book(args.file)
currentChapterNum = config['books'].get(book.get_title(), dict()).get('chapter', 0)

@app.route('/')
def entrypoint():
    return index(currentChapterNum, startOnProgress = True)


@app.route('/<int:num>')
def index(num, link = None, startOnProgress = False):
    global currentChapterNum
    url = book.id_to_href[book.content_spine_ids[num]]
    if book.is_valid_chapter(num - 1):
        prev = num - 1
    else:
        prev = -1 # because template adds 1 to prev and if result is = 0 than it hides the buttone
    if book.is_valid_chapter(num + 1):
        next_ = num + 1
    else:
        next_ = None
    currentChapterNum = num
    try:
        config['books'][book.get_title()]['chapter'] = currentChapterNum
    except KeyError:
        config['books'][book.get_title()] = dict()
        config['books'][book.get_title()]['chapter'] = currentChapterNum
    if startOnProgress:
        progress = config['books'].get(book.get_title(), dict()).get('progress', 0)
    else:
        progress = 0
    return render_template(
        'index.html',
        contentUrl = url, 
        prev = prev, 
        next = next_, 
        num = num, 
        total = len(book.content_spine_ids), 
        link = link, 
        progress = progress, 
        title = book.get_title(), 
        fontSize = config.get('fontsize', '100%')
    )

@app.route('/api/pushProgress/<int:progress>')
def saveProgress(progress):
    config['books'][book.get_title()]['progress'] = progress
    with open(args.config, 'w+') as f:
        f.write(json.dumps(config))
    return jsonify({'pos': progress})

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