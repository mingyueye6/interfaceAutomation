import os

import yaml


def OperationYaml(file_name="cases.yaml"):
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_path, 'datas', file_name)
    with open(file_path, encoding="utf-8") as f:
        data = f.read()
        data = yaml.safe_load(data)
        data_list = []
        for key, value in data.items():
            data_list.append([key, value])
        return data_list


if __name__ == '__main__':
    data = OperationYaml()
    print(data)
