
# 代码报错(和这里后续的内容无关)，在查看23.14的时候，发现texi的内容有点偏差，可能主要是转义字符这块，
# 23-键盘映射.texi 的 998行最后：并将其作为向量 [?pf1] 返回。
# 对应的markdown 是 781行：并将其作为向量 `[?\Cc pf1]` 返回。
# 在线文档(目前是对应23.15章节)是 returns it as the vector [?\C-c pf1]. 
# 下载的最新的 texi中也是 returns it as the vector @code{[?\C-c pf1]}
# 不过看了其他的几个文件，感觉没有问题


# fork完，下载到本地，准备提交，才发现，那个demo.gif中，他可以有目录，跳转之类的，但是我不知道他是什么工具。
# https://www.zhihu.com/question/482341937 zhihu上有个类似的提问，回答是
# 不需要SEO就Docsify/Docute
# 有博客需求就Jekyll/Hexo/Hugo
# 喜欢用React/Vue就Docusaurus/VuePress
# 想要更加灵活就Gatsby/Next.js/Nuxt.js
# 。。。



# ----------

# 试图学习 emacs/elisp，找到了一份 emacs 的elisp文档 (https://www.gnu.org/software/emacs/manual/elisp.html) 的中文翻译版: https://github.com/advanceflow/Elisp

# 但是这是markdown的，无法使用浏览器打开并导航。
# 所以这里的代码的 主要目标: 
#   1. 将所有的标题单独抽取出来，形成目录。
#   2. 转成html，只是增加html的换行，增加锚点，上页，下页，目录来导航。
# 次要目标: 
#   1. 代码框，主要问题是原md中，应该也是直接复制的html，所以并没有``` ```的代码框，所以无法识别，转换。
#   2. 拆分文件，原md是，一个章节一个md文件，所以单个md文件有点大，最大的是40章，280k。

# 发现仓库里还有texi文件。里面的元信息更明确。
# texi2html，448mb。
# 不知道原先修改了md的什么内容，看了写git show，感觉好多。但是只改了md，没有改texi。

# 我也从官网下了texi文件，有Makefile文件，make时需要安装texinfo。生成了一个 4.9mb的elisp.info。

# 还是使用github仓库中的翻译后的texi。









# 1. 在 texi文件夹中，执行 `texi2html *.texi` ， 把所有texi文件转成html

#       转换后，内部的序号都是从1开始的，不过原先的序号还是在的，需要修正
#   感觉要用beautiful soup 来爬生成的html。也可以直接string find 当作文本处理。
#   <h2 class="section">1.5 9.5 速记</h2> 到 <hr/> 
#   每个文件需要导入css文件，设置head的title

# 2. 修改2处html
#   1. 2569行： <h2 class="section">1.12 26.12 使某些文件名 <code>神</code> 奇</h2> 改成 <h2 class="section">1.12 26.12 使某些文件名神奇</h2> 。 就是删除<code>标签，不然beautiful soup会报错。
#   2. 3106行：改成 <h3 class="subsection">1.17.3 29.17.3 带有侧窗的帧布局</h3> 。也是删除<code>标签
#   3. 785行：<h3 class="subsection">1.4.3 40.4.3 记录消息留言</h3>
# 直接本文搜 `<code>神</code> 奇</h2>` 可以看到出错的地方

# 3. 执行本脚本

# 4. 可以删除 texi 中的 *.html, `rm *.html`, 和 /html中的 done 文件夹



# todo  done
# 1 修正章节编号
# 2 拆分html
# 3 抽取相同的html

# 本来想的是: h2+section -> table+menu, 结果有 table+header 的。而且还有 subsection。
#   主要的问题是，我不知道正文是不是有table
#   table+menu是子章节，table+header是导航菜单
#   目前看起来，最深的是 <h3>, 有更深的标题号，但是html中不会用 h4 来标记了，而是用 li 来标记。
#   table+header 之上有 <a> 的锚点， table+menu 没有

# 拆分规则，h1+chapter -> table+menu/header
#           h2+section -> table+menu/header
#           h3+subsection -> table+menu/header


# 生成了 906个html，一共3.7mb (最终一共908个文件，增加一个 00_content.htm, 一个 elisp.css)
#   我下载了最新的html的elisp手册，一共1067项，10.3mb
#   个数差不多，大小差了很多，应该是中文和英文的区别？还有就是，我的没有previous，top，up，之类的导航


# 接下来，需要进行组织：主目录，prev,next,up等

# 根据文件名，排序，就可以获得完整的目录，然后就是上下级关系，可以通过序号。
# 要特别处理 附录的序号，比如 0D.1_Emacs_Lisp_编码约定.html, 这个是附录D的。

# 之前拆分生成的内容，附录那些文件，有点问题，有些附录还带着 texi2html 的那个table。不管了




from bs4 import BeautifulSoup
import os



fdir = "texi/"       # 需要修改
foutdir = "html/"             # 需要手工建立
fdone = foutdir + "done/"  # check file processed   # 需要手工建立

