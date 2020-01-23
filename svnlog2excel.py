import xlwt
import time


'''
svn log come from TortoiseSVN -> show Log -> Copy to blipboard -> Full date.
copy the log to svn_log.txt.
'''


class FileInfo:
    version=-1
    author='null'
    action='null'
    msg='null'
    branch="nil"
    name='null'

Aversion='Revision:'
Aauthor='Author:'
Aaction='Modified'
Amsg='Message'
Atag='----'
Abranch=''

# use Atag2 to get branch's name. The string after Atag2 is project's name. (project's name also is branch's name)
# set it by yourself
Atag2='这个需要自己设置的。。。'           # 这个是为了获得分支，路径中在这个string之后的就是工程名。(这里工程名就是分支名)。

map2 = {}

with open('svn_log.txt') as file:
    version2=-1
    author2='nil'
    action2='nil'
    msg2='nil'
    branch2='nil'
    name2='nil'
    isAction2 = True
    for line in file.readlines():
        # print(line)
        if (len(line)<=2):
            continue
        if (line.startswith(Aversion)):
            version2 = int(line[len(Aversion):])
            isAction2 = False
        elif (line.startswith(Aauthor)):
            author2 = line[len(Aauthor):-1]
        elif (line.startswith(Atag)):
            isAction2 = True
        elif isAction2:
            action2=line[0:line.find(':')]
            i2 = line.find(Atag2)+len(Atag2)
            # name2=line[line.find('/'):]
            name3=line[line.rfind('/')+1:-1]
            if name3 in map2:
                if map2[name3].version>version2:
                    pass
                else:
                    branch2=line[i2:line.find('/', i2+1)]
                    t1 = map2[name3]
                    t1.version=version2
                    t1.action=action2
                    t1.author=author2
                    t1.branch=branch2
            else:
                branch2=line[i2:line.find('/', i2+1)]
                t1=FileInfo()
                t1.name=name3
                t1.version=version2
                t1.action=action2
                t1.author=author2
                t1.branch=branch2
                map2.setdefault(name3, t1)

for k, v in map2.items():
    # print(k)
    print('%-60s %-25s %-10s %-10s' % (v.name, v.branch, v.version, v.author))

print(len(map2))

book = xlwt.Workbook()
sheet = book.add_sheet('last update')
row = 0
sheet.col(0).width=256*60
sheet.col(4).width=256*15
sheet.col(5).width=256*25
for v in map2.values():
    col = 0
    sheet.write(row, col, v.name)
    sheet.write(row, 2, v.version)
    sheet.write(row, 3, v.action)
    sheet.write(row, 4, v.author)
    sheet.write(row, 5, v.branch)
    # sheet.write(row, 6, v.)
    row += 1
book.save('Svn_' + time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime(int(time.time()))) + ".xls")
