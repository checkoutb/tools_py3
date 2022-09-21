
import os



# 。。没有什么用。postman本身就可以 graphql。


# 空行是分隔符
# 没有variable。只是body。
# " 没有转义..直接replace了



txtPath = "111.ignore"


def main():
    out = ""
    with open(txtPath, 'r', encoding='utf-8') as f:
        done = False
        lstIs0 = True
        while not done:
            line = f.readline()
            # print(len(line))
            if line == '':
                done = True
            else:
                if len(line) <= 1:
                    if not lstIs0:
                        out += '\r\n'       # 真换行
                    lstIs0 = True
                else:
                    if not lstIs0:
                        out += '''\\r\\n '''
                    out += line[0 : -1].strip()
                    lstIs0 = False
    out = out.replace('"', '\\"')
    with open(txtPath + "222.ignore", 'w', encoding='utf-8') as f:
        f.write(out)





if __name__ == '__main__':
    # print(os.getcwd())
    main()