outhead = '''<!DOCTYPE html><html><head><link rel="stylesheet" type="text/css" href="elisp.css"><title>n33d_repLaced</title></head><body lang="en" bgcolor="#FFFFFF" text="#000000" link="#0000FF" vlink="#800080" alink="#FF0000">'''
outend = "</body></html>"


# 获得文件目录
def get_files_meta():
    paths = os.listdir(fdir)
    ans = []    # fname
    for p in paths:
        if p.endswith("html"):
            ans.append(p)
    return ans

# 读取文件
# def read_file():

# 生成名字
# def generate_file_name():

# 检查文件是否已生成
def check_file_existed(fname):
    return os.path.exists(fdone + fname)

# 生成文件来表示文件已处理
def file_done(fname):
    with open(fdone + fname, 'w', encoding='utf-8') as f:
        f.write("")

# 写文件
def write_file(fcontent, title):
    fcontent = outhead.replace("n33d_repLaced", title) + fcontent + outend

    if title[1] == '.' or title[1] == ' ':
        title = "0" + title
    title = title.replace(' ', '_')
    title = title.replace('/', '')
    title += ".html"
    # print(title)

    with open(foutdir + title, 'w', encoding='utf-8') as f:
        f.write(fcontent)

# 处理文件：读取，拆分，保存
def process_file(fname):
    # read file
    fhtml = open(fdir + fname, encoding='utf-8').read()
    bsoup = BeautifulSoup(fhtml, features="html.parser")

    # chapter

    ch = bsoup.body.find("h1", "chapter")        # chapter, 每个文件一个
    # out = ch.string
    # print(ch)
    # ch = ch.find_next_sibling("table", "menu")
    out = ""
    title = ""

    ch.string.replace_with(ch.string[ch.string.find(' ') + 1:])
    title = ch.string

    while ch != None:
        if 'table' == ch.name:
            if hasattr(ch, "attrs") and 'class' in ch.attrs and "menu" in ch.attrs['class']:
                break

        # print("\n======\n" + str(ch))
        # print(ch.tag)
        # print(type(ch))
        # print(ch.name)
        # if callable(getattr(ch, 'attrs', None)):
        # if hasattr(ch, 'attrs'):
        #     print(ch.attrs)
        # else:
        #     print("noooooo attrs")

        out += str(ch)
        ch = ch.next_sibling

    write_file(out, title)
    out = ""
    title = None

    # section

    chs = bsoup.body.find_all("h2", "section")
    for ch in chs:
        # print(ch.string)
        # print(ch.string.find(' '))
        # print(ch.string[ch.string.find(' ') + 1:])      # not exist: -1, -1+1 = 0.
        ch.string.replace_with(ch.string[ch.string.find(' ') + 1: ])
        title = ch.string
        # print(ch)
# <h2 class="section">1.12 26.12 使某些文件名 `<code>神</code> 奇</h2>`
# 估计这个有问题，导致 ch 不是 string，而是一个tag。
# 是的，<h3 class="subsection">1.17.3 29.17.3 带有侧窗的 <code>帧</code> ( <code>frame</code> )布局</h3>
# 这些报错，直接改原html。

        while ch != None:
            if 'table' == ch.name:
                if hasattr(ch, "attrs") and 'class' in ch.attrs and ("header" in ch.attrs['class'] or "menu" in ch.attrs['class']):
                    break

            if 'a' == ch.name:
                if hasattr(ch, "attrs") and 'name' in ch.attrs:
                    # print(ch)
                    ch = ch.next_sibling
                    continue

            out += str(ch)
            ch = ch.next_sibling
        
        write_file(out, title)
        out = ""
        title = None


    # subsection

    chs = bsoup.body.find_all("h3", "subsection")
    for ch in chs:
        
        ch.string.replace_with(ch.string[ch.string.find(' ') + 1: ])
        title = ch.string
        while ch != None:        
            if 'table' == ch.name:
                if hasattr(ch, "attrs") and 'class' in ch.attrs and ("header" in ch.attrs['class'] or "menu" in ch.attrs['class']):
                    break

            if 'a' == ch.name:
                if hasattr(ch, "attrs") and 'name' in ch.attrs:
                    # print(ch)
                    # print(ch.attrs)
                    ch = ch.next_sibling
                    continue

            out += str(ch)
            ch = ch.next_sibling
        
        write_file(out, title)
        out = ""




################## organize ###################

class HtmlEntry:
    def __init__(self, fname):
        self.fname = fname
        self.ord = ""

        # 附录_A, 0D.2, XXXXXX.html
        # 40.1, 40.10, 40.2     附录_E.10 不管了，就一个。
        if fname[1].isnumeric():
            self.ord = fname[: fname.find('_')]
            self.ord = ".".join([x if len(x) == 2 else ("0"+x) for x in self.ord.split('.')])        # niuwa，精通！
        else:
            if fname[0].isnumeric():        # 0D.2
                self.ord = "附录_" + fname[1: fname.find("_")]
            elif fname.startswith("附录"):
                self.ord = fname[: fname.find('_') + 2]
            else:   # xxxxx.html
                self.ord = fname

        # self.fst = ""
        # self.snd = ""
        # self.thd = ""

        # t2 = fname[: fname.find("_")]
        # self.fst = t2[0: t2.find(".")]
        # t2 = t2[t2.find("."): ]
        # if len(t2) > 0:
        #     self.snd = t2[0: t2.find(".")]
        #     t2 = t2[t2.find("."): ]
        # if len(t2) > 0:
        #     self.thd = t2[0: t2.find(".")]

    def __repr__(self):
        # return self.fst + ", " + self.snd + ", " + self.thd + ", " + self.fname
        return self.ord + ", " + self.fname

