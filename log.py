from os import truncate
import login
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
    dic = { 'admin':'root'}

    with open('data/users.pkl', 'wb') as f:
        pickle.dump(dic, f)
    
    print("user data initialize/reseted")

def dash_register(use=None,pas=None):   
    
    dic = dash_load_data()
    
    for x in dic:
        if x == use:
            print("already there..")
            return
    
    dic[use]=pas        

    try:
        with open('data/users.pkl', 'wb') as f:
            pickle.dump(dic, f)
    except:
        print("error")

def menu():
    while(True):
        t=int(input("\n\n1. View data\n2. Register user\n3. Reset data\n:"))
        if t==1:
            f = dash_load_data()
            print(f)
        elif t==2:
            u = input("username : ")    
            p = input("password : ")
            dash_register(u,p)
        elif t==3:
            dash_data_res()
