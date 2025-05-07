# Take user input
user_input=input("Enter a string :")

# Open the file in write mode to save the input
f1=open('user_input','w')   
f1.write(user_input)        
f1.close()

# Open the file in read mode to read the content back
f2=open('user_input','r')   
read_input=f2.read() 
f2.close()

# Print the content read from the file
print(read_input)