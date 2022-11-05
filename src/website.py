import os
import flask
import string
import random
import hashlib
from datetime import datetime, timedelta
import src.url


app = flask.Flask("")


def verify(token):
	if not token:
		return flask.redirect("/login")

	elif token != os.environ["admin_token"]:
		return flask.redirect("/login?w=1")

	return None


@app.route("/login")
def login():
	# for GET method
	if flask.request.method == "GET":
		token: str = flask.request.cookies.get("token")

		if not token:
			return flask.render_template("login.html")

		elif token != os.environ["token_sha"]:
			return flask.render_template("login.html", wrong="1")

		return flask.redirect("/")

	# for POST method
	token = flask.request.form["token"]
	sha: str = hashlib.sha256(token.encode()).hexdigest()

	if sha != os.environ["token_sha"]:
		return flask.render_template("login.html", wrong="1")

	elif token:
		resp = flask.make_response(flask.redirect("/"))
		resp.set_cookie("token", value=sha, expires=(datetime.now()+timedelta(days=7)))
		return resp

	return flask.render_template("login.html", wrong="1")


@app.route("/")
def root():
	# verify user
	token = flask.request.cookies.get("token")
	auth = verify(token)

	if auth is not None:
		return auth

	# for GET method
	if flask.request.method == "GET":
		return flask.render_template("create.html")

	# for POST method
	orig: str = flask.request.form["orig"]
	short: str = flask.request.form["short"]

	# create a random 6-character-long back-half if not provided
	if not short:
		short = "".join(random.choices(string.ascii_uppercase, k=6))

	operation = url.add(orig, short)

	if operation.ok:
		short_url: str = f"t.nekogc.com/{short}"
		return flask.render_template("create.html", status="successful", detail=f"{short_url}")

	return flask.render_template("create.html", status="failed", detail=operation.detail)


@app.route("/<short>")
def convert(short):
	if url.url_exists(short):
		return flask.abort(404)

	return flask.redirect(url.table[short])
