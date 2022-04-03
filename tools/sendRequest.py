import requests


def SendRequest(url, method="GET", data=None, headers=None):
    try:
        if method.upper() == "GET":
            res = requests.get(url=url, params=data, headers=headers)
        elif method.upper() == "POST":
            res = requests.post(url=url, data=data, headers=headers)
        elif method.upper() == "DELETE":
            res = requests.delete(url=url, data=data, headers=headers)
    except Exception as err:
        print(err)
        return None
    data = {}
    try:
        data = res.json()
    except Exception as err:
        pass
    try:
        cookies = {}
        cookie_str = res.request.headers.get('Cookie', '')
        if cookie_str:
            cookie_list = cookie_str.split(";")
            for cookie in cookie_list:
                key, value = cookie.strip().split("=")
                cookies[key] = value
        if not cookies:
            cookies = requests.utils.dict_from_cookiejar(res.cookies)
    except Exception as err:
        print(err)
    return {"cookies": cookies, "data": data}


if __name__ == '__main__':
    data = {"csrfmiddlewaretoken": "YNCCm2BX1S3lplxhaDWO90ynqBm9dRPB1CwZ1fG75czvoVuLuMzWGCAaP7rEDcmL",
            "next": "/userfavs/?format=json", "username": "test001", "password": "ceshi001", "submit": "Log in"}
    url = "http://49.235.168.69:8000/api-auth/login/"
    headers = {
        "Cookie": "csrftoken=YNCCm2BX1S3lplxhaDWO90ynqBm9dRPB1CwZ1fG75czvoVuLuMzWGCAaP7rEDcmL"
    }
    # data = SendRequest(url, "post", data=data, headers=headers)
    data = SendRequest("http://49.235.168.69:8000/api-auth/login/")
    print(data)
