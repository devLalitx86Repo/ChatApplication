import socket
import sys
import json

#import thread
from _thread import *

clients = {}
client_sockets = {}
client_unames = {}
client_ready=[]

def to_json(data):
    return json.dumps(data)

def connectClient(conn, addr):
    '''
    This function is called when a new client connects to the server.
    '''
    # conn.send("Welcome to the server".encode())
    while True:
        try:
            message = conn.recv(2048)
            if message:
                process_msg(message.decode(), conn, addr)
            else:
                print("Disconnected from: ", addr[0], ":", addr[1])
                
                if addr[1] in clients:
                    clients.pop(addr[1]) 
                break
        except:
            continue

def process_msg(message, conn, addr):
    print("Message from: ", addr[0], ":", addr[1], ":", message)
    message = json.loads(message)
    if message['type'] == 'INIT':
        username = message['sender']
        clients[addr[1]] = (username, conn)
        client_unames[username] = addr[1]
        # conn.send("Hello",username,"\n::: Welcome to the server :::".encode())
        str_message = ">> Hello " + username + "\n::: Welcome to the PyChat :::"
        response = {"type": "INIT","clients": get_clients() , "message": str_message}
        # print(response)
        conn.send(to_json(response).encode())
        print("New client connected: ", username, ":", addr[1])
    
    elif message['type'] == 'connect':
        avaliable=False
        status_msg="user not found"
        print("message------",message)
        if message['receiver'] in client_unames:
            avaliable=True
            status_msg="Connect Request successful"
            client_ready.append(message['sender'])
        response = {"type": "connect","status":avaliable ,"connect_to": message['receiver'], "message":status_msg }
        # print("connect------",response)
        conn.send(to_json(response).encode())
    
    elif message['type'] == 'MSG':
        send_to = message['send_to']
        print("Messege for ",send_to)
        if send_to in client_ready:
            response={'message':message['message'], "status":True ,'sender':message['sender']}
            port = client_unames[send_to]
            clients[port][1].send(to_json(response).encode())
            print("message sent")
        # print(client_ready)
        else: 
            response = {"type": "error","status":False ,"message":"client not avaliable" }
            print("responce: ",response)
            conn.send(to_json(response).encode())
            # print(client_ready,"----",response)
    
    else:
        print("Unknown message type: ", message['type'])

def get_clients():
    return ",".join(list(client_unames.keys()))

if __name__ == "__main__":

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    IP_ADDR = sys.argv[1]
    PORT = int(sys.argv[2])

    server.bind((IP_ADDR, PORT))
    server.listen(100)

    print("Server Initiated on: ", PORT)

    while True:
        conn, addr = server.accept()
        # print("Connected to: ", addr[0], ":", addr[1])
        # clients[addr[1]] = conn
        start_new_thread(connectClient, (conn,addr))

    conn.close()
    server.close()