import jsonpath


def UpdateData(parmas_data, json_data):
    if not json_data:
        return parmas_data
    try:
        if isinstance(parmas_data, dict):
            for key, value in parmas_data.items():
                if isinstance(value, list):
                    value = UpdateData(value, json_data)
                    parmas_data[key] = value
                elif isinstance(value, dict):
                    value = UpdateData(value, json_data)
                    parmas_data[key] = value
                elif isinstance(value, str):
                    if "$." in value:
                        value_list = jsonpath.jsonpath(json_data, value)
                        if value_list:
                            parmas_data[key] = value_list[0]
        elif isinstance(parmas_data, list):
            for index, value in enumerate(parmas_data):
                if isinstance(value, dict):
                    value = UpdateData(value, json_data)
                    parmas_data[index] = value
                elif isinstance(value, list):
                    value = UpdateData(value, json_data)
                    parmas_data[index] = value
                elif isinstance(value, str):
                    if "$." in value:
                        value_list = jsonpath.jsonpath(json_data, value)
                        if value_list:
                            parmas_data[index] = value_list[0]
        elif isinstance(parmas_data, str):
            if "$." in parmas_data:
                value_list = jsonpath.jsonpath(json_data, parmas_data)
                if value_list:
                    parmas_data = value_list[0]
    except:
        pass
    return parmas_data


if __name__ == '__main__':
    parmas_data = {'login': {'username': 'test001', 'password': 'test001', 'data': {'code': '$.login.code'}},
                   'select': {'user': 0}}
    # parmas_data = "$.login.code"
    # parmas_data = ["a", {"code":"$.login.code"}]
    json_data = {'login': {'code': 200}}
    parmas_data = UpdateData(parmas_data, json_data)
    print(parmas_data)
