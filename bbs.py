#導庫
import os
import keyboard
import time
from colorama import Fore
import socket

#定義變量
cons = "0"

#定義連接服務器類
class connServer:
    def __init__(self):
        self.connect = False
        self.host = ""
        self.port = 0
        self.username = ""

#面向對象（服務器類）
sc = connServer()

#定義退出函數
def sysexit():
    os.system("cls")
    print("感謝使用簡易郵件！")
    print("Bye!")
    exit = os._exit(os.X_OK)
    if sc.connect == True:
        client.close()
    return exit 

#定義主菜單功能
def menu():
    os.system("cls")
    print("----------------------------------------------------------------")
    print("|                           簡易論壇                           |")
    if sc.connect == False:
        print("| 服務器連接狀態： "+ Fore.RED + "未連接" + Fore.RESET +"      聯繫作者：contact@p07575.eu.org |")
    elif sc.connect == True:
        print("| 服務器連接狀態： "+ Fore.GREEN + "已連接" + Fore.RESET +"      聯繫作者：contact@p07575.eu.org |")
    print("|                                                              |")
    print("| 功能：                                                       |")
    print("|                                                              |")
    print("|1) 連接服務器                                                 |")
    print("|                                                              |")
    print("|2) 發表帖子                                                   |")
    print("|                                                              |")
    print("|3) 查看帖子                                                   |")
    print("|                                                              |")
    print("|4) 退出軟件                                                   |")
    print("----------------------------------------------------------------")
    if __name__ == '__main__':
        keyboard.add_hotkey('1', ConnectServer)
        keyboard.add_hotkey('2', sm)
        keyboard.add_hotkey('3', get_post)
        keyboard.add_hotkey('4', sysexit)
        keyboard.add_hotkey('esc', menu)
        keyboard.add_hotkey('ctrl+c', sysexit)
        keyboard.wait('ctrl+c')

#定義主菜單（無鍵盤識別功能）功能
def mprint():
    os.system("cls")
    print("----------------------------------------------------------------")
    print("|                           簡易論壇                           |")
    if sc.connect == False:
        print("| 服務器連接狀態： "+ Fore.RED + "未連接" + Fore.RESET +"      聯繫作者：contact@p07575.eu.org |")
    elif sc.connect == True:
        print("| 服務器連接狀態： "+ Fore.GREEN + "已連接" + Fore.RESET +"      聯繫作者：contact@p07575.eu.org |")
    print("|                                                              |")
    print("| 功能：                                                       |")
    print("|                                                              |")
    print("|1) 連接服務器                                                 |")
    print("|                                                              |")
    print("|2) 發表帖子                                                   |")
    print("|                                                              |")
    print("|3) 查看帖子                                                   |")
    print("|                                                              |")
    print("|4) 退出軟件                                                   |")
    print("----------------------------------------------------------------")

#定義連接服務器功能
def ConnectServer():
    while True:
        sc.host = input("請輸入服務器的域名或IP地址以連接服務器>>> ")
        sc.username = input("請輸入用戶名（不用註冊）>>> ")
        while True:
            try:
                sc.port = int(input("請輸入服務器的端口以連接服務器>>> ")) # server's port
                global client
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((sc.host, sc.port))
                sc.connect = True
                break
            except:
                print("這不是一個有效的端口，請重新輸入！")
                break
        if sc.connect == True:
            break
    mprint()

#定義發送帖子功能
def post(title,name,content):
    global client
    post_content=f"{title}|jasonishandsome|{name}|jasonishandsome|{content}"
    client.send(post_content.encode("UTF-8"))

#定義顯示帖子功能
def get_post():
    if sc.connect == True:
        global client
        os.system("cls")
        client.send("get".encode("UTF-8"))
        message = client.recv(1024000).decode("UTF-8")
        print(message)
        os.system("pause")
        mprint()
    else:
        print("請先連接服務器再查看帖子！！！")
        time.sleep(1)
    mprint()

#定義輸入帖子功能
def sm():
    if sc.connect == True:
        title=input("帖子標題>>> ")
        content = ""
        print("請輸入帖子內容:")
        while True:
            c1=input()
            if c1 == "":
                break
            else:
                content=content+c1+"\n"
        post(title,sc.username,content)
        print("發表成功！！！")
        time.sleep(1)
    else:
        print("請先連接服務器再發表帖子！！！")
        time.sleep(1)
    mprint()

#打開菜單
menu()
os.system("pause")
