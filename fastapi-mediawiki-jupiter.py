from typing import Union
from fastapi import FastAPI
from mediawiki import MediaWiki

app = FastAPI()

#Hello World: url = http://127.0.0.1:8000/
@app.get("/")
def read_root():
    return {"Hello": "World"}

#Path Parameters dummy example, can turn into search (info@ https://fastapi.tiangolo.com/tutorial/path-params/)
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

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
#        "content": p.content,        
#        "sections": p.sections,
    }
    return everything;    
    #TODO
#ERROR: NOTE: mediawiki.exceptions.MediaWikiBaseException: Unable to extract page content; the TextExtracts extension must be installed
#https://pymediawiki.readthedocs.io/en/latest/_modules/mediawiki/mediawikipage.html?highlight=TextExtracts
#https://www.mediawiki.org/wiki/Extension:TextExtracts we think it requires the extension on the gentoo server. :/

# SEARCHTEST:
# url = http://127.0.0.1:8000/wiki/searchtest/xxxxxxx?q=SomeText
@app.get("/wiki/searchtest/{page}")
def read_item(page: str, q: Union[str, None] = None):
    return {"page": page, "q": q}

# SEARCH:
# url = http://127.0.0.1:8000/wiki/search/Main%20Page?q=SomeText
@app.get("/wiki/search/{page}")
def read_item(page: str, q: Union[str, None] = None):
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
