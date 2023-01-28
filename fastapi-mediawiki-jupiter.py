# @ copyleft genr8eofl @ gentoo IRC Jan 26 2023

from fastapi import FastAPI, Form
from typing import Union

app = FastAPI()

#Hello World: url = http://127.0.0.1:8000/
@app.get("/hello")
def read_root():
    return {"Hello": "World"}

#Path Parameters dummy example, can turn into search (info@ https://fastapi.tiangolo.com/tutorial/path-params/)
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

from mediawiki import MediaWiki

wikigentoo = MediaWiki(url='http://wiki.gentoo.org/api.php')

# Get Main Example
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
# url = http://127.0.0.1:8000/wiki/searchtest/xxxxxxx?q=SomeText #(Q unused yet)
@app.get("/wiki/searchtest/{page}")
def read_item(page: str, q: Union[str, None] = None):
    return {"page": page, "q": q}

# SEARCH:
# url = http://127.0.0.1:8000/wiki/search/Main%20Page?q=SomeText #(Q unused yet)
@app.get("/wiki/search/{page}")
def read_item(page: str, q: Union[str, None] = None):
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
    }
    return everything;    

from pydantic import BaseModel
 
# Our First Example Model
class CourseModel(BaseModel):
    name: str
    price: int
    author: Union[str, None] = None
    description: Union[str, None] = None
    internalData: Union[str, None] = None

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

from fastapi.responses import HTMLResponse
# /coursesform =  COURSES FORM (FormData / HTML)
# helper endpoint to call real endpoint /_courses
# generate a little HTML webpage form to send <form> data to our own server (same-origin)
# request body: name=NotBiberaoCertified&price=9001&author=someoneelse&description=notEmpty
#URL= @ http://127.0.0.1:8000/coursesform
@app.get("/coursesform", response_class=HTMLResponse)
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
#URL= @ http://127.0.0.1:8000/coursesjson
@app.get("/coursesjson", response_class=HTMLResponse)
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

@app.get("/")
def show_endpoints():
    return {"http://127.0.0.1:8000/hello": "GET - Hello World", 
            "http://127.0.0.1:8000/wiki": "GET - Query Gentoo Wiki (Main Page)",
            "http://127.0.0.1:8000/wiki/search/{page}": "GET - search Gentoo Wiki for {page}",
            "http://127.0.0.1:8000/coursesform": "POST - course form (HTML form data)",
            "http://127.0.0.1:8000/coursesjson": "POST - course form (JSON javascript)",
            "http://127.0.0.1:8000/login": "POST - login w/ username password (DISABLED)", 
    }    