import json
import re
import urllib2
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)


# load the html page
@app.route('/')
def index():
    return render_template("gh-index.html")


@app.route('/calculate')
def calculate():

    # create some empty lists
    data = []
    repolist = []
    jsondata = []
    countlist = []

    # take the input and validate it
    user = request.args.get("a")
    if len(user) > 30:
        return jsonify(result="[error : too many characters]")
    elif re.compile(r'[^a-zA-Z0-9]').search(user):
        return jsonify(result="[error : invalid characters \
                               - use only A-Z and 0-9]")
    else:
        pass

    # make the api call
    # the api breaks results into pages. iterate through pages
    for i in range(1, 4):
        try:
            data.append(urllib2.urlopen(
                "https://api.github.com/users/{}/repos?per_page=100&page={}"
                .format(user, i)))
        except Exception, e:
            if e.code == 404:
                return jsonify(result="[error : user not found]")
            elif e.code == 403:
                return jsonify(result="[error : api limit reached, try again later]")
            else:
                return jsonify(result="[error : " + str(e.code) + "]")

    # turn the api call data into json
    for i in data:
        jsondata.append(json.loads(i.read()))

    # get the stargazers counts from the json
    for call in jsondata:
        for repo in call:
            for k, v in repo.iteritems():
                if k == "stargazers_count" and v != 0:
                    repolist.append(v)

    # sometimes there are no stars :(
    if repolist == []:
        return jsonify(result="No stars found.")
    else:
        sortedlist = sorted(repolist)

        # calculate the h-index
        print sortedlist
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
        print countlist
        return jsonify(result=str(max(countlist)))

if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')
