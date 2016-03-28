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
	data1 = urllib2.urlopen("https://api.github.com/users/%s/repos?per_page=100&page=1"\
	% requestdata)
	data2 = urllib2.urlopen("https://api.github.com/users/%s/repos?per_page=100&page=2"\
	% requestdata)
	data3 = urllib2.urlopen("https://api.github.com/users/%s/repos?per_page=100&page=3"\
	% requestdata)

	repolist = []
	countlist = []
	finallist = []
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

#	if len(repolist) == 100:
#	    sys.exit('You have more than 100 repositories. \
#	This tool won\'t work correctly with that many repos.')


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

	print countlist
	print repolist

	d = dict(zip(repolist, countlist))
	print d

	for k, v in d.iteritems():
	    if k <= v:
	        finallist.append(k)

	return jsonify(result=str(max(finallist)))


if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1', debug=True)