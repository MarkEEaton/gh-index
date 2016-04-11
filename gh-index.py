import json
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

    # take the input from the form and make the api call
    # the api breaks results into pages. iterate through pages
    requestdata = request.args.get("a")
    for i in range(1, 3):
        data.append(urllib2.urlopen(
                    "https://api.github.com/users/{}/repos?per_page=100&page={}"
                    .format(requestdata, i)))

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
    app.run(port=8000, host='127.0.0.1', debug=True)
