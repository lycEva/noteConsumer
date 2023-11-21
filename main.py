import unittest
from BeautifulReport import BeautifulReport
import os

ENVIRON = "Offline"  # 线上 Online 测试环境 Offline
Dir = os.path.dirname(os.path.abspath(__file__))


def run(test_suite):
    # 定义输出的文件位置和名字
    filename = "report.html"
    result = BeautifulReport(test_suite)
    result.report(filename=filename, description='测试报告', report_dir='./')


if __name__ == '__main__':
    pattern = 'all'  # all: run all case,  smoking: run smoking case.
    if pattern == 'all':
        suite = unittest.TestLoader().discover('./testCase', 'test_*')
    elif pattern == 'smoking':
        suite = unittest.TestLoader().discover('./testCase', 'test_major')
    else:
        raise Exception("pattern error")
    run(suite)

