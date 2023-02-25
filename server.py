import socket
import threading
import json
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
        try:
            # Broadcasting Messages
            global message_from_user
            message_from_user = client.recv(1024).decode("UTF-8")
            if "%0|%0" in message_from_user:
                message_from_user = message_from_user.split("%0|%0")
                if login(message_from_user[0],message_from_user[1]):
                    client.send("T".encode("UTF-8"))
                else:
                    client.send("F".encode("UTF-8"))

            elif "|jasonishandsome|"in message_from_user:
                message_from_user = message_from_user.split("|jasonishandsome|")
                save_posts(message_from_user[0],message_from_user[1],message_from_user[2])
            elif "get" in message_from_user:
                message_from_user = message_from_user.split("/uSB/")
                send_data(get_posts(message_from_user[1]),client)
        except:
            # Removing And Closing Clients
            clients.remove(client)
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

check()

receive()