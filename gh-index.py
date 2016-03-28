import json
import urllib2
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("gh-index.html")


@app.route('/calculate')
def calculate():
    requestdata = request.args.get("a")
    data1 = urllib2.urlopen(
        "https://api.github.com/users/%s/repos?per_page=100&page=1"
        % requestdata)
    data2 = urllib2.urlopen(
        "https://api.github.com/users/%s/repos?per_page=100&page=2"
        % requestdata)
    data3 = urllib2.urlopen(
        "https://api.github.com/users/%s/repos?per_page=100&page=3"
        % requestdata)

    repolist = []
    countlist = []
    readdata1 = data1.read()
    readdata2 = data2.read()
    readdata3 = data3.read()
    jsondata1 = json.loads(readdata1)
    jsondata2 = json.loads(readdata2)
    jsondata3 = json.loads(readdata3)
    jsondata = jsondata1 + jsondata2 + jsondata3

    for repo in jsondata:
        for k, v in repo.iteritems():
            if k == "stargazers_count" and v != 0:
                repolist.append(v)

    if repolist == []:
        return jsonify(result="No stars found.")
    else:
        sortedlist = sorted(repolist)

        print sortedlist
        for item in sortedlist:
            if len(sortedlist[sortedlist.index(item):]) >= item:
                countlist.append(item)

        print countlist
        return jsonify(result=str(max(countlist)))

if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1', debug=True)
