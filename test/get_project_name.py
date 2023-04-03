import hanlp
from hanlp_common.document import Document
import pandas as pd
import re


def merge_pos_into_con(doc: Document):
    flat = isinstance(doc['pos'][0], str)
    if flat:
        doc = Document((k, [v]) for k, v in doc.items())
    for tree, tags in zip(doc['con'], doc['pos']):
        offset = 0
        for subtree in tree.subtrees(lambda t: t.height() == 2):
            tag = subtree.label()
            if tag == '_':
                subtree.set_label(tags[offset])
            offset += 1
    if flat:
        doc = doc.squeeze()
    return doc


def getNP(s):
    # s = '(TOP (NP-HLN (NP-PN (NR 新田县) (NR 石羊镇)) (NP (NN 污水) (NN 处理) (NN 设施) (NN 建设) (NN 项目))))'
    s = s.replace(" ", "")
    start = 0  # 记录开始位置
    stack = []  # 记录括号匹配
    np_list = []
    for i in range(len(s)):  # 遍历字符串
        if s[i] == '(':  # 如果遇到左括号
            stack.append(i)  # 把位置压入栈
        elif s[i] == ')':  # 如果遇到右括号
            start = stack.pop()  # 把栈顶位置弹出，作为开始位置
            if s[start + 1:start + 3] == 'NP' and s[start + 3:start + 4] == "(":
                np_list.append(s[start:i + 1])
    return np_list  # 打印从开始位置到当前位置的子串


def getNN(s):
    # s = '(TOP (NP-HLN (NP-PN (NR 新田县) (NR 石羊镇)) (NP (NN 污水) (NN 处理) (NN 设施) (NN 建设) (NN 项目))))'
    s = s.replace(" ", "")
    start = 0  # 记录开始位置
    stack = []  # 记录括号匹配
    nn_list = []
    for i in range(len(s)):  # 遍历字符串
        if s[i] == '(':  # 如果遇到左括号
            stack.append(i)  # 把位置压入栈
        elif s[i] == ')':  # 如果遇到右括号
            start = stack.pop()  # 把栈顶位置弹出，作为开始位置
            if s[start + 1:start + 3] == 'NN':
                nn_list.append(s[start:i + 1])
    return nn_list  # 打印从开始位置到当前位置的子串


con = hanlp.load('CTB9_CON_FULL_TAG_ELECTRA_SMALL')
tok = hanlp.load(hanlp.pretrained.tok.COARSE_ELECTRA_SMALL_ZH)
pos = hanlp.load(hanlp.pretrained.pos.CTB9_POS_ELECTRA_SMALL)
nlp = hanlp.pipeline() \
    .append(pos, input_key='tok', output_key='pos') \
    .append(con, input_key='tok', output_key='con') \
    .append(merge_pos_into_con, input_key='*')

# hanlp.pretrained.constituency.ALL  # 语种见名称最后一个字段或相应语料库

nlp.insert(0, tok, output_key='tok')
# 读取项目名称
# all_name = []
# data = pd.read_excel(r"E:\python\练习\词向量聚类\hx\100\data4_test.xlsx", sheet_name="Sheet1")
# project_names = data["项目名称"]
# for name in project_names:
#     new_name = re.sub(u"\\(.*?\\)|\\（.*?\\）|\\（.*?\\)|\\(.*?\\）", "", name)  # 去括号
#     if new_name[-2::] == "项目":
#         new_name = new_name.replace("用地", "").replace("建设用地", "").replace("建设", "")
#         doc = nlp(new_name)
#         NP_list = getNP(str(doc["con"]))
#         for i in range(len(NP_list)):
#             NP_list[i] = NP_list[i].replace("(", "").replace(")", "").replace(" ", "").replace("NP", "") \
#                 .replace("NN", "").replace("CC", "").replace("NT", "").replace("QP", "").replace("OD", "") \
#                 .replace("CD", "").replace("VV", "").replace("PR", "").replace("NPP", "").replace("-", "") \
#                 .replace("OBJ", "").replace("ADJP", "").replace("JJ", "").replace("SBJ", "").replace("PN", "") \
#                 .replace("NR", "").replace("\n", "").replace("\\n", "").replace("ADVPAD", "").replace("VA", "") \
#                 .replace("APP", "").replace("PU", "").replace("ETC", "")
#         print(new_name, NP_list)
        # if len(NP_list) > 1:
        #     NP = NP_list[-1]  # 取NP_List中的最后一项作为项目的类型
        #     if NP == "项目" and NP_list[-2] != '2022':
        #         NP = NP_list[-2] + NP
        #     elif NP == "建设项目" and NP_list[-2] != '2022年度' and NP_list[-2] != '2022年' and \
        #             NP_list[-2] != '工程' and NP_list[-2] != '2021年' and NP_list[-2] != '2021年度':
        #         NP = NP_list[-2] + NP
        #     elif NP == "建设用地项目" or NP == "建设项目":
        #         NP = "无法分类"
        #     print(new_name, NP_list, NP)
        #     all_name.append([new_name, "  ", NP])

# 将结果导出到txt
# f = open("data3.txt", "a", encoding="utf-8")
# for name in all_name:
#     f.writelines(name)
#     f.writelines("\n")
# f.close()

doc = nlp("武冈市大甸镇尖山村50兆瓦农光互补光伏发电项目升压站建设项目")
print(doc["con"])
doc.pretty_print()
# NP_list = getNP(str(doc["con"]))
NN_list = getNN(str(doc["con"]))
# print(NP_list)
print(NN_list)
# NP = NP_list[1]
# NP = NP.replace("(", "").replace(")", "").replace(" ", "").replace("NP", "") \
#     .replace("NN", "").replace("CC", "").replace("NT", "").replace("QP", "").replace("OD", "") \
#     .replace("CD", "").replace("VV", "").replace("PR", "").replace("NPP", "").replace("-", "") \
#     .replace("OBJ", "").replace("ADJP", "").replace("JJ", "").replace("SBJ", "").replace("PN", "") \
#     .replace("NR", "").replace("\n", "").replace("\\n", "").replace("ADVPAD", "").replace("VA", "") \
#     .replace("APP", "").replace("PU", "").replace("ETC", "")
# print(NP)
