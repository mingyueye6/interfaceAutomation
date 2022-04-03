import os
import shutil
import logging
import jsonpath
import pytest

from tools.operationYaml import OperationYaml
from tools.updateData import UpdateData
from tools.sendRequest import SendRequest


class TestCase():
    cases = OperationYaml('cases.yaml')
    global depend_data
    depend_data = {}

    @pytest.mark.parametrize("case", cases)
    def test_case(self, case):
        case_name = case[0]
        if not case_name:
            pytest.skip()
        logging.info("用例名称：%s" % case_name)
        case_data = case[1]
        if case_data['is_run'] == "N":
            pytest.skip()
        case_data = UpdateData(case_data, depend_data)
        url = case_data['url']
        request_type = case_data['request_type']
        request_header = case_data['request_header']
        request_data = case_data['request_data']
        request_cookie = case_data["request_cookie"]
        if request_cookie == "Y":
            if not request_header:
                request_header = {}
            cookies_dic = depend_data["cookies"]
            cookies_list = []
            for key, value in cookies_dic.items():
                cookies_list.append(key + "=" + value)
            request_header["Cookie"] = "; ".join(cookies_list)
        res = SendRequest(url, request_type, request_data, request_header)
        logging.info(res)
        if not res:
            raise Exception("请求异常")
        else:
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
    if os.path.exists('../reports/pytest-html/'):
        shutil.rmtree('../reports/pytest-html/')
    pytest.main(['-s', '-v', "test_001.py", '--html=../reports/pytest-html/report.html'])
