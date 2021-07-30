import config
import log

def verification(var):
    di = log.dash_load_data()
    
    print(di,var)
    
    if var in di:
        return 2

    user = var['username'] 
    pas = var['password']
    
    d = log.dash_load_data()

    if user == config.username and pas == config.password:
        return 1
    elif user in d:
        if d[user]['password']==pas:
            return 1
        else:
            return "Incorrect password !"
    else:
        return "Username does not exist !"