""" gh-index """
from __future__ import print_function
import json
import re
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen
from flask import Flask, render_template, jsonify, request, url_for, redirect
from wtforms import Form, StringField, validators

app = Flask(__name__)

URLTEMPLATE = "https://api.github.com/users/{}/repos?per_page=100&page={}"

class SearchForm(Form):
    """ set up wtforms class """
    keywords = StringField('query', [
        validators.Length(max=30, message='[error : too many characters]'),
        validators.Regexp(r'^[-a-zA-Z0-9]*$',
                          message='[error : invalid characters. Use only A-Z,\
                                   0-9, and hyphen]'),
        validators.DataRequired(message='[error : you must type something]')])

# load the html page
@app.route('/')
def index():
    """ load the index page """
    return render_template("gh-index.html")


@app.route('/calculate')
def calculate():
    """ do the calculations and return jsonified data """

    # create some empty lists
    data = []
    repolist = []
    jsondata = []
    countlist = []

    # take the input and validate it
    user = request.args.get("a")
    form = SearchForm(keywords=user)
    if form.validate():

        # make the api call
        # the api breaks results into pages. iterate through pages
        for i in range(1, 4):
            url = URLTEMPLATE.format(user, i)
            try:
                data.append(urlopen(url))
            except Exception as e:
                if e.code == 404:
                    return jsonify(result="[error : user not found]")
                elif e.code == 403:
                    return jsonify(result="[error : api limit reached, try again later]")
                else:
                    return jsonify(result="[error : " + str(e.code) + "]")

        # turn the api call data into json
        for i in data:
            jsondata.append(json.loads(i.read().decode('utf-8')))

        # get the stargazers counts from the json
        for call in jsondata:
            for repo in call:
                for k, v in repo.items():
                    if k == "stargazers_count" and v != 0:
                        repolist.append(v)

        # sometimes there are no stars :(
        if repolist == []:
            return jsonify(result="No stars found.")
        else:
            sortedlist = sorted(repolist)

            # calculate the h-index
            for item in sortedlist:
                remaininglist = len(sortedlist[sortedlist.index(item):])
                if remaininglist > item:
                    countlist.append(item)
                elif remaininglist == item:
                    countlist.append(item)
                    break
                else:
                    while remaininglist < item:
                        item -= 1
                    else:
                        countlist.append(item)
                        break

            # return the h-index value
            return jsonify(result=str(max(countlist)))

    else:
        return jsonify(result=form.errors['keywords'][0])

if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')
