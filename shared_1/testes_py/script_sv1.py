#!/usr/bin/python3

import requests
s=requests.Session()
for i in range(1,10000):

    try:
        r= s.get("http://192.168.10.2/sv1")
        print(r.text)
    except:
        print(str(i) + "- oops")
    
    

