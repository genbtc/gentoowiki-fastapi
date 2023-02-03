# @ copyleft genr8eofl @ gentoo IRC Jan 26 2023

from fastapi import FastAPI, Form
from typing import Union
import mimetypes
mimetypes.init()

app = FastAPI()

#SHOW ENDPOINTS (try to keep updated manually.)
@app.get("/")
def show_endpoints():
    return {"http://127.0.0.1:8448/hello": "GET - Hello World!",
            "http://127.0.0.1:8448/wiki": "GET - Show Gentoo Wiki Main Page",
            "http://127.0.0.1:8448/wiki/search/{page}": "GET - Search Gentoo Wiki for {page}",
            "http://127.0.0.1:8448/coursesform": "POST - course form (by HTML form data)",
            "http://127.0.0.1:8448/coursesjson": "POST - course form (by JSON javascript)",
            "http://127.0.0.1:8448/login": "POST - login w/ username password (DISABLED)",
            "http://127.0.0.1:8448/proc/cpuinfo": "GET - CPUInfo procfiles",
            "http://127.0.0.1:8448/github/{repoowner}/{reponame}/desc": "GET - Github Description Title for any repo",
            "http://127.0.0.1:8448/equery/g/{atom}": "GET - Gentoo query package dependencies",
            "http://127.0.0.1:8448/equery/u/{atom}": "GET - Gentoo query package USE Flags",
    }

#Hello World!: url = http://127.0.0.1:8448/hello
@app.get("/hello")
def read_root():
    return {"Hello": "World!"}

#Path Parameters dummy example, can turn into search (info@ https://fastapi.tiangolo.com/tutorial/path-params/)
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str|None = None):
    return {"item_id": item_id, "q": q}

from mediawiki import MediaWiki

wikigentoo = MediaWiki(url='http://wiki.gentoo.org/api.php')

#Get Main Page of Wiki
@app.get("/wiki")
def read_root():
    p = wikigentoo.page('Main Page')
    everything = {
        "title": p.title,
        "pageid": p.pageid,
        "summary": p.summary,
        "links": p.links,
        "images": p.images,
        "references": p.references,
        "categories": p.categories,
        "coordinates": p.coordinates,
        "redirects": p.redirects,
        "backlinks": p.backlinks,
        "langlinks": p.langlinks,
        "logos": p.logos,
        "hatnotes": p.hatnotes,
        "html": p.html,
#        "content": p.content,        #TODO
#        "sections": p.sections,      #see error note
    }
    return everything;
#ERROR: NOTE: mediawiki.exceptions.MediaWikiBaseException: Unable to extract page content; the TextExtracts extension must be installed
#https://pymediawiki.readthedocs.io/en/latest/_modules/mediawiki/mediawikipage.html?highlight=TextExtracts
#https://www.mediawiki.org/wiki/Extension:TextExtracts we think it requires the extension on the gentoo server. :/

# SEARCHTEST:
# url = http://127.0.0.1:8448/wiki/searchtest/xxxxxxx?q=SomeText #(Q unused yet)
@app.get("/wiki/searchtest/{page}")
def read_item(page: str, q: str|None = None):
    return {"page": page, "q": q}

# SEARCH:
# url = http://127.0.0.1:8448/wiki/search/Main%20Page?q=SomeText #(Q unused yet)
@app.get("/wiki/search/{page}")
def read_item(page: str, q: str|None = None):
#check database if it exists first
    if (page in db.data['wiki']):
        print("[200] /wiki/search/"+page+" FOUND in db")
        return db.data['wiki'][page]
#if not, request from gentoo wiki remote url
    #take page and call pymediawiki
    p = wikigentoo.page(page)
    everything = {
        "title": p.title,
        "pageid": p.pageid,
        "summary": p.summary,
        "links": p.links,
        "images": p.images,
        "references": p.references,
        "categories": p.categories,
        "coordinates": p.coordinates,
        "redirects": p.redirects,
        "backlinks": p.backlinks,
        "langlinks": p.langlinks,
        "logos": p.logos,
        "hatnotes": p.hatnotes,
        "html": p.html,
        "wikitext": p.wikitext,
    }
    #Add result and Write to database
    db.data['wiki'].append({page:everything})
    db.write()

    return everything;

from pydantic import BaseModel

# Our First Example Model
class CourseModel(BaseModel):
    name: str
    price: int
    author: str|None = None
    description: str|None = None
    internalData: str|None = None

