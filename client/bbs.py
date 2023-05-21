#導庫
import os
import keyboard
import time
from colorama import Fore
import socket
import rsa

def get_rsa():
    with open ("rsa_public_key.pem", "r") as r:
        return r.read()

#定義連接服務器類
class connServer:
    def __init__(self):
        self.connect = False
        self.host = ""
        self.port = 0
        self.username = ""
        self.password = ""
        self.sessionKey = ""

#面向對象（服務器類）
sc = connServer()

#定義退出函數
def sysexit():
    os.system("cls")
    print("感謝使用簡易日記！")
    print("Bye!\n")
    os.system("pause")
    exit = os._exit(os.X_OK)

#定義主菜單功能
def menu():
    os.system("cls")
    print("----------------------------------------------------------------")
    print("|                           簡易日記                           |")
    if sc.connect == False:
        print("| 服務器連接狀態： "+ Fore.RED + "未連接" + Fore.RESET +"      聯繫作者：contact@p07575.eu.org |")
    elif sc.connect == True:
        print("| 服務器連接狀態： "+ Fore.GREEN + "已連接" + Fore.RESET +"      聯繫作者：contact@p07575.eu.org |")
    print("|                                                              |")
    print("| 功能：                                                       |")
    print("|                                                              |")
    print("|1) 連接服務器                                                 |")
    print("|                                                              |")
    print("|2) 撰寫日記                                                   |")
    print("|                                                              |")
    print("|3) 查看日記                                                   |")
    print("|                                                              |")
    print("|4) 退出軟件                                                   |")
    print("----------------------------------------------------------------")

#定義連接服務器功能
def ConnectServer():
    while True:
        sc.host = input("請輸入服務器的域名或IP地址以連接服務器>>> ")
        while True:
            try:
                sc.port = int(input("請輸入服務器的端口以連接服務器>>> ")) # server's port
                global client
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((sc.host, sc.port))
            except:
                print("這不是一個有效的端口,請重新輸入！")
                break
            sc.username = input("請輸入用戶名>>> ")
            sc.password = input("請輸入密碼>>> ")
            client.send(f"sign|||{get_rsa()}".encode("UTF-8"))
            rs = client.recv(1024000)
            with open ("rsa_public_key.pem", "wb") as r:
                r.write(rs)
            data = f"{sc.username}|||{sc.password}"
            # print(data)
            # print((rsa.encrypt_data(data)+"|||"+rsa.rsa_private_sign(data)))
            client.send(("login|||"+rsa.encrypt_data(data)+"|||"+rsa.rsa_private_sign(data)).encode("UTF-8"))
            time.sleep(0.8)
            log = client.recv(10240000).decode("utf-8") #Cannot receve data yet
            print(log)
            log = log.split("|||")
            #[0]+"\n\n\n\n"+log[1])
            d = rsa.decrypt_data(log[0])
            print(d+"\n\n"+log[0])
            if rsa.rsa_public_check_sign(d,log[1]):
                log = d
                if "T" in log:
                    sc.connect = True
                    sc.sessionKey = log.split("/")[1]
                    # print(sc.sessionKey)
                    # os.system("pause")
                    break
                else:
                    print("用戶名或密碼出錯,請重新輸入！")
                    break
        if sc.connect == True:
            break
    menu()
    

#定義發送帖子功能
def post(title,name,content):
    global client
    encryptedData=rsa.encrypt_data(f"upload|||{title}|||{name}|||{content}|||{sc.sessionKey}")
    post_content=f"upload|||{encryptedData}|||{rsa.rsa_private_sign(encryptedData)}"
    client.send(post_content.encode("UTF-8"))

#定義顯示帖子功能
def get_post(name):
    if sc.connect == True:
        global client
        os.system("cls")
        data = f"get|||{name}|||{sc.sessionKey}"
        client.send((rsa.encrypt_data(data)+"|||"+rsa.rsa_private_sign(data)).encode("UTF-8"))# Receive code not written on server.py yet! 
        message = client.recv(1024000).decode("UTF-8")
        print(message)
        os.system("pause")
        menu()
    else:
        print("請先連接服務器再查看帖子！！！")
        time.sleep(1)
    menu()

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
    menu()

def gp():
    get_post(sc.username)

rsa.gen_key()

#打開菜單
menu()
if __name__ == '__main__':
    keyboard.add_hotkey('1', ConnectServer)
    keyboard.add_hotkey('2', sm)
    keyboard.add_hotkey('3', gp)
    keyboard.add_hotkey('4', sysexit)
    keyboard.add_hotkey('esc', menu)
    keyboard.add_hotkey('ctrl+c', sysexit)
    keyboard.wait('ctrl+c')
os.system("pause")
