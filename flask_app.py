# Import statements necessary
from flask import Flask, render_template
from flask_script import Manager
import requests
import json

# Set up application
app = Flask(__name__)

manager = Manager(app)


# Routes
@app.route('/')
def hello_world():
    return '<h1>Hello World!</h1>'


@app.route('/user/<yourname>')
def hello_name(yourname):
    return '<h1>Hello {0}</h1>'.format(yourname)


@app.route('/showvalues/<name>')
def basic_values_list(name):
    lst = ["hello", "goodbye", "tomorrow", "many", "words", "jabberwocky"]
    if len(name) > 3:
        long_name = name
        short_name = None
    else:
        long_name = None
        short_name = name
    return render_template('values.html', word_list=lst, long_name=long_name,
                           short_name=short_name)


# PART 1: Add another route /word/<new_word> as the instructions describe.
@app.route('/word/<new_word>')
def rhyme_word(new_word):
    baseurl = 'https://api.datamuse.com/words'
    params = {}
    params['rel_rhy'] = new_word.strip()
    params['max'] = 1
    response_obj = requests.get(baseurl, params=params)
    datamuse_data = json.loads(response_obj.text)
    return '<h1>Word {0} rhymes with {1}</h1>'.format(
        new_word.strip(), datamuse_data[0]['word'])


# PART 2: Edit the following route so that the photo_tags.html template will
# render
@app.route('/flickrphotos/<tag>/<num>')
def photo_titles(tag, num):
    # HINT: Trying out the flickr accessing code in another file and seeing
    # what data you get will help debug what you need to add and send to the
    # template!
    # HINT 2: This is almost all the same kind of nested data investigation
    # you've done before!
    # fill in a flickr key
    FLICKR_KEY = "7df34cf4700d90ca91aa20f4432d2f9b"
    baseurl = 'https://api.flickr.com/services/rest/'
    params = {}
    params['api_key'] = FLICKR_KEY
    params['method'] = 'flickr.photos.search'
    params['format'] = 'json'
    params['tag_mode'] = 'all'
    params['per_page'] = num
    params['tags'] = tag
    response_obj = requests.get(baseurl, params=params)
    trimmed_text = response_obj.text[14:-1]
    flickr_data = json.loads(trimmed_text)
    # Add some code here that processes flickr_data in some way to get
    # what you nested
    photo_titles = [photo['title'] for photo in flickr_data['photos']['photo']]

    # Edit the invocation to render_template to send the data you need
    return render_template('photo_info.html', photo_titles=photo_titles,
                           num=int(num), tag=tag)


if __name__ == '__main__':
    # Runs the flask server in a special way that makes it nice to debug
    manager.run()
