import os
import sys

# mk xxxx.cpp

def mk_cpp():
    '''
    用来生成 LeetCodeCCpp 中的 LT_xx_x.cpp文件
    generate LeetCodeCCpp's LT_xx_x.cpp
    you should copy the problem's name from leetcode. e.g. "720. Longest Word in Dictionary" from https://leetcode.com/problems/longest-word-in-dictionary/
    '''
    lt_name = ""

    if (len(lt_name) < 5):
        lt_name = input("plz input name:")

    # print("-------------")

    t2 = lt_name[0:lt_name.find('.')]
    f_name = "/LT" + t2.zfill(4) + "_" + lt_name[lt_name.find('.') + 2 :].replace(" ", "_") + ".cpp"
    dir_name = "ge" + str(int(int(int(t2)/100)*100))
    if int(t2) < 100:
        dir_name = "gt000"

    content = """
#include "../header/myheader.h"

class """
    content = content + "LT" + t2.zfill(4)

    content = content + """
{
public:



};

int main()
{

    """

    content = content + "LT" + t2.zfill(4) + " lt;\n\n"
        
    content = content + """
    return 0;
}
"""

    # print(f_name)
    name = dir_name + f_name
    pwd = os.getcwd() + "/" + name
    print(pwd)

    # if os.path.isfile(pwd):
    if os.path.exists(name):
        print("already exists, so exit...")
        sys.exit()

    # 如果是/开头，那么是 根目录文件下。
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)

    # not a file, 已经能确保不会删除其他文件了。
    if not os.path.isfile(name):
        fd = open(name, mode="a+", encoding='utf-8')
        fd.write(content)
        fd.close()

if __name__ == "__main__":
    mk_cpp()
    # print(mk_cpp.__doc__)
