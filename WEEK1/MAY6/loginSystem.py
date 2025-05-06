username='admin'    #Saved username
password='Admin@1234'   #Saved password
attempts=3  #number of attempts,currently setted it upto 3 attempts
while(attempts>0):

    #Get user input
    entered_username=input("Enter the username :")
    entered_password=input("Enter the password :")

    #Check credetials
    if entered_username==username and entered_password==password:
        print("Login Successful")
        break
    else:
        attempts-=1
        print("Incorrect credentials")
        print(attempts,'left')
        
#if all attempts are used up
if attempts==0:
    print("Too many failed attempts.Try after some time!!")