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
            print("Debug Mode On")
            if "login|||" in message_from_user: # User Login
                print(message_from_user.split())
                message_from_user = message_from_user.split("|||")
                sig = message_from_user[2]
                message_from_user = rsa.decrypt_data(message_from_user[1])
                # ms = rsa.decrypt_data(ms)
                ms = message_from_user
                message_from_user = message_from_user.split("|||")
                with open("tempRsa.pem", "w") as t:
                    t.write(Rsa[address[0]])
                print("\n\n"+ms+"\n\n"+sig+"\n\n"+"tempRsa.pem")
                if rsa.rsa_public_check_sign(ms, sig,"tempRsa.pem"): # Sign Passed
                    print("Sign Pass")
                    if login(message_from_user[0],message_from_user[1]):
                        print("Login Pass")
                        while True:
                            key = sK.GenPasswd2(8,string.digits) + sK.GenPasswd2(15,string.ascii_letters) # Gen Session Key
                            if key not in Keys:
                                break
                        Keys.append(key) # Session Keys stored in Keys
                        print("\n"+"key:"+key+"\n")
                        CliKey[key]=[message_from_user[0],address[0]] # CliKey[key]=[username, password]
                        print(message_from_user[0]+"\n"+address[0])
                        Cli[address[0]]=key # Cli[password]=key
                        print("Key is saved to varible"+"\n\n")
                        try:print(rsa.encrypt_data(f"T/{key}","tempRsa.pem")+"|||"+rsa.rsa_private_sign(f"T/{key}"))
                        except Exception as e:
                            print(e)
                            print("data encrypt failed")
                        # print(message_from_user[2])
                        # print()
                        client.send((rsa.encrypt_data(f"T/{key}","tempRsa.pem")+"|||"+rsa.rsa_private_sign(f"T/{key}")).encode("UTF-8"))
                        print(f"\nUser {message_from_user[0]} Logined to the Server")
                    else:
                        client.send(rsa.encrypt_data("F","tempRsa.pem")+"|||"+rsa.rsa_private_sign("F").encode("UTF-8"))
            elif "sign" in message_from_user: # Exchange Keys
                message_from_user = message_from_user.split("sign|||")
                Rsa[address[0]]=message_from_user[1]
                client.send(get_rsa())
            elif "upload"in message_from_user: # Upload the post to the server *Needs Rsa 
                with open("tempRsa.pem", "w") as t:
                    t.write(Rsa[address[0]])
                message_from_user = message_from_user.split("|||")
                sign = message_from_user[2]
                message_from_user=rsa.decrypt(message_from_user[1])
                print(f"Message from {}{message_from_user}")
                print("Checking Sign")
                if rsa.rsa_public_check_sign(message_from_user, sign,"tempRsa.pem"):
                    print("Login Pass")
                    message_from_user = message_from_user.split("|||")
                    if CliKey[message_from_user[3]][0] == message_from_user[1]:
                        save_posts(message_from_user[0],message_from_user[1],message_from_user[2])
            elif "get" in message_from_user: # *Needs Rsa
                with open("tempRsa.pem", "w") as t:
                    t.write(Rsa[address[0]])
                message_from_user = message_from_user.split("|||")
                sign=message_from_user[1]
                message_from_user=rsa.decrypt(message_from_user[0])
                # print(f"{CliKey[message_from_user[2]][0]} / {message_from_user[1]} is using function get_post.")
                print("Checking Sign")
                if rsa.rsa_public_check_sign(message_from_user, sign,"tempRsa.pem"):
                    print("Login Pass")
                    message_from_user = message_from_user.split("|||")
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

"""
Problem 1: HUGE BUG
When user gets session key, he/she can get other account's data without a password.
Statues: Mis-found, Not a real bug
"""