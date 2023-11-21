import unittest


class OutputCheck(unittest.TestCase):
    def assert_output(self, expr, actual):
        """
        断言返回体
        1.断言返回体字段个数
        2.断言返回体字段是否正确
        3.断言返回体字段类型
        4.断言返回体获取列表便签的个数
        :param expr: 期望值，dict demo：{'a':'1,'b':[{'aa': 1,'bb': 'asvd','cc': True},{'aa': 2,'bb':'abcd','cc':False}]}
        :param actual: 实际值
        """
        self.assertEqual(len(expr.keys()), len(actual.keys()), msg='actual keys error!')  # 返回结果字段缺失/异常
        for k, v in expr.items():
            self.assertIn(k, actual.keys())
            if isinstance(v, type):
                self.assertEqual(v, type(actual[k]), msg=f'{k} Dynamic value type assert fail！')  # 返回结果字段类型异常
            elif isinstance(v, dict):
                self.assert_output(v, type(actual[k]))
                self.assertEqual(len(v), len(actual[k]))
            elif isinstance(v, list):
                for index in range(len(v)):
                    if isinstance(v[index], dict):
                        self.assert_output(v[index], actual[k][index])
                    else:
                        self.assertEqual(v[index], actual[k][index], msg=f'{k}(type:list) index:{index} value:{v}')  # 返回字段异常
            else:
                self.assertEqual(v, actual[k], msg=f'key: {k} assert error!')  # 返回结果异常

