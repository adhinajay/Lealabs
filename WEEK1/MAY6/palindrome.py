#Get user input
word=input('Enter a string :') 

#Converting the user input into lowercase
word=word.lower()
i=0                     #Start pointer              
j=len(word)-1           #End pointer
is_palindrome=True      #Flag to track palindrome status

#Comparing characters from both ends towards the center
while i<=j:                    
    if word[i]!=word[j]:        
        is_palindrome=False     #Mismatch found
        break
    else:
        i+=1                    #Move start pointer forward
        j-=1                    #Move end pointer backward

#Final result based on the flag
if is_palindrome==True:
    print(word,'is palindrome')
else:
    print(word,"is not a palindrome!!")