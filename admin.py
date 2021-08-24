import log

#run this program to control data via console

def menu():
    while(True):
        t=int(input("\n\n0. Quit\n1. View data\n2. Register user\n3. Delete User\n4. Reset data\n5. View guest\n6. delete guest\n7. Reset guest data\n:"))
        
        if t==0:
            exit()

        elif t==1:
            f = log.dash_load_data()

            admin = {}
            sudo = {}
            member = {}
            
            for i  in f:
                user = f[i]

                if user["member"] == "sudo":
                    sudo[user["username"]] = user  
                elif user["member"] == "admin":
                    admin[user["username"]] = user
                elif user["member"] == "user":
                    member[user["username"]] = user
            
            print()
            #print("Sudo Users -")
            for user in sudo:
                print(sudo[user])
            #print("\nAdmin Users -")
            for user in admin:
                print(admin[user])
            #print("\nMember Users -")
            for user in member:
                print(member[user])

        elif t==2:
            
            fn = input("firstname : ")
            ln = input("lastname : ") 
            u = input("username : ")    
            p = input("password : ")
            e = input("email : ")
            m = input("member : ")
            log.arrange(u,p,e,fn,ln,m)
        
        elif t==3:
            u = input("Enter username : ")
            log.delete_user(username=u)
        
        elif t==4:
            log.dash_data_res()
        
        elif t==5:
            f = log.dash_load_data_guest()

            print()
            for guest in f:
                print(f[guest])

        elif t==6:
            u = input("Enter username : ")
            log.delete_guest(u)
        
        elif t==7:
            log.dash_data_res_guest()
        
menu()