# Pydantic Model can be directly populated by HTTP POST data, but the request body has to be given in JSON
#NOTE:can not reach POST method directly via browser URL. error: ""GET /_coursesPYDANTICJSON HTTP/1.1" 405 Method Not Allowed"
# A HTML <form><input> _can_ be sent w/ POST, but requires clientside JS to convert the form data to JSON, thus non conducive to simple examples
#DONE: See /coursesjson below to hit this internal endpoint
@app.post("/_coursesPYDANTICJSON")
def create_course(course: CourseModel):
    course.internalData = "This super secret data came from inside the server";
    return { "course": course}

#lol dont do this for real, but
global STOREDASSWORD
#Example simple login w/ HTTP POST request, which Converts the <form> data for us:
@app.post("/login/")
async def login(username: str = Form(), password: str = Form()):
    STOREDASSWORD = password
    return { "username": username}

#Model object has to be explicitly constructed out of individual = Form() parameters
#TODO: find smaller way to code it, reduce the redundancy during non-JSON <form> creation
@app.post("/_courses")
def create_course(name: str = Form(),
                  price: int = Form(),
                  author: str = Form(),
                  description: str= Form() ):
    course = CourseModel(
                  name = name,
                  price = price,
                  author = author,
                  description = description )
    return { "course": course}

from fastapi.responses import Response,HTMLResponse
# /coursesform =  COURSES FORM (FormData / HTML)
# helper endpoint to call real endpoint /_courses
# generate a little HTML webpage form to send <form> data to our own server (same-origin)
# request body: name=NotBiberaoCertified&price=9001&author=someoneelse&description=notEmpty
#URL= @ http://127.0.0.1:8448/coursesform
@app.get("/coursesform")
def courses_form():
    htmlpage="""<html><head><title>Course List Form (FormData)</title></head>
<form action="/_courses" method="POST">
<!-- generates HTML Form Data, not JSON -->
  <input type="text"   name="name"        value="NotBiberaoCertified" />
  <input type="number" name="price"       value="9001" />
  <input type="text"   name="author"      value="someoneelse" />
  <input type="text"   name="description" value="notEmpty" />
  <input type="submit" />
</form>
</html>
"""
#This was required because the default response is JSON
    return HTMLResponse(content=htmlpage, status_code=200)


# /coursesjson = COURSES FORM (JSON / Javascript)
# helper endpoint to call fetch() on real endpoint /_coursesPYDANTICJSON
# Serve the user up this combination of JS + HTML to do it.
# javascript Crafts request JSON from internal hardcoded data, (or data from wherever),
# Prints data back in browser window when submit button is pushed
#URL= @ http://127.0.0.1:8448/coursesjson
@app.get("/coursesjson")
def courses_json():
    htmlpage="""<html><head><title>Course List Form (JSON)</title></head>
    <body> You have reached the Biberao hotline. Automatically crafting a manual request.
    <br> push Submit Query to talk to server.
    <a href="view-source:coursesjson"> (view source)</a> or Console. </body>
    <script id="courses">
      <!-- easiest to just craft the request manually. note `{body}` -->
      craftRequest = {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: `{
            "name": "genr8Certified",
            "price": 9002,
            "author": "me",
            "description": "thebestthingever"
        }`,
      };
      <!-- sends server request w/ fetch(), async, await, gets a response & dumps the JSON data to console & HTML screen -->
      async function callResponse() {
        response = await fetch("/_coursesPYDANTICJSON", craftRequest );
        response.json().then(data => {
          if('course' in data) {
            r = data["course"];
            console.log(r);
            document.body.innerHTML+="<p><h1>Server Response Printout</h1><p>";
            document.body.innerHTML+="<h1>Name: "+r["name"]+"</h1>";
            document.body.innerHTML+="<h2>Price: "+r["price"]+"</h2>";
            document.body.innerHTML+="<h2>Author: "+r["author"]+"</h2>";
            document.body.innerHTML+="<h3>Description: "+r["description"]+"</h3>";
            document.body.innerHTML+="<h3>SuperSecretDataWeDidntSeeUntilNow: "+r["internalData"]+"</h3>";
          }
        });
      }
    </script>
    <!-- start server request on button click -->
    <input type="submit" onclick="callResponse()"/>
    </html>
    """
    #    callResponse();
    return HTMLResponse(content=htmlpage, status_code=200)

#--------------------------- DATABASE.JSON ------------------------

import json
#https://pythonawesome.com/tiny-local-json-database-for-python/
import os
from os import path
from pylowdb import (
    Low,
    JSONFile,
)
# Use JSON file for storage
dbfile = path.join(os.getcwd(), 'database.json')
dbadapter = JSONFile(dbfile)
db = Low(dbadapter)

# Read data from JSON file, this will set db.data content
db.read()

# If file.json doesn't exist, db.data will be None
# Set default data
# db.data = db.data or { 'wiki': [] }
#INITIALIZE DATABASE
db.data = db.data or { 'wiki': [] }

