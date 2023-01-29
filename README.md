#### @ copyleft genr8eofl @ gentoo IRC Jan 26 2023
# FastAPI - python - pymediawiki - gentoo project

_Description:_

#### Making a REST API for microservices and sending messages between servers

_Setup Instructions_:

    pip install --user fastapi pymediawiki
    emerge uvicorn  #(Gentoo)

_System Dependencies:_

**uvicorn (ASGI server)**

**Python imports**:
fastapi pymediawiki pydantic

    from fastapi import FastAPI, Form
    from typing import Union
    from mediawiki import MediaWiki 
    from pydantic import BaseModel


_Run_:

 ``/usr/bin/env /usr/bin/python3.10 -m uvicorn --reload fastapi-mediawiki-gentoo:app ``

_Endpoints_:

    "http://127.0.0.1:8000/hello": "GET - Hello World"
    "http://127.0.0.1:8000/wiki": "GET - Query Gentoo Wiki (Main Page)"
    "http://127.0.0.1:8000/wiki/search/{page}": "GET - search Gentoo Wiki for {page}"
    "http://127.0.0.1:8000/coursesform": "POST - course form (HTML form data)"
    "http://127.0.0.1:8000/coursesjson": "POST - course form (JSON javascript)"
    "http://127.0.0.1:8000/login": "POST - login w/ username password (DISABLED)"


*VSCode* recommended to use, launch.json included.


_Python VENV_:

The following command will install a set of packages from file requirements.txt. (freeze'd)

``$ pip install -r requirements.txt``

or

    $ pip install fastapi pymediawiki
    Requirement already satisfied: fastapi in ./lib/python3.10/site-packages (0.89.1)
    Requirement already satisfied: pymediawiki in ./lib/python3.10/site-packages (0.7.2)
    Requirement already satisfied: starlette==0.22.0 in ./lib/python3.10/site-packages (from fastapi) (0.22.0)
    Requirement already satisfied: pydantic!=1.7,!=1.7.1,!=1.7.2,!=1.7.3,!=1.8,!=1.8.1,<2.0.0,>=1.6.2 in ./lib/python3.10/site-packages (from fastapi) (1.10.4)
    Requirement already satisfied: anyio<5,>=3.4.0 in ./lib/python3.10/site-packages (from starlette==0.22.0->fastapi) (3.6.2)
    Requirement already satisfied: requests<3.0.0,>=2.0.0 in ./lib/python3.10/site-packages (from pymediawiki) (2.28.2)
    Requirement already satisfied: beautifulsoup4 in ./lib/python3.10/site-packages (from pymediawiki) (4.11.1)
    Requirement already satisfied: typing-extensions>=4.2.0 in ./lib/python3.10/site-packages (from pydantic!=1.7,!=1.7.1,!=1.7.2,!=1.7.3,!=1.8,!=1.8.1,<2.0.0,>=1.6.2->fastapi) (4.4.0)
    Requirement already satisfied: charset-normalizer<4,>=2 in ./lib/python3.10/site-packages (from requests<3.0.0,>=2.0.0->pymediawiki) (3.0.1)
    Requirement already satisfied: urllib3<1.27,>=1.21.1 in ./lib/python3.10/site-packages (from requests<3.0.0,>=2.0.0->pymediawiki) (1.26.14)
    Requirement already satisfied: idna<4,>=2.5 in ./lib/python3.10/site-packages (from requests<3.0.0,>=2.0.0->pymediawiki) (3.4)
    Requirement already satisfied: certifi>=2017.4.17 in ./lib/python3.10/site-packages (from requests<3.0.0,>=2.0.0->pymediawiki) (2022.12.7)
    Requirement already satisfied: soupsieve>1.2 in ./lib/python3.10/site-packages (from beautifulsoup4->pymediawiki) (2.3.2.post1)
    Requirement already satisfied: sniffio>=1.1 in ./lib/python3.10/site-packages (from anyio<5,>=3.4.0->starlette==0.22.0->fastapi) (1.3.0)

    (or the deps for which can be gotten from emerge, FIRST )    
    emerge beautifulsoup4 requests charset-normalizer certifi idna urllib3 soupsieve #(PyMediaWiki)
    emerge starlette pydantic anyio typing-extensions idna sniffio                   #(FastAPI)
