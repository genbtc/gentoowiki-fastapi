from typing import Union
from fastapi import FastAPI, Form

app = FastAPI()

#Hello World: url = http://127.0.0.1:8000/
@app.get("/")
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
class Course(BaseModel):
    name: str
    price: int
    author: Union[str, None] = None
    description: Union[str, None] = None    

#Example login w/ HTTP POST request:
@app.post("/login/")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}

#can not reach directly via browser URL. 
@app.post("/courses")
def create_course(name: str = Form(), 
                 price: int = Form(),
                 author: str = Form(),
                 description: str= Form() ):
    course = Course( name=name,
                     price=price,
                     author=author,
                     description=description )
    return { "course": course}

from fastapi.responses import HTMLResponse

#URL= @ http://127.0.0.1:8000/coursesform
# generate a little HTML webpage to send form data to our own server, same-origin
# request payload: name=BiberaoCertified&price=9001&author=someoneelse&description=thebestthingever
@app.get("/coursesform", response_class=HTMLResponse)
def courses_form():
    htmlpage="""<html><head><title>Course List Form</title></head>
<form action="/courses" method="POST">
  <input type="text" name="name" value="BiberaoCertified" />
  <input type="number" name="price" value="9001" />
  <input type="text" name="author" value="someoneelse" />
  <input type="text" name="description" value="thebestthingever" />
  <input type="submit" />
</form>
</html>
"""
    return HTMLResponse(content=htmlpage, status_code=200)

