import json
import sys
import urllib2

if len(sys.argv) != 2:
    sys.exit('Usage: python gh-index.py <username>')

data = urllib2.urlopen("https://api.github.com/users/%s/repos?per_page=100"
                       % sys.argv[1])

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

print "\n" + sys.argv[1] + "\'s stars:\n" + \
      str(sorted(repolist, reverse=True)) + "\n"


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

print sys.argv[1] + ", your gh-index is " + str(max(finallist)) + "\n"
