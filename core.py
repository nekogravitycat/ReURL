from replit import db
import re


class status:
	def __init__(self, ok: bool, detail: str = ""):
		self.ok: bool = ok
		self.detail: str = detail


class url:
	def is_legal(key: str) -> bool:
		illeagal: list = ["login", "utr"]
		return re.match(r"^[\w-]+$", key) and not key in illeagal

	
	def add(shorten: str, orig: str) -> str:
		if(not shorten or not orig):
			return status(False, "empty orig or shorten")

		if(not url.is_legal(shorten)):
			return status(False, "illegal shorten url")
	
		#adds https protocol if not exists
		if(not orig.startswith("https://") and not orig.startswith("http://")):
			orig = f"https://{orig}"

		db[shorten] = orig
		return status(True, "ok")

	
	def delete(code: str):
		if(not code in db.keys()):
			return status(False, "key does not exist")
			
		del db[code]
		return status(True, "ok")