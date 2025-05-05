import random
low=int(input("Enter the lower limit :"))
high=int(input("Enter the upper limit :"))
value=random.randint(low,high)
count=10
attempt=1
while count>0:
    count=count-1
    guess=int(input("Guess an integer :"))
    if (guess<low or guess>high):
        print("Invalid input!!")
    if guess==value:
        print("Congratulations!!, you guessed the value in",attempt,"attempt")
        break
    elif guess>value:
        print("Your guess is too large, Try again!!\nNumber of Chances left:",count)
    elif guess<value:
        print("Your guess is too small, Try again!!\nNumber of Chances left:",count)
    attempt=attempt+1
print("\nYour chance is over!!\nThe value is :",value,"\nIt was a nice game!!")