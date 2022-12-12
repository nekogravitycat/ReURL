import flask
import string
import random
from src import url

app = flask.Flask("")


@app.route("/")
def root():
	return flask.redirect("/admin", code=301)


@app.route("/admin", methods=["POST", "GET"])
def admin():
	# for GET method
	if flask.request.method == "GET":
		return flask.render_template("create.html")

	# for POST method
	orig: str = flask.request.form.get("orig").strip()
	short: str = flask.request.form.get("short").strip()
	override: str = flask.request.form.get("override")

	# create a random 6-character-long back-half if not provided
	if not short:
		short = "".join(random.choices(string.ascii_uppercase, k=6))

	operation = url.add(orig, short, override)

	if operation.status == 0:
		short_url: str = f"t.gravitycat.tw/{short}"
		return flask.render_template("create.html", status="successful", detail=f"{short_url}")

	elif operation.status == 1:
		return flask.render_template("create.html", status="failed", detail=operation.detail)

	elif operation.status == 2:
		return flask.render_template(
			"create.html",
			status="interrupted",
			override="1",
			orig=orig,
			short=short,
			detail=operation.detail
		)

	return flask.abort(500, f"unknown operation status code: {operation.status}")


@app.route("/<short>")
def convert(short):
	if not url.url_exists(short):
		return flask.render_template("notfound.html")

	return flask.redirect(url.table[short])
