"""
    Filename : str_util.py
    Summary  : 字符串处理
    License  : www.cyeap.com
    Version  : 1.0
    Author   : Jet Bi
    Email    : 1207501666@qq.com
    Date     : 2018/06/17
    Notes    :
        20180617 1.0 增加 none2empty(obj)
"""


def none2empty(obj):
    """
    如果 obj 为 None,将返回空字符串,否则返回 obj
    :param obj:
    :return: obj or ""
    """
    return obj if obj is None else ""
