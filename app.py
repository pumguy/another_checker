from sys import exit
import re
import json
from pathlib import Path

def main():
    # 打开文件与验证
    try:
        checker=open("./checker.cfg")
        
    except IOError:
        print("无法找到 checker.cfg 配置文件或配置文件无法打开，请确认本程序运行路径下包含该文件。")
        return

    try:
        contest=json.load(checker)

    except JSONDecoderError:
        print("无法解析 checker.cfg ，请确认格式正确。")
        return

    # 主要部分
    root_path=Path(contest["root_path"])
    ID_pattern=re.compile(contest["regex"])
    contestant_list=[]

    for some in root_path.iterdir():
        if some.is_dir() and ID_pattern.match(some.name):
            contestant_list.append({"name": some.name, "path": some})
    
    if len(contestant_list)==0:
        print("没有找到符合要求的个人文件夹，请检查你的代码文件夹存放位置正确，且考号填写正确")
        return

    if len(contestant_list)>1:
        print("发现多个符合要求的个人文件夹，请确保考号填写正确")
        return

    contestant=contestant_list[0]
    print("选手："+contestant["name"])
    for problem in contest["problems"]:
        print("题目："+problem["name"])

        source_pattern=re.compile(problem["regex"])
        source_list=[]

        for some in (root_path/contestant["path"]).rglob("*"):
            if source_pattern.match(str(some.relative_to(root_path/contestant["path"]))):
                source_list.append(some)

        if len(source_list)==0:
            print("本题没有找到任何源文件，请确保你的代码源文件储存在个人文件夹下的题目文件夹中，且扩展名符合要求。")

        if len(source_list)>1:
            print("本题找到了多份源文件，请确保本题只有一份源代码。")

        for source in source_list:
            print("将提交的源文件："+str(source))


if __name__=="__main__":
    main()
    input("按任意键继续...")
