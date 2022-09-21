
import tkinter
from pywinauto import application
from pywinauto import keyboard
import time
import random
import threading

# stop all
# kill one --- 5 button

wins = []
titles = ['LDPlayer-0', "LDPlayer-1", "LDPlayer-2", "LDPlayer-3", "LDPlayer-4"]
clzname = 'LDPlayerMainFrame'
killed = {}
stop_all = False
ctl = None
btnall = None
btn0 = None
btn1 = None
btn2 = None
btn3 = None
btn4 = None

def init_before_all():
    for t in titles:
        killed[t] = False

def init_get_all_window():
    for t in titles:
        try:
            wd = application.Application(backend='win32').connect(title_re=t, class_name=clzname).window(title_re='LDP*').window(title_re='TheR*')
            wins.append(wd)
            print(wd.process_id())
        except Exception:
            wins.append(None)
            killed[t] = True
            print("------------------------")
            print("--EEEEEEEEEEEEEError    " + t)
            print("------------------------")

def on_stop_all():
    global stop_all
    global btnall
    if stop_all:        # before click, stop all is True
        stop_all = False
        # mylabel['text'] = "stop-all is False00000"
        btnall['bg'] = 'green'
        # print('stop all false')
    else:
        stop_all = True
        # mylabel['text'] = 'stop-all is True111111'
        btnall['bg'] = 'red'
        # print('stop all true')

def on_kill0():
    global titles
    global killed
    global btn0, btn1, btn2, btn3, btn4
    killed[titles[0]] = True
    # label0['text'] = 'die'
    # label0['bg'] = 'red'
    btn0['text'] = 'die'
    btn0['bg'] = 'red'

def on_kill1():
    global titles
    global killed
    global btn0, btn1, btn2, btn3, btn4
    killed[titles[1]] = True
    # label1['text'] = 'die'
    # label1['bg'] = 'red'
    btn1['text'] = 'die'
    btn1['bg'] = 'red'

def on_kill2():
    global titles
    global killed
    global btn0, btn1, btn2, btn3, btn4
    killed[titles[2]] = True
    # label2['text'] = 'die'
    # label2['bg'] = 'red'
    btn2['text'] = 'die'
    btn2['bg'] = 'red'

def on_kill3():
    global titles
    global killed
    global btn0, btn1, btn2, btn3, btn4
    killed[titles[3]] = True
    # label3['text'] = 'die'
    # label3['bg'] = 'red'
    btn3['text'] = 'die'
    btn3['bg'] = 'red'

def on_kill4():
    global titles
    global killed
    global btn0, btn1, btn2, btn3, btn4
    killed[titles[4]] = True
    # label4['text'] = 'die'
    # label4['bg'] = 'red'
    btn4['text'] = 'die'
    btn4['bg'] = 'red'

def generate_control_window():
    global ctl
    global killed, titles
    global btn0, btn1, btn2, btn3, btn4
    global btnall
    ctl = tkinter.Tk(className='Control')
    ctl.geometry("=180x200+0+300")
    btnall = tkinter.Button(ctl, cnf={"width":11, 'height':5, 'background':'green', 'command':on_stop_all})
    btnall.pack()
    frm2 = tkinter.Frame(ctl, height=20, width=3)
    frm2.pack()
    frm = tkinter.Frame(ctl)
    frm.pack()

    btn0 = tkinter.Button(frm, text='123', bg='blue', command=on_kill0)
    btn0.pack(side=tkinter.LEFT)
    if killed[titles[0]]:
        on_kill0()

    btn1 = tkinter.Button(frm, text='123', bg='blue', command=on_kill1)
    btn1.pack(side=tkinter.LEFT)
    if killed[titles[1]]:
        on_kill1()

    btn2 = tkinter.Button(frm, text='123', bg='blue', command=on_kill2)
    btn2.pack(side=tkinter.LEFT)
    if killed[titles[2]]:
        on_kill2()

    btn3 = tkinter.Button(frm, text='123', bg='blue', command=on_kill3)
    btn3.pack(side=tkinter.LEFT)
    if killed[titles[3]]:
        on_kill3()

    btn4 = tkinter.Button(frm, text='123', bg='blue', command=on_kill4)
    btn4.pack(side=tkinter.LEFT)
    if killed[titles[4]]:
        on_kill4()
    

# SEMA = threading.Semaphore(1)
LOCK = threading.Lock()

# ... thread....
class mythread(threading.Thread):
    def __init__(self, title, win):
        threading.Thread.__init__(self)
        self.title = title
        self.win = win
    
    def run(self):
        try:
            sleeptime = 1
            isfight = False
            ischoose = False
            while True:
                if killed[self.title]:
                    print(self.title + ' killed, so exit')
                    break

                slp = sleeptime + (random.randint(500, 1200) / 1000)
                # print(self.title + " sleep " + str(slp))
                time.sleep(slp)

                if stop_all:
                    print(self.title + " stop all outer")
                    time.sleep(6 + random.randint(7000, 15000) / 1000)
                    continue

                LOCK.acquire()
                try:
                    
                    time.sleep(0.67)
                    sleeptime = 1

                    if stop_all:
                        print(self.title + " stop all inner")
                        continue
                    
                    state = check_state(self.win)

                    if state == 1:      # fight
                        print("   fight...")
                        sleeptime = 21
                        continue
                    elif state == 2:        # choose
                        sleeptime = 19
                        print("   choose...")
                        # sleeptime = 6
                        # time.sleep(15)      # 直接这里等待，这段时间内手工完成。
                        continue
                    else:
                        self.win.set_focus()
                        cnt = random.randint(4,5)
                        while cnt > 0:
                            cnt -= 1
                            if stop_all:
                                cnt -= 10000
                                print(self.title + " stop all inner")
                                continue
                            time.sleep(random.randint(288, 655) / 1000)
                            keyboard.send_keys(
                                '{a down}'
                                '{a up}'
                            )
                        time.sleep(random.randint(1526,1999) / 1000)
                        keyboard.send_keys(
                            '{a down}'
                            '{a up}'
                        )
                        print(self.title + " operation over, release lock")


                finally:
                    LOCK.release()
        except Exception as e:
            print(self.title + " ..error " + str(e))
        finally:
            print(self.title + "... exit...")

def check_state(win) -> int:
    """ 
    1       :   fight 
    2       :   choose 
    other   :   other 

    缺少 拼图的状态
    """
    
    win.set_focus()
    img = win.capture_as_image()
    a = img.getpixel((50, 270))
    b = img.getpixel((200, 270))
    c = img.getpixel((200, 290))

    if a == (130, 156, 202) and b == (132, 157, 203) and c == (132, 157, 203):
        return 1
    elif a == (152, 186, 235) and b == (152, 186, 235) and c == (192, 207, 240):
        return 2

    return -1

# def check_fight(win) -> bool:
#     pass
#     return False

# def check_choose(win) -> bool:
#     pass
#     return False


def start_thread():
    for t in range(len(wins)):
        mt = mythread(titles[t], wins[t])
        mt.start()
        time.sleep(0.32)




if __name__ == "__main__":
    init_before_all()
    init_get_all_window()
    generate_control_window()
    start_thread()

    ctl.mainloop()
