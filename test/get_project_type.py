import hanlp
import pandas as pd
import re


def extract_project_type(sentence):
    """通过NN生成项目类别"""
    hanlp.pretrained.mtl.ALL  # MTL多任务，具体任务见模型名称，语种见名称最后一个字段或相应语料库
    pipeline = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_UDEP_SDP_CON_ELECTRA_SMALL_ZH)
    doc = pipeline([sentence], tasks=['pos/ctb', 'dep'])
    # print(doc['tok/fine'][0])
    project_types = []
    for i, (word, (head, dep), ctb) in enumerate(zip(doc['tok/fine'][0], doc['dep'][0], doc['pos/ctb'][0])):
        if dep == 'compound:nn' and ctb == 'NN':
            project_types.append(word)
        elif dep == 'nmod:assmod' and ctb == 'NN':
            project_types.append(word)
        else:
            # project_type.clear()
            pass
    # 组合提取到的名词，构成项目类型描述
    project_type_str = ''.join(project_types) + '项目'
    return project_type_str


def is_useful(s: str):
    """筛选有用的项目关键词"""
    info = False
    if "电气" in s:
        info = True
    elif "污水" in s:
        info = True
    elif "公路" in s:
        info = True
    elif "大桥" in s:
        info = True
    elif "输变电" in s:
        info = True
    elif "配水站" in s:
        info = True
    elif "垃圾" in s:
        info = True
    elif "升压站" in s:
        info = True
    elif "游客" in s:
        info = True
    return info


def get_type(project_names):
    """循环生成项目类别"""
    all_types = []
    all_project_names = []
    for project_name in project_names:
        # 只有项目名称以“项目”结尾的才添加到all_project_names列表中
        if project_name[-2::] == "项目":
            all_project_names.append(project_name)
            project_type = extract_project_type(project_name)
            if project_type[-6::] == "建设用地项目" and not is_useful(project_type):
                project_type = "无法分类"
            elif project_type[-4::] == "建设项目" and not is_useful(project_type):
                project_type = "无法分类"
            elif project_type[-4::] == "用地项目" and not is_useful(project_type):
                project_type = "无法分类"
            elif project_type[-4::] == "工程项目" and not is_useful(project_type):
                project_type = "无法分类"
            elif "年度" in project_type:
                project_type = "无法分类"
            all_types.append(project_type)
            print(f"{project_name} -> {project_type}")
    return all_types, all_project_names


def name_format(name_list: list):
    """去除文件名中的括号及括号里的内容"""
    project_names = []
    for name in name_list:
        new_name = re.sub(u"\\(.*?\\)|\\（.*?\\）|\\（.*?\\)|\\(.*?\\）", "", name)
        project_names.append(new_name)
    return project_names


def _get_new_type(_type: str, _key: str):
    """去除项目名称中的地名"""
    new_string = _type
    for s in _type:
        if s != _key[0]:
            new_string = new_string[1:]
        elif s == _key[0]:
            return new_string


def type_clean(type_list: list):
    """对类型结果进行清洗"""
    all_type_cleaned = []
    for _type in type_list:
        if "污水" in _type:
            all_type_cleaned.append(_get_new_type(_type, "污水"))
        elif "升压站" in _type:
            all_type_cleaned.append(_get_new_type(_type, "升压站"))
        elif "公路" in _type:
            all_type_cleaned.append(_get_new_type(_type, "公路"))
        else:
            all_type_cleaned.append(_type)
    return all_type_cleaned


def save_to_txt(type_list: list, all_project_nams: list, save_path="all_type.txt"):
    """将结果分行写入txt文件"""
    f = open(save_path, "a", encoding="utf-8")
    for idx in range(len(type_list)):
        s = f"{all_project_nams[idx]} -> {type_list[idx]}"
        f.writelines(s)
        f.writelines("\n")
    f.close()


if __name__ == "__main__":
    data = pd.read_excel(r"E:\python\练习\词向量聚类\hx\100\data4_test.xlsx", sheet_name="Sheet1")
    allNames = data["项目名称"]
    projectNames = name_format(allNames)
    allProjectTypes, allProjectNames = get_type(projectNames)
    allTypesCleaned = type_clean(allProjectTypes)
    save_to_txt(allTypesCleaned, allProjectNames)
