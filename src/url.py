import os
import re
import json


table_file = "/app/data/url_table.json"
table = {}


class Status:
	def __init__(self, status: int, detail: str = ""):
		self.status: int = status  # 0=ok, 1=failed, 2:interrupted (override confirm)
		self.detail: str = detail


def load_table():
	if not os.path.exists(table_file):
		with open(table_file, "w+") as f:
			f.write(json.dumps({"admin": "https://t.gravitycat.tw/admin"}))

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


def is_loop(url):
	return "t.gravitycat.tw" in url


def add(orig, short, override=None):
	if not short or not orig:
		return Status(1, "empty orig or shorten")
	
	if is_loop(orig):
		return Status(1, "cannot shorten already shorten url")

	if not is_legal(short):
		return Status(1, "illegal shorten url")

	# adds https protocol if no protocol exists
	if not orig.startswith("https://") and not orig.startswith("http://"):
		orig = f"https://{orig}"

	if url_exists(short) and not override:
		return Status(2, f"back-half '{short}' already exists, pointing to '{table[short]}'")

	table[short] = orig
	dump_table()
	return Status(0, "ok")


def delete(short: str):
	if not url_exists(short):
		return Status(1, "key does not exist")

	del table[short]
	dump_table()
	return Status(0, "ok")


load_table()
