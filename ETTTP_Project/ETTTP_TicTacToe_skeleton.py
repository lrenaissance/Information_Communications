'''
  ETTTP_TicTacToe_skeleton.py
 
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

SIZE=1024

class TTT(tk.Tk):
    def __init__(self, target_socket,src_addr,dst_addr, client=True):
        super().__init__()
        
        self.my_turn = -1

        self.geometry('500x800')

        self.active = 'GAME ACTIVE'
        self.socket = target_socket
        
        self.send_ip = dst_addr
        self.recv_ip = src_addr
        
        self.total_cells = 9
        self.line_size = 3
        
        
        # Set variables for Client and Server UI
        ############## updated ###########################
        if client: #0: server, 1: client
            self.myID = 1   # client일 때 ui
            self.title('34743-02-Tic-Tac-Toe Client')
            self.user = {'value': self.line_size+1, 'bg': 'blue',
                         'win': 'Result: You Won!', 'text':'O','Name':"ME"} #client가 이긴 경우
            self.computer = {'value': 1, 'bg': 'orange',
                             'win': 'Result: You Lost!', 'text':'X','Name':"YOU"} #client가 진 경우(시작한 사람이 client?)
        else:
            self.myID = 0 # server일 때 ui
            self.title('34743-02-Tic-Tac-Toe Server')
            self.user = {'value': 1, 'bg': 'orange',
                         'win': 'Result: You Won!', 'text':'X','Name':"ME"}  #server가 이긴 경우
            self.computer = {'value': self.line_size+1, 'bg': 'blue',
                     'win': 'Result: You Lost!', 'text':'O','Name':"YOU"} #server가 진 경우
        ##################################################

            
        self.board_bg = 'white'
        self.all_lines = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6))

        self.create_control_frame()

    def create_control_frame(self):
        '''
        Make Quit button to quit game 
        Click this button to exit game

        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.control_frame = tk.Frame()
        self.control_frame.pack(side=tk.TOP)

        self.b_quit = tk.Button(self.control_frame, text='Quit',
                                command=self.quit)
        self.b_quit.pack(side=tk.RIGHT)
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def create_status_frame(self):
        '''
        Status UI that shows "Hold" or "Ready"
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.status_frame = tk.Frame()
        self.status_frame.pack(expand=True,anchor='w',padx=20)
        
        self.l_status_bullet = tk.Label(self.status_frame,text='O',font=('Helevetica',25,'bold'),justify='left')
        self.l_status_bullet.pack(side=tk.LEFT,anchor='w')
        self.l_status = tk.Label(self.status_frame,font=('Helevetica',25,'bold'),justify='left')
        self.l_status.pack(side=tk.RIGHT,anchor='w')
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def create_result_frame(self):
        '''
        UI that shows Result
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.result_frame = tk.Frame()
        self.result_frame.pack(expand=True,anchor='w',padx=20)
        
        self.l_result = tk.Label(self.result_frame,font=('Helevetica',25,'bold'),justify='left')
        self.l_result.pack(side=tk.BOTTOM,anchor='w')
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def create_debug_frame(self):
        '''
        Debug UI that gets input from the user
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.debug_frame = tk.Frame()
        self.debug_frame.pack(expand=True)
        
        self.t_debug = tk.Text(self.debug_frame,height=2,width=50)
        self.t_debug.pack(side=tk.LEFT)
        self.b_debug = tk.Button(self.debug_frame,text="Send",command=self.send_debug)
        self.b_debug.pack(side=tk.RIGHT)
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    
    def create_board_frame(self):
        '''
        Tic-Tac-Toe Board UI
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.board_frame = tk.Frame()
        self.board_frame.pack(expand=True)

        self.cell = [None] * self.total_cells
        self.setText=[None]*self.total_cells
        self.board = [0] * self.total_cells
        self.remaining_moves = list(range(self.total_cells))
        for i in range(self.total_cells):
            self.setText[i] = tk.StringVar()
            self.setText[i].set("  ")
            self.cell[i] = tk.Label(self.board_frame, highlightthickness=1,borderwidth=5,relief='solid',
                                    width=5, height=3,
                                    bg=self.board_bg,compound="center",
                                    textvariable=self.setText[i],font=('Helevetica',30,'bold'))
            self.cell[i].bind('<Button-1>',
                              lambda e, move=i: self.my_move(e, move))
            r, c = divmod(i, self.line_size)
            self.cell[i].grid(row=r, column=c,sticky="nsew")
            
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def play(self, start_user=1): #game을 시작하는 함수
        '''
        Call this function to initiate the game
        
        start_user: if its 0, start by "server" and if its 1, start by "client"
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.last_click = 0
        self.create_board_frame()
        self.create_status_frame()
        self.create_result_frame()
        self.create_debug_frame()
        self.state = self.active
        if start_user == self.myID: #시작하는 사람, client
            self.my_turn = 1    #내 차례이면 my_turn 값이 1, 아니면 0
            self.user['text'] = 'X' #시작한 사람이 X
            self.computer['text'] = 'O' #상대방은 O로 표시
            self.l_status_bullet.config(fg='green')
            self.l_status['text'] = ['Ready']
        else: # 두번째. 내 차례가 아님, server
            self.my_turn = 0
            self.user['text'] = 'O'
            self.computer['text'] = 'X'
            self.l_status_bullet.config(fg='red')
            self.l_status['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,()) #tkinter update를 위해 필요. 멈추지 않게 하기 위함
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def quit(self):
        '''
        Call this function to close GUI
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.destroy()
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def my_move(self, e, user_move):    #버튼을 누르면 이 함수로 들어간다. send_move에서 처리함.
        '''
        Read button when the player clicks the button
        
        e: event
        user_move: button number, from 0 to 8 
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        
        # When it is not my turn or the selected location is already taken, do nothing
        if self.board[user_move] != 0 or not self.my_turn:
            return
        # Send move to peer 
        valid = self.send_move(user_move)
        
        # If ACK is not returned from the peer or it is not valid, exit game
        if not valid:
            self.quit()
            
        # Update Tic-Tac-Toe board based on user's selection
        self.update_board(self.user, user_move)
        
        # If the game is not over, change turn
        if self.state == self.active:    
            self.my_turn = 0
            self.l_status_bullet.config(fg='red')
            self.l_status ['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def get_move(self): # 상대방의 결과 값을 받음
        '''
        Function to get move from other peer
        Get message using socket, and check if it is valid
        If is valid, send ACK message
        If is not, close socket and quit
        '''
        ###################  Fill Out  #######################
        
        # get message using socket
        msg = self.socket.recv(SIZE).decode()
       
        #msg_valid_check: msg의 valid함을 check하는 변수
        msg_valid_check = False 
        
        #check_msg를 통해 받은 msg가 format에 맞는지 valid 체크
        if check_msg(msg,self.send_ip) :
            msg_valid_check = True
            # check_msg 함수에는 ACK,SEND,RESULT를 구분할 수 없으므로, split을 하여 SEND인 경우에만 valid하게 확인
            p_msg=[]
            for s in re.split('[ /\r\n:]',msg):
                if s!='':
                    p_msg.append(s)
            if p_msg[0]!="SEND":
                msg_valid_check = False 
        
        # Message is not valid, quit
        if msg_valid_check==False:
            self.socket.close()   
            self.quit()
            return
        else:  # If message is valid - send ack 
            #ack를 보내기 위해서 p_msg에 msg를 파싱한 정보 저장
            p_msg=[]
            for s in re.split('[ /\r\n:]',msg):
                if s!='' :
                    p_msg.append(s)
            
            # p_msg에서 row와 column 정보를 파싱하기 위해 파싱을 한 번 더 적용
            p_msg2=[]
            for s in re.split('[(),]',p_msg[6]):
                if s!='' :
                    p_msg2.append(s)
            

            #파싱해서 얻은 row와 col로 ack메세지 작성
            ack_msg ="ACK ETTTP/1.0\r\nHost:127.0.0.1\r\nNew-Move:("+ p_msg2[0] +"," + p_msg2[1] +")\r\n\r\n"
            #send ACK
            self.socket.send(ack_msg.encode())
            
            #received next-move
            loc = int(p_msg2[0])*3+ int(p_msg2[1])
            
            ######################################################   
            
            #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
            #update board and change turn
            self.update_board(self.computer, loc, get=True)
            
            if self.state == self.active:  
                self.my_turn = 1
                self.l_status_bullet.config(fg='green')
                self.l_status ['text'] = ['Ready']
            #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                

    def send_debug(self):
        '''
        Function to send message to peer using input from the textbox
        Need to check if this turn is my turn or not
        '''
        #내 차례가 아니면 discard input
        if not self.my_turn:
            self.t_debug.delete(1.0,"end")
            print("not my turn")
            return
        # get message from the input box
        d_msg = self.t_debug.get(1.0,"end")
        d_msg = d_msg.replace("\\r\\n","\r\n")   # msg is sanitized as \r\n is modified when it is given as input
        self.t_debug.delete(1.0,"end")
        
        ###################  Fill Out  #######################
        '''
        Check if the selected location is already taken or not
        '''

        #d_msg에서 파싱한 정보를 p_msg배열에 저장
        p_msg=[]
        for s in re.split('[ /\r\n:]',d_msg):
            if s!='' :
                p_msg.append(s)
        #p_msg 예시: p_msg= ['SEND', 'ETTTP', '1.0', 'Host', '127.0.0.1', 'New-Move', '(2,3)']
        
        #p_msg2에는 p_msg[6]에 저장된 row, column 정보를 파싱하여 저장
        p_msg2=[]
        for s in re.split('[(),]',p_msg[6]):
            if s!='' :
                p_msg2.append(s)
        #p_msg2에 저장된 row,col이 str이므로 int로 캐스팅
        row=int(p_msg2[0])
        col=int(p_msg2[1])
        
        #row, col 정보를 이용해 loc(누른 위치를 의미) 저장
        loc=row*3+col

        #차지 되어있던 칸인지 아닌지 먼저 판단, 눌렸다면 버리면 됨 아니라면 보낸다
        #이미 누른 보드인 경우, discard
        if self.board[loc] != 0:
            print("selected board")
            return False
        
        '''
        Send message to peer
        '''
        sendmsg = self.socket.send(d_msg.encode())
        
        '''
        Get ack
        '''
        # recieve ack
        ack_msg=self.socket.recv(SIZE).decode()
        
        # check ack msg if it is valid
        if check_msg(ack_msg,self.send_ip)==False : 
            return
        
        
        ######################################################  
        
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.update_board(self.user, loc)
            
        if self.state == self.active:    # always after my move
            self.my_turn = 0
            self.l_status_bullet.config(fg='red')
            self.l_status ['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
            
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
        
    def send_move(self,selection): 
        '''
        Function to send message to peer using button click
        selection indicates the selected button
        '''
        # send_move function : send msg to peer and get ack from peer. if ack is valid- return True, else return False
        row,col = divmod(selection,3) # selection : 보드에서 클릭한 위치. divmod을 통해 표시한 위치를 row,col로 받음
        
        ###################  Fill Out  #######################
        # send msg to peer that I clicked. 
        msg="SEND ETTTP/1.0\r\nHost:127.0.0.1\r\nNew-Move:("+ str(row) +"," + str(col) +")\r\n\r\n"
        self.socket.send(msg.encode())
        
        # get ack msg from peer
        ack_msg=self.socket.recv(SIZE).decode() 
        
        # check_msg를 통해 ack_msg가 valid한지 판단
        # ack_msg가 valid하지 않은 경우 False를 리턴
        if check_msg(ack_msg,self.send_ip)==False : 
            return False
        #ack_msg가 valid한 경우 True를 return
        return True
        ######################################################  

    
    def check_result(self,winner,get=False): #winner=player['Name']="ME","YOU"
        '''
        Function to check if the result between peers are same
        get: if it is false, it means this user is winner and need to report the result first
        '''
        # no skeleton
        ###################  Fill Out  #######################
        
        #각자의 보드에서 승자가 나옴. ME 또는 YOU
        #loser가 winner =YOU 가 뜨면 제대로 결과 값이 나온것.
        #winner가 상대방에게 RESULT MSG 보냄
        
        if get==False: # winner임
            # 상대에게 자신이 이겼다고 RESULT 메세지를 보냄
            self.socket.send("RESULT ETTTP/1.0\r\nHost:127.0.0.1\r\nWinner:ME\r\n\r\n".encode())
            # get ack from loser
            ack=self.socket.recv(SIZE).decode()
            # 위너는 진 사람으로부터 받은 ack가 valid 한지 확인한다
            if check_msg(ack,self.send_ip)==False:
                return False
        elif get==True: #진 사람일 때
            # 진 사람은 이긴상대의 result msg를 받는다
            result=self.socket.recv(SIZE).decode() # 내가 이겼다는 메시지가 옴
            # 진 사람은 자신의 winner 값을 체크한다. winner가 YOU이어야하므로, ME일 경우엔 False
            if winner== "ME" :
                return False
            # msg valid 한지 확인한다음, valid 하면 위너에게 ack전송
            if check_msg(result,self.send_ip)==False:
                return False
            # 상대가 우승했다고 RESULT 메세지를 보냄
            self.socket.send("RESULT ETTTP/1.0\r\nHost:127.0.0.1\r\nWinner:YOU\r\n\r\n".encode())
                          
        else:
            #둘다 아니라면 리턴 false
            return False
        
        return True
        ######################################################  
        

        
    #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
    def update_board(self, player, move, get=False):
        '''
        This function updates Board if is clicked
        
        '''
        self.board[move] = player['value']
        self.remaining_moves.remove(move)
        self.cell[self.last_click]['bg'] = self.board_bg
        self.last_click = move
        self.setText[move].set(player['text'])
        self.cell[move]['bg'] = player['bg']
        self.update_status(player,get=get)

    def update_status(self, player,get=False):
        '''
        This function checks status - define if the game is over or not
        '''
        winner_sum = self.line_size * player['value']
        for line in self.all_lines:
            if sum(self.board[i] for i in line) == winner_sum: # 한줄완성
                self.l_status_bullet.config(fg='red') 
                self.l_status ['text'] = ['Hold'] # 상태는 hold
                self.highlight_winning_line(player, line) # winning line을 red로 칠하기
                correct = self.check_result(player['Name'],get=get) # 한줄 완성한 player(winner)의 결과 체크
                if correct:
                    self.state = player['win']
                    self.l_result['text'] = player['win']
                else:
                    self.l_result['text'] = "Somethings wrong..."

    def highlight_winning_line(self, player, line):
        '''
        This function highlights the winning line
        '''
        for i in line:
            self.cell[i]['bg'] = 'red'

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# End of Root class

def check_msg(msg, recv_ip): #self.recv_ip: src_addr
    '''
    Function that checks if received message is ETTTP format
    '''
    
    ###################  Fill Out  #######################
    # check_msg function : check if recieved msg is ETTTP format. if it is- return True, not- return False
    # parse recieved msg by using split function. below is the example of parsed array
    # array= ['SEND', 'ETTTP', '1.0', 'Host', '127.0.0.1', 'New-Move', '(2,3)']
    
    # parse msg and save it in array
    array= []
    for s in re.split('[ /\r\n:]',msg):
        if s!='' :
            array.append(s)
    # check if msg is SEND, ACK, RESULT (only those msg can be valid)
    try:
        if array[0]!="SEND" and array[0]!="ACK" and array[0]!="RESULT": 
            return False
        #ETTTP check
        if array[1]!="ETTTP": 
            return False
        #version check
        if array[2]!="1.0": 
            return False
        #ip address check
        if array[4]!=recv_ip: 
            return False
    except IndexError:
        # send_debug 메세지 때문에 작성한 부분입니다!
        # msg가 형식에 맞지 않으면 전송되지 않으므로 check_msg에 아무것도 전달받지 못하여 배열에 아무것도 들어가지 않는 경우가 생긴다
        # 이에 IndexError exception을 작성하여 터미널에 메세지가 출력되어 전송되지 않음을 시각적으로 확인할 수 있도록 했습니다
        print("msg is not received(because it is not valid) so we can not get array")
        return False
    # check if it is First-Move, Winner, New-Move
    # First-Move, Winner check
    if array[5]=="First-Move" or array[5]=="Winner":
        # First-Move와 Winner가 올 때에는 YOU나 ME만이 올 수 있다
        if array[6]!="YOU" and array[6]!="ME":
            return False
    # New-Move check
    if array[5]=="New-Move": #New-Move에는 row,col값이 있으므로 한번 더 파싱한다
        # get row,col value
        # ex: '(2,3)'을 파싱하여 rowcol=[2,3] 으로 만든다
        rowcol=[]
        for k in re.split('[(,)]',array[6]):
            if k!='' :
                rowcol.append(k)
        row=rowcol[0]
        col=rowcol[1]

        #if row,col is not integer, ValueError exception
        try:
            row=int(row)
            col=int(col)
        except ValueError:
            return False
        
    # if msg is valid - return True  
    return True
    ######################################################  
