import socket
import threading
import json

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
    
def send_data(message,client):
    client.send(message.encode("UTF-8"))

def save_posts(title,name,content):
    with open("posts.json", "r") as p:
        data = json.load(p)
    data.append({"title":title,"name":name,"content":content})
    with open("posts.json", "w") as p:
        json.dump(data,p)

def get_posts():
    posts=""
    with open("posts.json", "r") as p:
        data = json.load(p)
    if data == []:
        return "本服務器暫時沒有任何帖子！！！"
    for d in data:
        posts=posts+(f'標題：{d["title"]}       由 {d["name"]} 發表 \n\n{d["content"]}\n----------------------------------------------------------------\n')
    return posts

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message_from_user = client.recv(1024).decode("UTF-8")
            if "|jasonishandsome|"in message_from_user:
                message_from_user = message_from_user.split("|jasonishandsome|")
                save_posts(message_from_user[0],message_from_user[1],message_from_user[2])
            elif "get" in message_from_user:
                send_data(get_posts(),client)
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