navi_template = '''<div class="nav-panel"><p>Next: <a href="{}">{}</a>, Previous: <a href="{}">{}</a>, Up: <a href="{}">{}</a> &nbsp; [<a href="00_content.htm" title="Table of contents" rel="contents">Contents</a>]</p></div></body></html>'''

url_template = '''<a href="{}">{}</a>'''

def generate_index():
    paths = os.listdir(foutdir)
    fname = []    # fname
    for p in paths:
        if p.endswith("html"):
            fname.append(HtmlEntry(p))
    # fname.sort()      # 40.9.2 在 40.9 前面，不能默认
    fname.sort(key = lambda x: x.ord)

    # for f in fname:
    #     print(f)

    content_out = "<ul>"
    content = HtmlEntry("00_content.htm")
    prev = content
    nxt = None
    up = [content]
    lvl = 0
    
    # 生成目录
    # 生成prev,next,up
    for i in range(len(fname)):
        if i + 1 == len(fname):
            nxt = content
        else:
            nxt = fname[i + 1]
        
        navi = navi_template.format(nxt.fname, nxt.fname[nxt.fname.find("_") + 1: -5], prev.fname, prev.fname[prev.fname.find("_") + 1: -5], up[-1].fname, up[-1].fname[up[-1].fname.find("_") + 1: -4])

        lines = []
        with open(foutdir + fname[i].fname, 'r') as f:
            lines = f.readlines()
        
        # print(fname[i].fname)
        lines.pop()
        if len(lines) <= 1 or not lines[1].startswith('<div class="nav-panel">'):  # 多次运行，只插入一次       # 23.14 pop后只有一行。
            lines.insert(1, navi + "<hr/>")
        lines.append(navi)

        with open(foutdir + fname[i].fname, 'w') as f:
            f.writelines(lines)
# <ul>
#     <li><a>111</a></li>
#     <li><a>222</a>
#         <ul>
#             <li><a>zzz</a></li>
#         </ul>
#     </li>
# </ul>
        prev = fname[i]
        ahref = url_template.format(fname[i].fname, fname[i].fname[: -5])
        dotcnt = nxt.fname.count('.')       # 1.1.2.3.2 后 1.2
        if dotcnt > lvl:        # 不认为会出现 1.1 后 1.1.1.1, 就是 缺失了 1.1.1, 不考虑这个问题
            up.append(fname[i])     # 1.1 -> 1.1.1
            lvl = dotcnt
            content_out += "<li>" + ahref + "<ul>\n"
        elif dotcnt < lvl:      # 1.1.1.1 -> 1.2
            content_out += "<li>" + ahref + "</li>\n"
            while dotcnt < lvl:
                up.pop()
                lvl -= 1
                content_out += "</ul></li>"
        else:
            content_out += "<li>" + ahref + "</li>\n"

    with open(foutdir + content.fname, 'w', encoding="utf-8") as f:
        f.write(content_out)

#####################################
css = '''
a.summary-letter {text-decoration: none}
blockquote.smallquotation {font-size: smaller}
div.display {margin-left: 3.2em}
div.example {margin-left: 3.2em}
div.lisp {margin-left: 3.2em}
div.smalldisplay {margin-left: 3.2em}
div.smallexample {margin-left: 3.2em}
div.smalllisp {margin-left: 3.2em}
pre.display {font-family: serif}
pre.format {font-family: serif}
pre.menu-comment {font-family: serif}
pre.menu-preformatted {font-family: serif}
pre.smalldisplay {font-family: serif; font-size: smaller}
pre.smallexample {font-size: smaller}
pre.smallformat {font-family: serif; font-size: smaller}
pre.smalllisp {font-size: smaller}
span.nocodebreak {white-space:pre}
span.nolinebreak {white-space:pre}
span.roman {font-family:serif; font-weight:normal}
span.sansserif {font-family:sans-serif; font-weight:normal}
ul.no-bullet {list-style: none}
'''

def create_css():
    with open(foutdir + "elisp.css", 'w', encoding='utf-8') as f:
        f.write(css)



if __name__ == "__main__":
    fileNames = get_files_meta()
    print("got" + str(len(fileNames)))
    print(fileNames)
    for fname in fileNames:
        # exist_name = check_file_existed(fname)
        # if exist_name != None:
        if check_file_existed(fname):
            print("file already exist: " + fname)
            continue
        
        print("start to process " + fname)

        process_file(fname)
        file_done(fname)

##############################
    generate_index()


##############################
    create_css()


