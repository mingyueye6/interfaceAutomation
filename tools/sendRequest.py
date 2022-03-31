import requests


def SendRequest(url, method="GET", data=None, headers=None, cookies=None):
    try:
        if method.upper() == "GET":
            res = requests.get(url=url, params=data, headers=headers, cookies=cookies)
        elif method.upper() == "POST":
            res = requests.post(url=url, data=data, headers=headers, cookies=cookies)
        elif method.upper() == "DELETE":
            res = requests.delete(url=url, data=data, headers=headers, cookies=cookies)
    except:
        return None
    try:
        data = res.json()
    except:
        data = {}
    try:
        cookies = requests.utils.dict_from_cookiejar(res.cookies)
        cookie = res.request.headers.get('Cookie', '')
        if not cookie:
            cookies["cookies"] = res.cookies
        else:
            cookies["cookies"] = cookie
    except Exception as err:
        print(err)
        cookies = {"cookies":""}
    return {"cookies": cookies, "data": data}


if __name__ == '__main__':
    data = {"csrfmiddlewaretoken": "YNCCm2BX1S3lplxhaDWO90ynqBm9dRPB1CwZ1fG75czvoVuLuMzWGCAaP7rEDcmL",
            "next": "/userfavs/?format=json", "username": "test001", "password": "ceshi001", "submit": "Log in"}
    url = "http://49.235.168.69:8000/api-auth/login/"
    headers = {
        "Cookie": "csrftoken=YNCCm2BX1S3lplxhaDWO90ynqBm9dRPB1CwZ1fG75czvoVuLuMzWGCAaP7rEDcmL"
    }
    data = SendRequest(url, "post", data=data, headers=headers)
    print(data)
