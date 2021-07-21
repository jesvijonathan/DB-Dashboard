import config

def verification(var):
    print(var)
    user = var['username'] 
    pas = var['password']
    if user == config.username and pas == config.password:
        return 1
    else:
        return "Incorrect username/password !"