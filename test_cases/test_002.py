import os
import shutil

import jsonpath
import pytest

from tools.updateData import UpdateData
from tools.sendRequest import SendRequest
from tools.operationExcel import xlrdOperationExcel


class TestCase():
    cases = xlrdOperationExcel('cases.xlsx')
    global depend_data
    depend_data = {"csrftoken": "", "cookies": ""}

    @pytest.mark.parametrize("case", cases)
    def test_case(self, case):
        print("用例名称：%s" % case[0])
        case_data = case[1]
        if case_data['is_run'] == "N":
            pytest.skip()
        case_data = UpdateData(case_data, depend_data)
        url = case_data['url']
        request_type = case_data['request_type']
        request_header = case_data['request_header']
        request_data = case_data['request_data']
        request_cookie = case_data["request_cookie"]
        res = SendRequest(url, request_type, request_data, request_header, request_cookie)
        if not res:
            raise Exception("请求异常")
        else:
            if res["csrftoken"]:
                depend_data["csrftoken"] = res["csrftoken"]
            if res["cookies"]:
                depend_data["cookies"] = res["cookies"]
            response_data = case_data["response_data"]
            if response_data:
                for key, value in response_data.items():
                    value = jsonpath.jsonpath(res, value)
                    if value:
                        depend_data[key] = value[0]
        response_assert = case_data["response_assert"]
        if response_assert:
            for key, value in response_assert.items():
                res_value = jsonpath.jsonpath(res, key)
                if res_value:
                    res_value = res_value[0]
                    if res_value != value:
                        raise ValueError("返回结果与预期结果不一致")
                else:
                    raise ValueError("返回结果与预期结果不一致")


if __name__ == '__main__':
    # if os.path.exists('../reports/allure/'):
    #     shutil.rmtree('../reports/allure/')
    # pytest.main(['--alluredir=../reports/allure/xml', "test_002.py"])
    # os.system('allure generate ../reports/allure/xml -o ../reports/allure/result')
    pytest.main(["-s", "-v", "test_002.py"])
