import socket
import threading
import json
import sessionKey as sK
import string
import rsa
from datetime import datetime

# Open server.cfg
with open("server.cfg","r") as i:
    cfg = json.load(i)

# Connection Data
host = '127.0.0.1'
port = 8848

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
CliKey = {}
Cli = {}
Rsa = {}
Keys = []

def get_rsa():
    with open ("rsa_public_key.pem", "rb") as r:
        return r.read()

# Sending Messages To All Connected Clients
def check():
    try:
        with open("posts.json", "r") as p:
            data = json.load(p)
    except:
        with open("posts.json", "w") as p:
            json.dump([],p)

def login(username,password):
    for i in range(len(cfg["user"])):
        if cfg["user"][i]==username and cfg["password"][i]==password:
            return 1
    return 0

def send_data(message,client):
    client.send(message.encode("UTF-8"))

def save_posts(title,name,content):
    now = datetime.now()
    date = now.strftime("%d/%m/%Y")
    time = now.strftime("%H:%M:%S")
    with open("posts.json", "r") as p:
        data = json.load(p)
    data[name].append({"title":title,"name":name,"content":content,"date":date,"time":time})
    with open("posts.json", "w") as p:
        json.dump(data,p)

def get_posts(name):
    posts=""
    with open("posts.json", "r") as p:
        data = json.load(p)
    if data[name] == []:
        return "本服務器暫時沒有任何帖子！！！"
    da = data[name]
    for d in da:
        posts=posts+(f'標題：{d["title"]}       由 {d["name"]} 發表於 {d["date"]} {d["time"]} \n\n{d["content"]}\n----------------------------------------------------------------\n')
    return posts

# Handling Messages From Clients
def handle(client):
    while True:
        # print(clients,"\n",CliKey,"\n",Cli,"\n",Keys,"\n","\n")
        try:
            # Broadcasting Messages
            global message_from_user
            message_from_user = client.recv(1024).decode("UTF-8")
            if "%0|%0" in message_from_user:
                # print(message_from_user.split("%0|%0"))
                ms = message_from_user
                # message_from_user = message_from_user.split("%0|%0")
                sig = message_from_user[1]
                message_from_user = rsa.decrypt_data(message_from_user[0])
                ms = rsa.decrypt_data(ms)
                message_from_user = message_from_user.split("%0|%0")
                with open("tempRsa.pem", "w") as t:
                    t.write(Rsa[address[0]])
                # print("\n\n", ms,"\n\n", sig,"\n\n","tempRsa.pem")
                if rsa.rsa_public_check_sign(ms, sig,"tempRsa.pem"):
                    if login(message_from_user[0],message_from_user[1]):
                        while True:
                            key = sK.GenPasswd2(8,string.digits) + sK.GenPasswd2(15,string.ascii_letters)
                            if key not in Keys:
                                break
                        CliKey[key]=[message_from_user[0],address[0]]
                        Cli[address[0]]=key
                        # print(message_from_user[2])
                        Keys.append(key)
                        client.send(rsa.encrypt_data(f"T/{key}")+"%0|%0"+rsa.rsa_private_sign(f"T/{key}").encode("UTF-8"))
                    else:
                        client.send(rsa.encrypt_data("F")+"%0|%0"+rsa.rsa_private_sign("F").encode("UTF-8"))
            elif "rsa" in message_from_user:
                message_from_user = message_from_user.split("rsa/")
                Rsa[address[0]]=message_from_user[1]
                client.send(get_rsa())
            elif "|jasonishandsome|"in message_from_user:
                message_from_user = message_from_user.split("|jasonishandsome|")
                if CliKey[message_from_user[3]][0] == message_from_user[1]:
                    save_posts(message_from_user[0],message_from_user[1],message_from_user[2])
            elif "get" in message_from_user:
                message_from_user = message_from_user.split("/uSB/")
                # print(f"{CliKey[message_from_user[2]][0]} / {message_from_user[1]} is using function get_post.")
                if CliKey[message_from_user[2]][0] == message_from_user[1]:
                    # print("True")
                    send_data(get_posts(message_from_user[1]),client)

        except:
            # Removing And Closing Clients
            clients.remove(client)
            if address[0] in Cli:
                Keys.remove(Cli[address[0]])
                del CliKey[Cli[address[0]]]
                del Cli[address[0]]
            client.close()
            print(f"{str(address)} left!")
            break

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        global address
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        clients.append(client)

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

        # print(clients,"\n",CliKey,"\n",Cli,"\n",Keys,"\n","\n")

rsa.gen_key()

check()

receive()