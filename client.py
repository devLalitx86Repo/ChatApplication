import socket
import sys
import json

from threading import Thread

state = {}

def to_json(data):
    return json.dumps(data).encode()

def prepare_msg(type, message, **kwargs):
    message = {"sender": state["username"], "type": type, "message": message}
    if type == "connect":
        message["receiver"] = kwargs["receiver"]        
    return to_json(message)
    

def connect_response(server_socket):    
    print("Available Contacts:")
    for i, client in enumerate(state["avail_clients"]):
        print(i+1, ". ", client)
    print("\n")
    while not state['is_connected']:        
        message = input("Talk to: ")
        # json_msg = to_json({"type": "MSG","message": message})
        server_request = prepare_msg("connect", "Connect Request",receiver=message)
        server_socket.send(server_request)
        # server_response = server_socket.recv(2048).decode()
        # print(server_response)

def server_response(server_socket):
    while not state['is_connected']:
        message = server_socket.recv(2048).decode()
        print("<SERVER> : ",message)

def init_client(server_socket):
    json_msg = prepare_msg("INIT", "Hello !")
    server_socket.send(json_msg)
    server_response = server_socket.recv(2048).decode()
    # print("Initial Response: ", server_response)
    server_response = json.loads(server_response)
    state["avail_clients"] = server_response["clients"].split(",")


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    IP_ADDR = sys.argv[1]
    PORT = int(sys.argv[2])
    server_socket.connect((IP_ADDR, PORT))
    
    state['is_connected'] = False
    state["username"] = input("Enter your username: ")

    init_client(server_socket)
    # json_msg = to_json({"type": "INIT","username": uname})
    # server_socket.send(json_msg)
    # server_socket.recv(1024)
    # response = server_socket.recv(2048).decode()
    # print(response)

    thread_user_response = Thread(target=connect_response, args=(server_socket,))
    thread_server_response = Thread(target=server_response, args=(server_socket,))
    thread_user_response.start()
    thread_server_response.start()
    # thread_user_response.join()
    # thread_server_response.join()
    #lock
    while True:
        if state['is_connected']: break
        

if __name__ == "__main__":
    
    main()
    

    
    
    

    # def listen():
        
    #     while True:
    #         message = server.recv(2048)
    #         # print("<SERVER> : ",message.decode())
    #         if message:
    #             print(message.decode())
    #         else:
    #             break
    
    # start_new_thread(listen, ())

    # while True:
    #     message = input()
    #     json_msg = to_json({"type": "MSG","message": message})
    #     server.send(json_msg)

    # while True:

    #     socket_list = [sys.stdin, server]
    #     read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

    #     for sock in read_sockets:
    #         if sock == server:
    #             message = sock.recv(2048)
    #             print(message.decode())
    #         else:
    #             message = sys.stdin.readline()
    #             server.send(message.encode())
    #             sys.stdout.write("<You>")
    #             sys.stdout.write(message)
    #             sys.stdout.flush()

    # server.close()
