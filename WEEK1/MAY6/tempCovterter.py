# Convert Celsius to Fahrenheit
def celsius_to_fahrenheit(temp): 
    return temp*(9/5)+32

# Convert Fahrenheit to Celsius
def fahrenheit_to_celsius(temp):
    return (temp-32)*5/9

# Menu display
print("Temperature Converter")
print(" 1 for Celsius to Fahrenheit\n 2 for Fahrenheit to Celsius")

choice=input("Enter your choice :") #inputing the choice from the user

if choice=='1':
    temp=float(input("Enter the temperature in Celsiues :"))
    result=celsius_to_fahrenheit(temp)
    print(temp,'in Fahrenheit is:',result)  #print the temperature in Fahrenheit

elif choice=='2':
    temp=float(input("Enter the temperature in Fahrenheit :"))
    result=fahrenheit_to_celsius(temp)
    print(temp,'in Celsius is:',result) #Print the temperature in Celsius

else:
    print("Invalid input!!")  #Print error message if the input in invalid