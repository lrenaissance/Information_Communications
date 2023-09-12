'''
  ETTTP_Sever_skeleton.py
 
  34743-02 Information Communications
  Term Project on Implementation of Ewah Tic-Tac-Toe Protocol
 
  Skeleton Code Prepared by JeiHee Cho
  May 24, 2023
 
 '''

import random
import tkinter as tk
from socket import *
import _thread
import re

from ETTTP_TicTacToe_skeleton import TTT, check_msg

    
if __name__ == '__main__':
    
    global send_header, recv_header
    SERVER_PORT = 12000
    SIZE = 1024
    server_socket = socket(AF_INET,SOCK_STREAM)
    server_socket.bind(('',SERVER_PORT))
    server_socket.listen()
    MY_IP = '127.0.0.1'
    
    while True:
        client_socket, client_addr = server_socket.accept() #connected with client_socket
        
        start = random.randrange(0,2)   # select random to start
        
        ###################################################################
        # Send start move information to peer
        if start==1: # client starts
            msg="SEND ETTTP/1.0\r\nHost:127.0.0.1\r\nFirst-Move:YOU\r\n\r\n" #First-Move:YOU(client)
            
            client_socket.send(msg.encode()) #send msg to peer
            
        
        else: #server starts
            msg="SEND ETTTP/1.0\r\nHost:127.0.0.1\r\nFirst-Move:ME\r\n\r\n" #First-Move:ME(server)
            
            client_socket.send(msg.encode()) #send msg to peer
            
        
        
        ######################### Fill Out ################################
        # Receive ack - if ack is correct, start game
        start_msg = client_socket.recv(SIZE).decode() #recieve ack
    
        #check if ack is correct by parsing using split function, and save it in array 'ack'
        ack= []
        for s in re.split('[ /\r\n:]',start_msg):
            if s!='' :
                ack.append(s)
        
        #check if ack is correct
        if ack[0] !="ACK" or check_msg(start_msg,MY_IP)==False:
            #ack wrong -> quit the game
            quit()
        #ack correct-> code below is executed
       
        ###################################################################
        
        root = TTT(client=False,target_socket=client_socket, src_addr=MY_IP,dst_addr=client_addr[0])
        root.play(start_user=start)
        root.mainloop()
        
        client_socket.close()
        
        break
    server_socket.close()