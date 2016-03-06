import json
import sys
import urllib2

if len(sys.argv) != 2:
    sys.exit('Usage: python gh-index.py <username>')

data = urllib2.urlopen("https://api.github.com/users/%s/repos" % sys.argv[1])

repolist = [] 
valueslist = [] 
readdata = data.read()
jsondata = json.loads(readdata)

for repo in jsondata:
    for k, v in repo.iteritems():
        if k == "stargazers_count":
            repolist.append(v)

print repolist

def hcount(n):
    hcountnum = 0
    for item in repolist:
        if n >= item:
            hcountnum += 1
            print "hcount added"
    return hcountnum

for item in repolist:
    itemcount = hcount(item)
    print "next item"
    valueslist.append(itemcount) 

print valueslist
#print sys.argv[1] + ", your gh-index is " + str(max(valueslist))
