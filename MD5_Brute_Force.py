import string # for string.printable
from timeit import default_timer as timer # for timing
import hashlib # allows for hashing

# go thru each password in the list
def bruteforce(passwords, forced):
    
    passcount = 0 # number of passwords seen
    
    # iterate through every password passed as an argument
    for password in passwords:
        
        # increment passcount for each new password
        passcount += 1
        
        # check if the newline was included in the password (it shouldn't be)
        if password[-1] == '\n':
            password = password[:-1] # remove the newline
        
        # start timing the bruteforce
        starttime = timer()
        
        # run brute force on the password
        foundpass = getpassword(password)
        
        # runtime == time-before-bruteforce - time-after-brute-force
        runtime = (timer() - starttime) * 1000
        
        # print password to console
        print("Found password " + str(passcount) + ": " + foundpass)
        print("In " + str(runtime) + " ms")
        
        # add to list
        forced.append(foundpass)
        
        
# individual brute force ran on each password
# note: will result in infinite loop if the hash is nonexistent in charset (or it is longer than 5 characters)
def getpassword(password) -> str:
    
    # get target hash
    target = password
    
    # "string" to hold the iterative bruteforce
    current = list('0')
    
    # true when the hash is found
    found = False
    
    # the current incrementing index in the b.f. loop
    index = 0 
    
    # brute force loop
        #   starts with character '0', and increments through the list until reaching '~'
        #   acts like a loop counting up in base-len(charSet)
    while not found:
        
        # carry ~ like they are ones when counting up
        while current[index] == '~':
            
            # reset char to 0 and move forwards
            current[index] = '0'
            index += 1
            
            # if you carry ones to the end of the string, increase password length
                # slower to check this way but u have to check bounds before accessing the element
            if index >= len(current):
                current.append('0')
                print("Trying strings of length " + str(len(current)) + "...")
                break
            
            # carry that one
            elif current[index] != '~': 
                current[index] = alphabet[alphabet.index(current[index]) + 1]
                
            
        # reset index to front
        index = 0
        
        # move char up one
        current[index] = alphabet[alphabet.index(current[index]) + 1]
        
        # convert list to string (because strings are immutable for some godforsaken reason?)
        currentstring = "".join([str(i) for i in current])
        
        # convert string to md5 hash
        encrypted = hashlib.md5(currentstring.encode()).hexdigest()
        
        # check if hashes match and return if they do
        if encrypted == target:
            found = True # just in case i guess lol
            return currentstring
            

if __name__ == '__main__':
    
    # get list of possible characters in password
    alphabet = list(string.printable)

    #open the file containing the hashes
    passwords = open('hashes.txt', 'r')
    passCount = 0

    # stores cracked passwords
    forced = ['Passwords:']
    
    # start timing
    beginning = timer()
    
    # run brute force
    bruteforce(passwords=passwords, forced=forced)
    
    # print the runtime of the brute force
    runtime = (timer() - beginning)*1000
    print(f"Found {len(forced)} passwords in {runtime} ms")

    # print the passwords
    for i in range(len(forced)):
        print(f"Password {i}: {forced[i]}")