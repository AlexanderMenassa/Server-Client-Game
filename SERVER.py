#Code for server
import socket
from socket import *
import random
import time
#For colored output, please open CMD and type: "pip install colorama" in order to use colored text
import sys


#Alex:
# this is class to use colored text in cmd
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
#server socket 
serverPort = 7772
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind( ("Alexander" , serverPort) )
serverSocket.listen(2)
print ("The server is ready to receive Players")

#Alex:
#messages to be send to players
ResponseToRequest1 = "Player has joined the Server! "
ResponseToRequest2 = colors.YELLOW +"Welcome Player 1, \nRules: a random number will be printed retype it and enter as quickly as possible \nYou have 20 secs before your connection severes, to exit type Exit"+ colors.RESET
ResponseToRequest3 = colors.YELLOW +"Welcome Player 2 \nRules: a random number will be printed retype it and enter as quickly as possible \nYou have 20 secs before your connection severes, to exit type Exit"+ colors.RESET


#Adel:
#Random number from 1 to 9 generator
def generate():
    Num_range= 10 # range from 0-9
    random_number_gen = random.randint(0, Num_range - 1)
    return random_number_gen




#Alex:
while True:

    #To check for error from Proxy side
    # try:
#Alex:        

        #Connecting with PLayer 1 and Player 2 before starting
        count =0
        connectionSocket1, addr1 = serverSocket.accept()
        connectionSocket1.recv(1024).decode()
        connectionSocket1.send(ResponseToRequest1.encode())
        connectionSocket1.send(ResponseToRequest2.encode())
        count+=1
        
        connectionSocket2, addr2 = serverSocket.accept()
        connectionSocket2.recv(1024).decode()
        connectionSocket2.send(ResponseToRequest1.encode())
        connectionSocket2.send(ResponseToRequest3.encode())
        count+=1
        
        
        
        #variables to use
        rounds = 0
        score1 =0
        score2 =0
        left = False
        left11 = False
        left22 = False
        g11 = '0'
        g12 ='0'
        g21 = '0'
        g22 = '0'
        g31 = '0'
        g32 = '0'
        if count == 2:
            while rounds<3:
                
                rounds+=1                
                disqualified1 = False
                disqualified2 = False
                
                
                
                
                
                
                #1
                
         
                #Sending random Number from 1 to 9 to each player
                #sending to player 1 random number 
                Random1 = generate()
#Adel:
                try:
                    connectionSocket1.send(str(Random1).encode())
                except:   #cheking for errors in case the other player left the game
                        connectionSocket2.send("!".encode())
                        connectionSocket2.send((colors.BLUE + "Player1 has left the game, Player2 wins!" + colors.RESET).encode())
                        left = True
                        break
#Alex:
                #start Timer 1 to get elapsed time
                startTime1 = time.time()
                #server receiving user input Player 1
#Mahdi:
                try:
#Alex:
                    player_input1 = connectionSocket1.recv(1024).decode()
                except:
#Adel:
                        connectionSocket2.send("!".encode())
                        connectionSocket2.send((colors.BLUE + "Player1 has left the game, Player2 wins!" + colors.RESET).encode())
                        left = True
                        endTime1 = time.time() 
                        break
#Alex:
                #end Timer 1
                endTime1 = time.time() 
                elapsed1 = endTime1 - startTime1 #calculating RTT
                #checking correctness of result
#Mahdi:
                if str(Random1) == player_input1: 
#Alex:
                    connectionSocket1.send((colors.GREEN  +"Correct Input!"+colors.RESET+'\n').encode())
                # if player1 exited manually we must let players know what happened
                elif player_input1 == "Exit" or player_input1 == "exit" or player_input1 == "EXIT":
                    connectionSocket1.send((colors.BLUE + "Player1 has left the game, Player2 wins!" + colors.RESET).encode())
                    connectionSocket2.send("!".encode())
                    connectionSocket2.send((colors.BLUE + "Player1 has left the game, Player2 wins!" + colors.RESET).encode())
                    left = True
                    break
                else:
                    connectionSocket1.send((colors.MAGENTA  +"Incorrect Input!"+colors.RESET+'\n').encode())
                    disqualified1 = True

 
#Alex:
                #2
                #same as player1 but for player2             
                #now sending to player 2
                Random2 = generate()
#Mahdi:
                try:
                    connectionSocket2.send(str(Random2).encode())  #Alex:
                except:
