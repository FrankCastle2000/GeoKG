import hanlp
import pandas as pd
import re


def extract_project_type(sentence):
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
    return info


data = pd.read_excel(r"E:\python\练习\词向量聚类\hx\100\data4_test.xlsx", sheet_name="Sheet1")
project_names = []
all_names = data["项目名称"]
# 筛选去除不规范文件名
# # 去除名文件名中的括号及括号里的内容
for project_name in all_names:
    new_name = re.sub(u"\\(.*?\\)|\\（.*?\\）|\\（.*?\\)|\\(.*?\\）", "", project_name)  # 去括号以及括号内的内容
    project_names.append(new_name)
# # 将结果写入txt文件
f = open("data3.txt", "a", encoding="utf-8")
for project_name in project_names:
    if project_name[-2::] == "项目":
        # project_name = project_name.replace("项目", "")
        project_type = extract_project_type(project_name)
        if project_type[-6::] == "建设用地项目" and not is_useful(project_type):
            project_type = "无法分类"
        elif project_type[-4::] == "建设项目" and not is_useful(project_type):
            project_type = "无法分类"
        elif project_type[-4::] == "用地项目" and not is_useful(project_type):
            project_type = "无法分类"
        elif project_type[-4::] == "工程项目" and not is_useful(project_type):
            project_type = "无法分类"
        f.writelines(f"{project_name} -> {project_type}")
        f.writelines("\n")
        print(f"{project_name} -> {project_type}")
f.close()


