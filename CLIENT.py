# #How to play:
# first of all open both client and server codes on your computer,
# second, open 2 command prompt from the file directory where the codes are saved
# write on CMD python Client.py and press enter 
# once both players are in the game, the server will begin the game,
# player1 will start, one match is a 3 round game, a number will appear on the screen
# player 1 must enter as quickly as possible the number, after that player 2 will do the same but with a different number
# if player1 or player2 entersan incorrect answer he loses the game or if both players do so its a draw
# if both answers are correct, the player with a faster entry time wins
# each player has a 20 second timer to enter the number or else he loses the round (unless the other players enter a wrong answer or times out)
# after each round, the player with higher score will appear as 1st and the second as second
# if a player exits or suddenly leaves the game, the other player wins
# in the end after 3 rounds, the game ends either with a winner or a draw and the score or all 3 rounds apprear in the summary 




#Alex:
#Code for client 1
from socket import *
import uuid #for mac address
#libraries for time
import time
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
from inputimeout import inputimeout, TimeoutOccurred

#For colored output, please open CMD and type: "pip install colorama" in order to use colored text
#class to use colored output

#Alex:
import sys
if sys.platform == "win32":
    import colorama
    colorama.init()
class colors:
    RED = '\033[95m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[91m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'


#Alex:
#Port number
serverPort = 7772
#Create new Socket
clientSocket = socket(AF_INET, SOCK_STREAM)
RequestMessage = "Hey, I'd like to join the server!"

try:
#Alex:
    #connect client to Game Server
    clientSocket.connect((gethostname(),serverPort))
    #We now encode and send the Request to the Server
    clientSocket.send(RequestMessage.encode())
    Welcome1 = clientSocket.recv(1024).decode()
    print(Welcome1)
    #receiving welcome message
    Welcome = clientSocket.recv(1024).decode()
#Adel:
    print(Welcome)
    left = False
    left1 = False
    rounds =0
    player_input = ""
    #game starts here
    while rounds <3:
        rounds+=1       
        #random number received
        Random = clientSocket.recv(1024).decode()
#Mahdi:
        if(Random == "!"or left == True):  
            #if something went wrong with the other player an "!" from server will arrive so that we handle the error
            ex = clientSocket.recv(1024).decode()
            print(ex)
            break
#Alex:
        print("\n" + "Round Number: " + str(rounds))
        print("\n" +"My number is: " + Random)
        #client input, the player has a timeout limit of 20 secs or else the game considers a failed input
        while player_input == "":
            try:
#Mahdi
                player_input = inputimeout("Enter the number displayed as fast as possible: ",20)  
            except TimeoutOccurred:
                player_input = "-1"
        clientSocket.send(player_input.encode())
#Alex:
        #in case a player wishes to exit manually
        if player_input == "Exit" or player_input == "exit" or player_input == "EXIT":                   
            left = True
            break
        player_input = ""
#Adel:
        #receives the if the input is correct or not
        response = clientSocket.recv(1024).decode()
#Mahdi
        if(response == "!" or left == True):
            ex = clientSocket.recv(1024).decode()
            print(ex)
            left = True
            break
        print(response)
#Adel:    
        #display of the scores of each plaeyer in order of whose winning
        scoreDisp = clientSocket.recv(1024).decode()
#Mahdi
        if(scoreDisp == "!" or left == True):
            ex = clientSocket.recv(1024).decode()
            print(ex)
            left1 = True
            break
#Adel
        print(scoreDisp)
    
    #displays final results and summary
    results = clientSocket.recv(1024).decode()
#Mahdi:
    if(results == "!"):
        ex = clientSocket.recv(1024).decode()
        print(ex)
        left = False
        clientSocket.close()
#Adel:
    else:
        print(results)
        clientSocket.close()
        
    if rounds <= 3 and left1 == True:
        print(colors.BLUE + "Opponent left the match, you are the winner!" + colors.RESET)
    
    
except Exception as e:
    print(e)
    clientSocket.close
    print("Error from client")

    