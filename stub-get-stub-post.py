#from old project, stub requests sender helper utilities
import httplib, hmac, copy, base64, urllib2, ssl
def _send_get(self, url, payload={}):
    try:
        body = urllib.parse.urlencode(payload)
        conn = HTTPConn(config['host'], config['data_port'])
        conn.request("GET", url, body)
        resp = conn.getresponse()
        s = resp.read()
        conn.close()
        return json.loads(s, object_hook=json_ascii.decode_dict)
    except Exception as e:
        print("General Error: %s" % e)
#not suitable for general use yet, change generic api headers
#relies on _key, _secret, _passphrase
def _send_post(self, host, port, endpoint, headers={}, payload={}):
    try:
        payload = copy.copy(payload) # avoid modifying the original dict
        payload['nonce'] = int(time.time()*1e6) # add a nonce
        body = urllib.parse.urlencode(payload)
        sig = hmac.new(base64.b64decode(self._secret), body, hashlib.sha512).digest()
        sig_b64 = base64.b64encode(sig)
        headers = {
            'generic-key': self._key,
            'generic-sign': sig_b64,
            'generic-passphrase': self._passphrase,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': len(body)
        }
        with HTTPConn(host, port) as conn:
            conn.request("POST", endpoint, body, headers)
            resp = conn.getresponse()
            s = resp.read()
        return json.loads(s, object_hook=json_ascii.decode_dict)
    #error checking code itself was not checked for errors
    except urllib2.HTTPError as e:
        #HTTP Error ie: 500/502/503 etc
        print 'HTTP Error %s: %s' % (e.code, e.msg)
        print "URL: %s" % (e.filename)
        if e.fp:
            datastring = e.fp.read()
            if "error" in datastring:
                print("Error: %s" % datastring)
    except urllib2.URLError as e:
        print("URL Error:", e)
    except ssl.SSLError as e:
        print("SSL Error: %s." % e)  #Read error timeout. (Removed timeout variable)
    except Exception as e:
        print("General Error: %s" % e)

