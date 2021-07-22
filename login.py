import config
import log

def verification(var):
    di = log.dash_load_data()
    
    print(di,var)
    
    if var in di:
        return 2

    user = var['username'] 
    pas = var['password']

    if user == config.username and pas == config.password:
        return 1
    else:
        return "Incorrect username/password !"