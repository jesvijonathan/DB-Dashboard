from os import truncate
import database
from config import *
from mysql import connector
from flask import Flask, redirect, url_for, request, render_template

import pickle

def visitor_ip():
    print(request.remote_addr,request.environ['REMOTE_ADDR'])
    pass


def dash_load_data():
    di = None

    try:
        with open('data/users.pkl', 'rb') as f:
            di = pickle.load(f)
        print("user data loaded")
    except:
        print("error laoding")
        dash_data_res()

    return di

def dash_data_res():
    dic = {}

    dic2 = { 'username':'admin', 
    'password':'root', 
    'email':'jesvijonathan.aids2020@citchennai.net', 
    'first_name':'administrator', 
    'last_name':'',
    'member':'sudo',}
    
    dic['admin']=dic2

    with open('data/users.pkl', 'wb') as f:
        pickle.dump(dic, f)
    
    print("user data initialize/reseted")

def dash_register(d):   
    
    dic = dash_load_data()
    ok_list = []

    for y in d:
        for x in dic:
            if y == x:
                print(x,"already there...")
                return "Username already present.."
            else:
                ok_list.append(y)

    for user in ok_list:
        dic[user]=d[user] 

    try:
        with open('data/users.pkl', 'wb') as f:
            pickle.dump(dic, f)
    except:
        print("error")
        return "Error"
        
    return 1

def menu():
    while(True):
        t=int(input("\n\n1. View data\n2. Register user\n3. Reset data\n4. Quit\n:"))
        if t==1:
            f = dash_load_data()
            print(f)
        elif t==2:
            
            fn = input("firstname : ")
            ln = input("lastname : ") 
            u = input("username : ")    
            p = input("password : ")
            e = input("email : ")
            m = input("member : ")
            arrange(u,p,e,fn,ln,m)
        elif t==3:
            dash_data_res()
        elif t==4:
            exit()

def arrange(u,p,e,fn,ln,m):
    d = {}
    d1 = {'username':u, 'password':p, 'email':e, 'firstname':fn, 'lastname':ln, 'member':m }
    d[u]=d1
    return dash_register(d)

#menu()