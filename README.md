### @ copyleft genr8eofl @ gentoo IRC Jan 26 2023
#FastAPI - python - pymediawiki - gentoo project

_Description:_

_Dependencies:_
**uvicorn (ASGI server)**
Python:
**pip install fastapi pymediawiki**
    from fastapi import FastAPI, Form
    from typing import Union
    from mediawiki import MediaWiki 
    from pydantic import BaseModel

_Setup Instructions_:
Gentoo:
    emerge uvicorn pydantic 

_Run_:
 /usr/bin/env /usr/bin/python3.10 -m uvicorn --reload fastapi-mediawiki-gentoo:app 

_Endpoints_:

"http://127.0.0.1:8000/hello": "GET - Hello World"
"http://127.0.0.1:8000/wiki": "GET - Query Gentoo Wiki (Main Page)"
"http://127.0.0.1:8000/wiki/search/{page}": "GET - search Gentoo Wiki for {page}"
"http://127.0.0.1:8000/coursesform": "POST - course form (HTML form data)"
"http://127.0.0.1:8000/coursesjson": "POST - course form (JSON javascript)"
"http://127.0.0.1:8000/login": "POST - login w/ username password (DISABLED)"


VSCode recommended to use.
