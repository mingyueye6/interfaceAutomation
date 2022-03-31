import os

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
            response_data = case_data["response_data"]
            if response_data:
                for key, value in response_data.items():
                    value = jsonpath.jsonpath(res, value)
                    if value:
                        value = value[0]
                        if case_name in depend_data:
                            depend_data[case_name][key] = value
                        else:
                            depend_data[case_name] = {}
                            depend_data[case_name][key] = value
        response_assert = case_data["response_assert"]
        if response_assert:
            for key, value in response_assert.items():
                res_value = jsonpath.jsonpath(res, key)
                if res_value:
                    res_value = res_value[0]
                    if res_value == value:
                        pass
                    else:
                        raise ValueError("返回结果与预期结果不一致")
        print(depend_data)


if __name__ == '__main__':
    pytest.main(['-s', '-v', '--html=../reports/pytest-html/report.html'])
