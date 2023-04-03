def is_useful(s: str):
    info = False
    if "电气" in s:
        info = True
    elif "污水" in s:
        info = True
    elif "公路" in s:
        info = True
    return info


def _get_new_type(_type: str, _key: str):
    new_string = _type
    for s in _type:
        print(s)
        if s != _key[0]:
            new_string = new_string[1:]
            print("new_string:", new_string)
        elif s == _key[0]:
            return new_string


if __name__ == "__main__":
    all_name = []
    s = "我是江一凡"
    all_name.append(s)
    all_name.append(s)
    all_name.append(s)
    all_name.append(s)
    all_name.append(s)
    all_name.append(s)
    all_name.append(s)
    all_name.append(s)

    print(all_name)

