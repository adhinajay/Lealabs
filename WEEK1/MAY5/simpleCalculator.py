num1=float(input("Enter the first number :"))
num2=float(input("Enter the second number :"))
choice=input(" 1 for Addition\n 2 for Subtraction\n 3 for Multiplication\n 4 for Division\nEnter your choice :")
if(choice=='1'):
    result=num1+num2
elif(choice=='2'):
    result=num1-num2
elif(choice=='3'):
    result=num1*num2
elif(choice=='4'):
    if(num2!=0):
        result=num1/num2
    else:
        print("The denominator should not be 0!!")
        result='Flag'
else:
    print("Invalid Input!!")   
if(result!='Flag'):
    print("The result is :",result)