# Create and query items using plain Python
#db.data['wiki'].append('hello world')
#db.data['wiki'][0]

# You can also use this syntax if you prefer
#wiki = db.data['wiki']
#wiki.append('hello world')

# Write db.data content to db.json
#db.write()

import subprocess
import sys

# show how use python subprocess.run to run any system command and return the data
# CPUINFO proc file
@app.get("/proc/cpuinfo")
def proc_cpuinfo():
    print("cat /proc/cpuinfo")
    result = subprocess.run(
        ["cat","/proc/cpuinfo"], capture_output=True, text=True
    )
    resultstr = result.stdout[:100000]    #cap to ~100KB to make sure no DoS
    print("stdout cpuinfo:", resultstr)
    # formatting as <pre> looks better than blank page
    return HTMLResponse(content="<pre>"+resultstr+"</pre>", status_code=200)

#Use a pre-determined list of files we can query in /proc and return the data
import allowedprocfiles
# PROCFILES (ALLLL) - well, most. allowlisted in allowedprocfiles.py. still risky.
@app.get("/proc/{procfile}")
def proc_cpuinfo(procfile: str, q: str|None = None):
    if (len(procfile)>50): return { "Error": "Blocked" }
    print("cat /proc/"+procfile)
    result = subprocess.run(
        ["cat","/proc/"+procfile], capture_output=True, text=True
    )
    resultstr = result.stdout[:100000]
    print("stdout "+procfile, resultstr)
    return HTMLResponse(content="<pre>"+resultstr+"</pre>", status_code=200)

#from my https://gist.github.com/genbtc/57fdc34d1bae507ab3815edb2dab4883
#!/usr/bin/env python3
#Copyright 2023 - genr8eofl @IRC/gentoo
# github-beautiful.py - fetch GitHub repo "Description" (for many links at once)
#       Makes 1 HTTPS connection per line, retreives the HTML page and parses it for <Title>
import requests
from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError
from bs4 import BeautifulSoup
import sys

# GITHUB show Description
@app.get("/github/{repoowner}/{reponame}/desc")
def github_repo_desc(repoowner: str, reponame: str, q: str|None = None):
    urlprefix="https://github.com/"
    repo = repoowner + "/" + reponame
    #Usage: Takes 1 argument, a filename containing github repos
    # internet connection to github
    try:
        page = requests.get(urlprefix + repo)
    except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError) as e:
        return {"Error": e }
    # parse HTML, find <Title> tag
    soup = BeautifulSoup(page.text, 'html.parser')
    title = soup.find('title')
    # output
    if title:
        print(title.string)
        return {"description": { repo: title.string} }
    else:
        print("404_NOT_FOUND - ", repo)
        return {"Error": "404 GitHub Repo Not Found" }
    # if line is empty, EOF is reached, done, end loop.
    if not repo:
        return {"Done": "" }

# EQUERY G - Use gentoo's equery to return a list of dependency_Graph for a package
@app.get("/equery/g/{atom}")
async def equery_g(atom: str):
    print("equery g "+atom)
    result = subprocess.run(
        ["equery","depgraph","-U",atom], capture_output=True, text=True
    )
    resultstr = result.stdout[:100000]    #cap to ~100KB
    return HTMLResponse(defaultstatichtmlpage+resultstr+htmlend, media_type='text/html')

#Show how to use the static files system.
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")
# created a /static directory
# and put Sakura.css (small CSS layout) in it.
defaultstatichtmlpage="""<!DOCTYPE html>
<html><head><title>FastAPI</title>
<link rel="stylesheet" href="/static/sakura.css">
</head>
<body><pre>
"""
htmlend="</pre>200</body></html>"
#This HTML file would probably rather also be included as a template file

#Show how to use the jinja templating system
from fastapi import Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

# EQUERY U - Use gentoo's equery to return a list of USE Flags for a package
@app.get("/equery/u/{atom}")
async def equery_u(request: Request, atom: str, response_class=HTMLResponse):
    print("equery u "+atom)
    result = subprocess.run(
        ["equery","uses","-i",atom], capture_output=True, text=True
    )
    resultstr = result.stdout[:100000]
    #these request params are mandatory, and " {{ pre }} " is inside the premade .html file to populate it
    return templates.TemplateResponse("layout.html", {"request": request, "pre": resultstr})

#use this for password keyfile encryption later
import unlock_api_key
import encrypt_api_key

#probably best to start using a main function
def main(prog_name, *argv):
	print("Not implemented. launch w. uvicorn to run")

if __name__ == '__main__':
    sys.exit(main(*sys.argv))
