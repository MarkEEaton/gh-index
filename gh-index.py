import json
import sys
import urllib2
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("gh-index.html")

@app.route('/calculate')
def calculate():
	requestdata = request.args.get("a")
	data = urllib2.urlopen("https://api.github.com/users/%s/repos?per_page=100"\
	% requestdata)

	repolist = []
	countlist = []
	finallist = []
	readdata = data.read()
	jsondata = json.loads(readdata)

	for repo in jsondata:
	    for k, v in repo.iteritems():
	        if k == "stargazers_count":
	            repolist.append(v)

	if len(repolist) == 100:
	    sys.exit('You have more than 100 repositories. \
	This tool won\'t work correctly with that many repos.')


	def count(n):
	    count = 0
	    for item in repolist:
	        if item == 0:
	            pass
	        elif n >= item:
	            count += 1
	    countlist.append(count)


	for item in repolist:
	    count(item)

	d = dict(zip(repolist, countlist))

	for k, v in d.iteritems():
	    if k <= v:
	        finallist.append(k)

	return jsonify(result=str(max(finallist)))


if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1', debug=True)