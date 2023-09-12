'''
  ETTTP_Client_skeleton.py
 
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

    SERVER_IP = '127.0.0.1'
    MY_IP = '127.0.0.1'
    SERVER_PORT = 12000
    SIZE = 1024
    SERVER_ADDR = (SERVER_IP, SERVER_PORT)

    
    with socket(AF_INET, SOCK_STREAM) as client_socket:
        client_socket.connect(SERVER_ADDR)  
        
        ###################################################################
        # Receive who will start first from the server
        #start 보냄
        start_msg = client_socket.recv(SIZE).decode()
        
        
        #받은 msg 파싱해서 누가 시작인지 파악하기. 잘 받았다는 ack보냄
        #p_msg: 받은 메시지를 파싱해서 저장할 리스트
        p_msg=[]
        for s in re.split('[ /\r\n:]',start_msg):
          #s가 공백이 아닐 경우에만 p_msg에 저장
          if s!='':
            p_msg.append(s)
        # p_msg 예시: ['SEND', 'ETTTP', '1.0', 'Host', '127.0.0.1', 'First-Move', 'ME']
 
        ######################### Fill Out ################################
        # Send ACK

        
        # p_msg[0]이 SEND이고 check_msg에서 start_msg가 제대로 도착했음이 확인되면
        if p_msg[0] == "SEND" and check_msg(start_msg,SERVER_IP):
          #send ACK
          msg = "ACK ETTTP/1.0\r\nHost:127.0.0.1\r\nFirst-Move:YOU\r\n\r\n"
          client_socket.send(msg.encode())
          #받은 msg를 파싱해서 시작하는 사람이 ME인지 YOU인지 확인
          if p_msg[6]=="YOU":
            #YOU인 경우 나부터 시작(start=1)
            start=1
          #ME인 경우 상대방부터 시작(start=0)
          else:
            start=0
        #제대로 된 메시지가 오지 않은 경우 종료    
        else :
            quit()
        ###################################################################
        
        # Start game
        root = TTT(target_socket=client_socket, src_addr=MY_IP,dst_addr=SERVER_IP)
        root.play(start_user=start)
        root.mainloop()
        client_socket.close()
        
        
        