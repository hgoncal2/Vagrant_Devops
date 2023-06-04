#!/usr/bin/python3

import requests
s=requests.Session()
for i in range(1,1000):

    try:
        r= s.get("http://192.168.10.2/")
        print(r.text)
    except:
        print(str(i) + "- oops")
    
    

