import http.client
import requests
import json

# IP address text file path\to\file
txt_file = r"C:\Users\asutton\Downloads\geist_imd_ip.txt"
file = open(txt_file, "r")
for line in file.readlines():
    ip = line.strip()
    try:
        # url for existing 'facilities' user to log in and get info
        url = f'http://{ip}/api/auth/facilities'
        # json for POST request
        login_json = json.dumps({"cmd": "login",
                                 "data": {
                                     "password": "facpub"
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
                    "username": "techopsadmn",
                    "password": "$iemens5Techops1",
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
                    "username": "techopsadmn",
                    "authType": "md5",
                    "authPassword": "$iemens5Techops1",
                    "privType": "aes",
                    "privPassword": "$iemens5Secur320"
                }
            })
            # POST request to modify 'read' snmpv3 user
            r3 = requests.post(url3, data=snmp_json)
            # prints the ip address and responses for each request
            print(ip, r.json(), r2.json(), r3.json())
    except requests.exceptions.RequestException or http.client.RemoteDisconnected or json.decoder.JSONDecodeError:
        print("failed for IP: ", ip)
