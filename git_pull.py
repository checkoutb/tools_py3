
import os
import time


def read_file():
    # print("------ done---")
    # f = open("paths.ignore", 'r')
    with open("paths.ignore", 'r') as f:
        arr = f.readlines()
        print(arr)
        print(len(arr))
        for p in arr:
            # print(p)
            git_pull(p)

def git_pull(path):
    if len(path) < 5:
        return
    if path.startswith("--"):
        # print("startswith --...")
        return
    if path.endswith('\n'):
        path = path[0 : len(path) - 1]
        # print("rm - " + path)
    # d = os.system("cd " + path)
    # print(d)
    cnt = 0
    done = False
    cmd = "git -C " + path + " pull"
    print(cmd)
    while ((not done) and (cnt < 5)):
        cnt += 1
        try:
            print("------------------>>> start to pull")
            # d = os.system("git pull")
            # d = os.system("git status")
            d = os.system(cmd)
            print(d)
            if d == 0:
                done = True
        except Exception as e:
            print(repr(e))
            time.sleep(15)       // second
    print("====================>>> done: " + str(done) + ", " + str(cnt))


if __name__ == '__main__':
    read_file()
    print("-----all done-----")





