""" gh-index """
import requests
from flask import Flask, render_template, jsonify, request, url_for, redirect
from wtforms import Form, StringField, validators

app = Flask(__name__)


class SearchForm(Form):
    """ set up wtforms class """

    keywords = StringField(
        "query",
        [
            validators.Length(max=30, message="[error : too many characters]."),
            validators.Regexp(
                r"^[-a-zA-Z0-9]*$",
                message="[error : invalid characters. Use only A-Z,\
                        0-9, and hyphen]."
            ),
            validators.DataRequired(message="[error : you must type something]."),
        ],
    )


@app.after_request
def add_security_headers(resp):
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["X-Frame-Options"] = "SAMEORIGIN"
    resp.headers["X-XSS-Protection"] = "1; mode=block"
    resp.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    resp.headers["Content-Security-Policy"] = "script-src 'self'; style-src 'self'; connect-src 'self'; default-src 'none'"
    return resp


# load the html page
@app.route("/")
def index():
    """ load the index page """
    return render_template("gh-index.html")


@app.route("/calculate")
def calculate():
    """ do the calculations and return jsonified data """

    # create some empty lists
    data = []
    repolist = []
    countlist = []
    star_count = 0

    # take the input and validate it
    user = request.args.get("a")
    form = SearchForm(keywords=user)
    if form.validate():

        # make the api call
        # the api breaks results into pages. iterate through pages
        def try_append(resp):
            if resp.status_code == 200:
                data.append(resp.json())
                return
            elif resp.status_code == 403:
                return jsonify(
                    result="[error : api limit reached, try again later].", count=0
                )
            elif resp.status_code == 404:
                return jsonify(result="[error : user not found].", count=0)
            else:
                return jsonify(result="[error : " + str(resp.status_code) + "].", count=0)

        resp = requests.get("https://api.github.com/users/" + user + "/repos?per_page=100&page=1") 
        result = try_append(resp)
        while resp.links.get('next'):
            resp = requests.get(resp.links['next']['url'])
            result = try_append(resp)

        # if there is an error, return it
        if result:
            return result

        # get the stargazers counts from the json
        for call in data:
            for repo in call:
                for k, v in repo.items():
                    if k == "stargazers_count" and v != 0:
                        star_count += int(v)
                        repolist.append(v)

        # sometimes there are no stars :(
        if repolist == []:
            return jsonify(result="No stars found.")
        else:
            sortedlist = sorted(repolist)

            # calculate the h-index
            for item in sortedlist:
                remaininglist = len(sortedlist[sortedlist.index(item) :])
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
            return jsonify(result=str(max(countlist)), count=str(star_count))

    else:
        return jsonify(result=form.errors["keywords"][0])


if __name__ == "__main__":
    app.run(port=8000, host="127.0.0.1")
