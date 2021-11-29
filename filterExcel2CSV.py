from typing import ItemsView
import xlrd
import csv
# import xlwt
# import pandas
import time

from xlrd.sheet import Cell


excel_path = "/home/ubuntu20/Documents/aa.xls"              # excel文件的 路径
out_path = "/home/ubuntu20/Documents/csvs/"            # csv文件的 目录

class LineInfo:
    id = ""         # video id
    name = ""       # video name
    category = ""       # app tag
    template = ""           # 类型/分辨率
    url = ""
    updatetime = ""

def readAndDistinct():
    pass
    alllist = []
    idset = set()
    cateset = set()
    tempset = set()
    catemap = {}
    tempmap = {}
    tempInfoMap = {}
    head = []
    suffix = ['v.','v.','c.','vo.','','v.']

    book = xlrd.open_workbook(excel_path)
    print("sz of sheets:" + str(book.nsheets))
    for i in range(0, book.nsheets):              # 遍历每个sheet
        sh = book.sheet_by_index(i)
        print("sz of rows:" + str(sh.nrows))
        print(sh.row(0))
        sz2 = sh.ncols
        print(sz2)
        if len(head) == 0:             # 这个是 构造 csv的 首行，是 通过 excel的 首行 + 前缀 来生成  csv的首行
            row = sh.row(0)
            # print(row.count)
            # for v in row:
            # for i in range(0, row.count()):
            for i in range(0, sz2):
                head.append(suffix[i] + row[i].value)
            print("head. ", head)
        for r in range(1, sh.nrows):              # 遍历 sheet。
            ll = sh.row(r)
            info = convert(ll)          # 一行转成 一个对象
            alllist.append(info)
            idset.add(info.id)
            cateset.add(info.category)
            tempset.add(info.template)
            # catemap[info.category].append(info.id)
            # tempmap[info.template].append(info.id)
            # catemap.get(info.category, []).append(info.id)
            if not (info.category in catemap):
                catemap[info.category] = set()
            if not (info.template in tempmap):
                tempmap[info.template] = set()
            if not (info.template in tempInfoMap):
                tempInfoMap[info.template] = []
            catemap[info.category].add(info.id)         # 按 app_tag 分组， 存的是 id， 为了print
            tempmap[info.template].add(info.id)     # 按 分辨率 分组， 存id， 为了 print 和 过滤
            tempInfoMap[info.template].append(info)  # 按分辨路分组， 存对象， 为了 csv文件



# 下面是 写代码时的 一些 输出， 来参考这些输出，写的代码。 没有什么用了
    print(len(alllist), len(idset), len(cateset), len(tempset))
    # print(idset)
    print(cateset)
    print(tempset)
    print(len(catemap), len(tempmap))
    # print(catemap)
    # print(tempmap)
    for k, v in catemap.items():
        print(k, len(v))
    for k, v in tempmap.items():
        print(k, len(v))

    set2 = set()
    for k, v in tempmap.items():
        if len(v) > 1000:
            set2 = set2 | v

    print(len(set2))

    set3 = set()
    for k, v in tempmap.items():
        if len(v) <= 1000:
            set3 = set3 | v
            for id in v:
                if id in set2:
                    print("in set2 " + id)
                else:
                    print("not", end = ',')
            print()
    print(len(set3))

    for k, v in tempmap.items():
        if len(v) <= 1000:
            for k2, v2 in tempmap.items():
                if k == k2:
                    continue
                seta = v & v2
                if len(seta) > 0:
                    print("aaa. ", k, seta)
# 输出的结束，上面没有什么用。 也不太清楚作用了。



    # 开始获得 csv文件中的 超请，高清，标清，流畅，并 过滤
    arr = ['超清','高清','标清','流畅']
    newList = []
    gotset = set()          # 已经获得的 videoID
    for tp in arr:            # 遍历arr，这样就 先获得 超请，再高清， 再标清，最后 流畅
        infoarr = tempInfoMap[tp]
        print(tp, len(infoarr), len(newList))
        for info in infoarr:
            if not info.id in gotset:            # 如果这个videoId 没有访问过，说明是 这个video的 最高分辨率。
                if tp == '超清':
                    print(info.template, "  tp ", len(newList))
                newList.append(info)
        gotset = gotset | tempmap[tp]            # 该分辨率的 所有id  都已经访问， 加入到 已访问集合
        print(len(newList))
    for k, v in tempInfoMap.items():
        if not k in arr:
            infoarr.extend(v)
            gotset = gotset | tempmap[k]

    print(len(newList), len(gotset))
    print(newList[0])

    newList = sorted(newList, key=lambda x : x.updatetime)         # 按 updatetime 倒序

# 下面只是 超请，高清，标清，流畅 的 csv
    csvfn = out_path + "asd"
    cnt = 1
    lstnum = 0
    num = 5000
    while lstnum <= len(newList):
        part = newList[lstnum : num]              # 每次5000条，在本段的最后修改。
        with open(csvfn + str(cnt).zfill(3) + '.csv', 'w', newline='') as csvFile:
            # sw = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            sw = csv.writer(csvFile)
            sw.writerow(head)
            # sw.writerows(part)            // not iterable...
            for info in part:
                # if info.template != '流畅':
                #     print(info.template)
                sw.writerow([info.id, info.name, info.category, info.template, info.url, info.updatetime])
        cnt += 1            # csv文件名字的一部分
        lstnum = num
        num += 5000         # +5000

# 下面是 非 超请，标情，高清，流畅 的 csv， 这里没有过滤。
    newList = []
    for k, v in tempInfoMap.items():
        if not k in arr:
            for info in v:
                newList.append(info)
    print("...", len(newList))
    with open(csvfn + '_other.csv', 'w', newline='') as csvFile:              # 数量比较少，所以直接一个文件
        sw = csv.writer(csvFile)
        sw.writerow(head)
        for info in newList:
            sw.writerow([info.id, info.name, info.category, info.template, info.url, info.updatetime])
    


# excel中 每行数据转换为 LineInfo对象。
def convert(ll: list) -> LineInfo:              # list != List
    info = LineInfo()
    info.id = ll[0].value
    info.name = ll[1].value
    info.category = ll[2].value
    info.template = ll[3].value
    info.url = ll[4].value
    info.updatetime = ll[5].value
    return info


if __name__ == "__main__":
    readAndDistinct()