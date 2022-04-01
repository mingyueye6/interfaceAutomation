### 1、生成项目依赖包：
```
pip install pipreqs
pipreqs ./ --encoding=utf-8 --force
```
### 2、pytest-html生成测试报告
```
pip install pytest-html
pytest --html=./reports/report.html

# 设置启动脚本,运行文件时通过python运行启动脚本
# pytest.main(['-s', '-v', '--html=./reports/reports.html'])
```
### 3、allure生成测试报告
#### 1、安装java，配置环境变量
下载并安装jdk1.8
#### 2、下载allure，配置环境变量
下载allure，解压缩，将allure的bin目录添加到环境变量中
#### 3、生成测试报告
```
1、安排allure模块
pip install allure-pytest
2、生成测试数据
pytest --alluredir ./report/allure
3、在线预览
allure serve ./report/allure
4、生成本地静态数据
allure generate ./report/allure -o ./report/result
```
![allure装饰器介绍](./assets/Readme-1636450087171.png)

```
Main()函数加参数时指定运行规则时，参数须要放在列表中。能够指定参数和路径，经常使用的参数有：
-s： 显示程序中的 print/logging 输出
-v: 丰富信息模式, 输出更详细的用例执行信息
-k： 运行包含某个字符串的测试用例。如：pytest -k add XX.py 表示运行 XX.py 中包含 add 的测试用例。
-q: 简单输出模式, 不输出环境信息
-x: 出现一条测试用例失败就退出测试。在调试阶段非常有用，当测试用例失败时，应该先调试通过，而不是继续执行测试用例。
-m: 对用例进行标记，用例需注释@pytest.mark.xxx,将xxx做为参数传入
```