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
	
	def add(dest: str, orig: str) -> str:
		if(not dest or not orig):
			return status(False, "empty input")
	
		#adds https protocol if not exists
		if(not orig.startswith("https://") and not orig.startswith("http://")):
			orig = f"https://{orig}"
	
		if(url.is_legal(dest)):
			db[dest] = orig
			return status(True, "ok")
		
		else:
			return status(False, "illegal key name")	
	
	def delete(code: str):
		if(code in db.keys()):
			del db[code]
			return status(True, "ok")
		
		else:
			return status(False, "key does not exist")