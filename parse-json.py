def get_nested_dynamic(data: dict, keys: list, default="N/A"):
    """
    按照动态 keys 列表查找嵌套字典的值（带错误捕捉）
    :param data: 原始字典
    :param keys: key 路径列表，比如 ["symbolication", "pat", "groupId"]
    :param default: 找不到时返回的默认值
    :return: 查找到的值或 default
    """
    try:
        current = data
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return default
        return current
    except Exception as e:
        print(f"⚠️ Error while accessing {keys}: {e}")
        return default