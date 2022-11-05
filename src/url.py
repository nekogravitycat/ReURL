import os
import re
import json


table_file = "url_table.json"
table = {}


class Status:
	def __init__(self, ok: bool, detail: str = ""):
		self.ok: bool = ok
		self.detail: str = detail


def load_table():
	if not os.path.exists(table_file):
		f = open(table_file, "w+")
		f.close()

	with open(table_file, "r") as f:
		global table
		table = json.loads(f.read())


def dump_table():
	with open(table_file, "w+") as f:
		f.write(json.dumps(table))


reserved = ["login", "admin", "api"]


def url_exists(short):
	return table.get(short) is not None and short not in reserved


def is_legal(key):
	return re.match(r"^[\w-]+$", key) and key not in reserved


def add(orig, short):
	if not short or not orig:
		return Status(False, "empty orig or shorten")

	if not is_legal(short):
		return Status(False, "illegal shorten url")

	# adds https protocol if no protocol exists
	if not orig.startswith("https://") and not orig.startswith("http://"):
		orig = f"https://{orig}"

	table[short] = orig
	dump_table()
	return Status(True, "ok")


def delete(short: str):
	if not url_exists(short):
		return Status(False, "key does not exist")

	del table[short]
	dump_table()
	return Status(True, "ok")


load_table()
