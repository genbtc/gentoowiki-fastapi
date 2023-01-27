from typing import Union
from fastapi import FastAPI
from mediawiki import MediaWiki

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

wikigentoo = MediaWiki(url='http://wiki.gentoo.org/api.php')

@app.get("/wiki")
def read_root():
    p = wikigentoo.page('Main Page')
    everything = {
        "title": p.title,
        "pageid": p.pageid,
        "links": p.links,
#        "content": p.content,
        "html": p.html,
        "images": p.images,
        "references": p.references,
        "categories": p.categories,
        "coordinates": p.coordinates,
        "redirects": p.redirects,
        "backlinks": p.backlinks,
        "langlinks": p.langlinks,
        "summary": p.summary,
#        "sections": p.sections,
        "logos": p.logos,
        "hatnotes": p.hatnotes,
    }
    #TODO ? I DONT KNOW
#ERROR: NOTE: mediawiki.exceptions.MediaWikiBaseException: Unable to extract page content; the TextExtracts extension must be installed
#https://pymediawiki.readthedocs.io/en/latest/_modules/mediawiki/mediawikipage.html?highlight=TextExtracts

    return everything;