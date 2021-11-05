
import os


# 毫无意义, 直接 主raml  raml2html 就可以生成一个html, 这个html 就是全部.不需要 dfs.

dir = "/home/ubuntu20/Documents/raml/api-test"
command = "raml2html"       # raml2html example.raml > example.html

def raml2html(path2):
    # d = os.system("ifconfig")
    # print("..")
    # print(d)
    if os.path.isdir(path2):
        lst = os.listdir(path2)
        for p in lst:
            np = os.path.join(path2, p)
            raml2html(np)
    else:
        if path2.endswith(".raml"):
            t2 = command + " " + path2 + " > " + path2[0 : -4] + "html"
            print(t2)
            os.system(t2)


if __name__ == "__main__":
    raml2html(dir)
    print("end")

