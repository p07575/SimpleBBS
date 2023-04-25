import json
while True:
    with open("server.cfg", "r") as cf:
        config = json.load(cf)
    username = input("Username>>> ")
    password = input("Password>>> ")
    config["user"].append(username)
    config["password"].append(password)
    with open("server.cfg", "w") as cfg:
        json.dump(config,cfg)