"""
等价于 import datetime
"""
from datetime import datetime


def StrTime(_fs_friendly=False):
    """
    获取统一格式的时间
    :param _fs_friendly: 为真时返回不带冒号的字符串
    """
    if _fs_friendly:
        return datetime.now().strftime('%Y-%m-%d_%H%M%S%f')[:-3]
    else:
        return datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')[:-3]


datetime = datetime
