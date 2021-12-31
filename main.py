import flask
from threading import Thread
from replit import db
import re

app = flask.Flask("")


def add(code: str, orig: str):
  if(code == "" or orig == ""):
    print("Empty input")
    return

  #adds https protocol if not exists
  if(not (orig.startswith("https://") or orig.startswith("http://"))):
    orig = f"https://{orig}"

  if(re.match(r"^[\w-]+$", code)):
    db[code] = orig
    print("Added successfully!")
  
  else:
    print("Key name is illegal")


def delete(code: str):
  if(code in db.keys()):
    del db[code]
    print("Deleted successfully!")
  
  else:
    print("Key does not exist")


@app.route("/")
def home():
  return flask.redirect("https://www.nekogc.com")


@app.route("/<url>")
def convert(url):
  if(url in db.keys()):
    return flask.redirect(db[url])
  else:
    flask.abort(404)


def run():
  app.run(host = '0.0.0.0', port = 8080)

t = Thread(target = run)
t.start()


while(True):
  command = input()

  if(command == "del-all"):
    print("Are you sure to delete all links?\n[Y/N]", end=": ")
    confirm = input()

    if(confirm == "y" or confirm == "Y"):
      for k in db.keys():
        del db[k]
    
    print("cancelled")
  
  elif(command == "list"):
    for k in db.keys():
      print(f"{k} : {db[k]}")

  elif(command == "add"):
    print("Please enter the shorten code:")
    code: str = input()
    print("Please enter the original url:")
    orig: str = input()
    
    add(code, orig)

  elif(command == "del"):
    print("Please enter the shorten code:")
    delete(input())

  print()