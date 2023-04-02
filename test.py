def is_useful(s: str):
    info = False
    if "电气" in s:
        info = True
    elif "污水" in s:
        info = True
    elif "公路" in s:
        info = True
    return info


if __name__ == "__main__":
    ss = "汝城县钨矿独立工矿区生活污水处理建设项目"
    print(is_useful(ss))