#Mahdi:
                    connectionSocket1.send("!".encode())
                    connectionSocket1.send((colors.BLUE + "Player2 has left the game, Player1 wins!" + colors.RESET).encode())
                    left = True
                    endTime2 = time.time() 
                    break
 #Alex:               #Timer 2
                startTime2 = time.time()
                #server receiving user input Player 2
                try:
                    player_input2 = connectionSocket2.recv(1024).decode()
#Mahdi
                except:
                    connectionSocket1.send("!".encode())
                    connectionSocket1.send((colors.BLUE + "Player2 has left the game, Player1 wins!" + colors.RESET).encode())
                    left = True
                    endTime2 = time.time() 
                    break
#Alex:
                #end Timer 2
                endTime2 = time.time()
                elapsed2 = endTime2 - startTime2
                print(elapsed2)             
                #cheking correctness of result
                if str(Random2) == player_input2:
                    connectionSocket2.send((colors.GREEN  + "Correct Input!"  + colors.RESET +'\n').encode())
                elif player_input2 == "Exit" or player_input2 == "exit" or player_input2 == "EXIT":                   
                    connectionSocket1.send("!".encode())
                    connectionSocket1.send((colors.BLUE + "Player2 has left the game, Player1 wins!" + colors.RESET).encode())
                    connectionSocket2.send((colors.BLUE + "Player2 has left the game, Player1 wins!" + colors.RESET).encode())
                    left = True
                    break
                else:
                    connectionSocket2.send((colors.MAGENTA+"Incorrect Input!"+ colors.RESET+'\n').encode())
                    disqualified2= True
                    
                
                
#Alex:
                #score

                    #disqualified happens in case a player inputed an incorrect input or timed out or else the server compared RTTs
                if disqualified1 == True and disqualified2 == False :
                    score2+=1
                    if(rounds == 1):
                        g12 = '1'
                    elif rounds == 2:
                        g22= '1'
                    elif rounds == 3:
                        g32 = '1'
                    if(score1 > score2):
                        res =  colors.YELLOW  +"Player1 lost the round due to incorrect input or due to time out!!"+colors.RESET + '\n'  +colors.GREEN +"Player1 score: " + str(score1)  +colors.RESET +'\n' +colors.MAGENTA+ "Player2 score: " + str(score2) +colors.RESET
                    else:
                        res =  colors.YELLOW  +"Player1 lost the round due to incorrect input or due to time out!!"+colors.RESET + '\n'  +colors.GREEN + "Player2 score: " + str(score2) +colors.RESET +'\n'  +colors.MAGENTA +"Player1 score: " + str(score1)+colors.RESET
                    connectionSocket1.send(res.encode())
                    connectionSocket2.send(res.encode())
                    continue
                elif disqualified2 == True and disqualified1 == False:
                    score1+=1
                    if(rounds == 1):
                        g11 = '1'
                    elif rounds== 2:
                        g21= '1'
                    elif rounds == 3:
                        g31 = '1'
                    if(score1 > score2):
                        res =  colors.YELLOW  +"Player2 lost the round due to incorrect input or due to time out!"+colors.RESET + '\n' +colors.GREEN +"Player1 score: " + str(score1) + colors.RESET +'\n' + colors.MAGENTA + "Player2 score: " + str(score2) + colors.RESET
                    else:
                        res =  colors.YELLOW  +"Player2 lost the round due to incorrect input or due to time out!" +colors.RESET + '\n' + colors.GREEN + "Player2 score: " + str(score2) + colors.RESET +'\n' + colors.MAGENTA +"Player1 score: " + str(score1) + colors.RESET
                    connectionSocket1.send(res.encode())
                    connectionSocket2.send(res.encode())
                    continue
                
                elif disqualified1 == True and disqualified2 == True:
                    if(score1 > score2):
                        res = "Draw!" + '\n' + colors.GREEN + "Player1 score: " + str(score1)+ colors.RESET + '\n' + colors.MAGENTA +"Player2 score: " + str(score2) + colors.RESET
                    else:
                        res = "Draw!" + '\n' +colors.GREEN + "Player2 score: " + str(score2) + colors.RESET+ '\n' +colors.MAGENTA + "Player1 score: " + str(score1)+colors.RESET

                    connectionSocket1.send(res.encode())
                    connectionSocket2.send(res.encode())
                    continue
                
                else:
                    dif = abs(elapsed1-elapsed2)
                    if elapsed1 < elapsed2:
                        score1+=1
                        if(rounds == 1):
                            g11 = '1'
                        elif rounds == 2:
                            g21= '1'
                        elif rounds == 3:
                            g31 = '1'
                        if(score1 > score2):
                            res = colors.YELLOW +"Player 1 was faster by: "+ str(dif) + colors.RESET + '\n' + colors.GREEN + "Player1 score: " + str(score1)+colors.RESET + '\n' +colors.MAGENTA +  "Player2 score: " + str(score2)+ colors.RESET
                        else:
                            res = colors.YELLOW + "Player 1 was faster by: " + str(dif)+ colors.RESET +'\n' + colors.GREEN + "Player2 score: " + str(score2) +colors.RESET+ '\n' +colors.MAGENTA +"Player1 score: " + str(score1)+ colors.RESET
                        connectionSocket1.send(res.encode())
                        connectionSocket2.send(res.encode())
                        continue
                        
                    elif elapsed2 < elapsed1:
                        score2+=1
                        if(rounds == 1):
                            g12 = '1'
                        elif rounds== 2:
                            g22= '1'
                        elif rounds == 3:
                            g32 = '1'
                        if(score1 > score2):
                            res = colors.YELLOW +"Player 2 was faster by: "+ str(dif)+ colors.RESET +'\n' +colors.GREEN + "Player1 score: " + str(score1) +colors.RESET+ '\n' +colors.MAGENTA+ "Player2 score: " + str(score2)+ colors.RESET
                        else:
                            res = colors.YELLOW +"Player 2 was faster by: "+ str(dif) +colors.RESET +'\n' +colors.GREEN + "Player2 score: " + str(score2) +colors.RESET+ '\n' +colors.MAGENTA+ "Player1 score: " + str(score1)+ colors.RESET
                        connectionSocket1.send(res.encode())
                        connectionSocket2.send(res.encode())
                        continue
                    else:
                        continue
        
        
            
