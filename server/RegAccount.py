import json
simpleBBS="""
  _________.__               .__           ____________________  _________
 /   _____/|__| _____ ______ |  |   ____   \______   \______   \/   _____/
 \_____  \ |  |/     \\____ \|  | _/ __ \   |    |  _/|    |  _/\_____  \ 
 /        \|  |  Y Y  \  |_> >  |_\  ___/   |    |   \|    |   \/        \ 
/_______  /|__|__|_|  /   __/|____/\___  >  |______  /|______  /_______  /
        \/          \/|__|             \/          \/        \/        \/ 

"""
while True:
    print(simpleBBS)
    with open("server.cfg", "r") as cf:
        config = json.load(cf)
    choice = input("1) Add Account 2) Delete Account>>> ")
    username = input("Username>>> ")
    password = input("Password>>> ")
    if int(choice)==1:
        config["user"].append(username)
        config["password"].append(password)
    else:
        ynq = input(f"Delete Account Named {username}? (Y/N)")
        if ynq=="Y":
            config["user"].remove(username)
            config["password"].remove(password)
    with open("server.cfg", "w") as cfg:
        json.dump(config,cfg)