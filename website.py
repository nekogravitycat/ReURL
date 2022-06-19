from datetime import date, timedelta
import flask
import threading
import hashlib
import os
from replit import db
import core


app = flask.Flask("")


@app.route("/login", methods = ["POST", "GET"])
def login() -> str:
	#For GET method
	if(flask.request.method == "GET"):
		token: str = flask.request.cookies.get("token")

		if(not token):
			return flask.render_template("login.html")
		
		elif(token != os.environ["admin_token"]):
			return flask.render_template("login.html", wrong="1")
			
		return flask.redirect("/")

	#For POST method
	token = flask.request.form["token"]
	sha: str = hashlib.sha256(token.encode()).hexdigest()

	if(sha != os.environ["admin_token"]):
		return flask.render_template("login.html", wrong="1")
	
	elif(token):
		resp = flask.make_response(flask.redirect("/"))
		resp.set_cookie("token", value = sha, expires = (date.today()+timedelta(days=7)))
		return resp

	return flask.render_template("login.html", wrong="1")


@app.route("/", methods=["POST", "GET"])
def home():
	# for verifying users
	token: str = flask.request.cookies.get("token")
	if(not token):
		return flask.redirect("/login")
	elif(token != os.environ["admin_token"]):
		return flask.redirect("/login?w=1")
	
	# for GET method
	if(flask.request.method == "GET"):
		return flask.render_template("home.html")

	# for POST method
	destination: str = flask.request.form["destination"]
	shorten: str = flask.request.form["shorten"]

	operation = core.url.add(shorten, destination)
	
	if(operation.ok):
		shorten: str = f"https://url.nekogc.com/{shorten}"
		return flask.render_template("home.html", pop_title="OK!", pop_msg=f"Shorten URL: {shorten}", pop_type="ok")

	return flask.render_template("home.html", pop_title="ERROR", pop_msg=operation.detail, pop_type="error")


@app.route("/<url>")
def convert(url):
	if(url in db.keys()):
		return flask.redirect(db[url])
		
	else:
		flask.abort(404)


def run() -> None:
	app.run(host = "0.0.0.0", port = 8080)


def alive() -> None:
	t = threading.Thread(target = run)
	t.start()