#Alex:
            #outside the loop
            #case where one of the players left
            if left == True:
#Mahdi
                 connectionSocket1.close()
                 connectionSocket2.close()
#Alex:            
                #if not someone should win or draw
            elif(score1 > score2):
                #player 1 wins:
                 connectionSocket1.send(( colors.CYAN + "\n\n"+ "Winner: Player 1!" +"\nSummary:\n"+f"Rounds       1      2      3\nplayer1      {g11}      {g21}      {g31}\nplayer2      {g12}      {g22}      {g32}"+colors.RESET).encode())
                 connectionSocket2.send(( colors.CYAN +"\n\n"+"Winner: Player 1!"+"\nSummary:\n"+f"Rounds       1      2      3\nplayer1      {g11}      {g21}      {g31}\nplayer2      {g12}      {g22}      {g32}"+colors.RESET).encode())
                 connectionSocket1.close()
                 connectionSocket2.close()
            elif (score2 > score1):
                #player 2 wins:
                 connectionSocket1.send(( colors.CYAN +"\n\n"+"Winner: Player 2!"+"\nSummary:\n"+f"Rounds       1      2      3\nplayer1      {g11}      {g21}      {g31}\nplayer2      {g12}      {g22}      {g32}"+colors.RESET).encode())
                 connectionSocket2.send(( colors.CYAN +"\n\n"+"Winner: Player 2!"+"\nSummary:\n"+f"Rounds       1      2      3\nplayer1      {g11}      {g21}      {g31}\nplayer2      {g12}      {g22}      {g32}"+colors.RESET).encode())
                 connectionSocket1.close()
                 connectionSocket2.close()
            else:
                 connectionSocket1.send(( colors.CYAN +"\n\n"+"Draw!"+"\nSummary:\n"+f"Rounds       1      2      3\nplayer1      {g11}      {g21}      {g31}\nplayer2      {g12}      {g22}      {g32}"+colors.RESET).encode())
                 connectionSocket2.send(( colors.CYAN +"\n\n"+"Draw!"+"\nSummary:\n"+f"Rounds       1      2      3\nplayer1      {g11}      {g21}      {g31}\nplayer2      {g12}      {g22}      {g32}"+colors.RESET).encode())
                 connectionSocket1.close()
                 connectionSocket2.close()
 
           
    # except Exception as e:
    #     print(e)
    #     print("Error from server")
    #     connectionSocket1.close()
    #     connectionSocket2.close()
    #     serverSocket.close()
    #     break

        

