import http.client
import requests
import json
import os
from py_dotenv import read_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
read_dotenv(dotenv_path)
# IP address text file path\to\file
txt_file = os.getenv('PATH_TO_TXT')
file = open(txt_file, "r")
for line in file.readlines():
    ip = line.strip()
    try:
        # url for existing 'facilities' user to log in and get info
        url = f'http://{ip}/api/auth/{os.getenv("ORIGINAL_USER")}'
        # json for POST request
        login_json = json.dumps({"cmd": "login",
                                 "data": {
                                     "password": os.getenv("ORIGINAL_PASS")
                                 }
                                 })
        # POST request to log in
        r = requests.post(url, data=login_json)
        response = r.json()
        retCode = response["retCode"]
        # checks if log in was successful
        if retCode != 0:
            # retcode 0 is success
            print(ip, "failed with retCode: ", retCode)
            pass
        else:
            # parse token from json response
            token = response["data"]["token"]
            # url for adding user
            url2 = f'http://{ip}/api/auth'
            # json for POST request
            add_user_json = json.dumps({
                "token": f"{token}",
                "cmd": "add",
                "data": {
                    "username": os.getenv('PDU_USER'),
                    "password": os.getenv('PDU_PASS'),
                    "enabled": True,
                    "admin": True
                }})
            # POST request to device to add user
            r2 = requests.post(url2, data=add_user_json)
            # url to modify the 'read' snmpv3 user
            url3 = f'http://{ip}/api/conf/snmp/user/0'
            # json for POST request
            snmp_json = snmp = json.dumps({
                "token": f"{token}",
                "cmd": "set",
                "data": {
                    "username": os.getenv('V3_USER'),
                    "authType": "md5",
                    "authPassword": os.getenv('V3_AUTH_PASS'),
                    "privType": "aes",
                    "privPassword": os.getenv('V3_PRIV_PASS')
                }
            })
            # POST request to modify 'read' snmpv3 user
            r3 = requests.post(url3, data=snmp_json)
            # prints the ip address and responses for each request
            print(ip, r.json(), r2.json(), r3.json())
    except requests.exceptions.RequestException or http.client.RemoteDisconnected or json.decoder.JSONDecodeError:
        print("failed for IP: ", ip)
