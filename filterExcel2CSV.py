import xlrd
import csv
# import xlwt
# import pandas
import time

from xlrd.sheet import Cell


excel_path = "/home/ubuntu20/Documents/aa.xls"
out_path = "/home/ubuntu20/Documents/csvs/"

class LineInfo:
    id = ""
    name = ""
    category = ""       # app tag
    template = ""           # fengbian
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
    for i in range(0, book.nsheets):
        sh = book.sheet_by_index(i)
        print("sz of rows:" + str(sh.nrows))
        print(sh.row(0))
        sz2 = sh.ncols
        print(sz2)
        if len(head) == 0:
            row = sh.row(0)
            # print(row.count)
            # for v in row:
            # for i in range(0, row.count()):
            for i in range(0, sz2):
                head.append(suffix[i] + row[i].value)
            print("head. ", head)
        for r in range(1, sh.nrows):
            ll = sh.row(r)
            info = convert(ll)
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
            catemap[info.category].add(info.id)
            tempmap[info.template].add(info.id)
            tempInfoMap[info.template].append(info)



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

    arr = ['超清','高清','标清','流畅']
    newList = []
    gotset = set()
    for tp in arr:
        infoarr = tempInfoMap[tp]
        print(tp, len(infoarr), len(newList))
        for info in infoarr:
            if not info.id in gotset:
                if tp == '超清':
                    print(info.template, "  tp ", len(newList))
                newList.append(info)
        gotset = gotset | tempmap[tp]
        print(len(newList))
    for k, v in tempInfoMap.items():
        if not k in arr:
            infoarr.extend(v)
            gotset = gotset | tempmap[k]

    print(len(newList), len(gotset))
    print(newList[0])

    newList = sorted(newList, key=lambda x : x.updatetime)

    csvfn = out_path + "asd"
    cnt = 1
    lstnum = 0
    num = 5000
    while lstnum <= len(newList):
        part = newList[lstnum : num]
        with open(csvfn + str(cnt).zfill(3) + '.csv', 'w', newline='') as csvFile:
            # sw = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            sw = csv.writer(csvFile)
            sw.writerow(head)
            # sw.writerows(part)            // not iterable...
            for info in part:
                # if info.template != '流畅':
                #     print(info.template)
                sw.writerow([info.id, info.name, info.category, info.template, info.url, info.updatetime])
        cnt += 1
        lstnum = num
        num += 5000




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