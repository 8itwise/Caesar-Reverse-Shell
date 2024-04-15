# Caesar Reverse Shell

<img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" alt="Python"> <img src="https://img.shields.io/badge/Elastic_Search-005571?style=for-the-badge&logo=elasticsearch&logoColor=white" alt="Elasticsearch"> <img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" alt="Linux"><img src="https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows"><img src="https://img.shields.io/badge/VirtualBox-21416b?style=for-the-badge&logo=VirtualBox&logoColor=white" alt="Virtualbox"><img src="https://img.shields.io/badge/Sqlite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="sqlite">

Caesar is a simple Python TCP reverse shell designed to manage multiple client connections simultaneously. Caesar is integrated with Elasticsearch to store the target's information, allowing for easy retrieval and analysis of data collected from connected targets. Additionally, images and audio files collected from connected clients will be stored in individual client folders named using their client ID which is assigned when a connection is made with the server.

Caesar serves as a prototype and is strictly intended for educational purposes only. The application includes a basic but effective demonstration of how reverse shell connections can be established and controlled remotely. While Python may not be the ideal choice for advanced malware development due to its limitations, this project provides a foundational understanding of how such malicious software operates.



## Setup Elasticsearch
* Before running Caesar's Server script, ensure that you have Elasticsearch installed and configured. Elasticsearch is used for storing and indexing target's exfiltrated data. Follow these steps to set up Elasticsearch:

* Install Elasticsearch: Download and install Elasticsearch from the official Elasticsearch website.

* Start Elasticsearch: Start the Elasticsearch service using the appropriate method for your operating system. Refer to the Elasticsearch documentation for detailed instructions on how to start the service.

* Configure Elasticsearch: Optionally, configure Elasticsearch settings such as cluster name, node settings, network host, etc., as per your requirements. Refer to the Elasticsearch documentation for guidance on configuration options.

* Verify Elasticsearch Setup: Confirm that Elasticsearch is running and accessible by visiting http://localhost:9200 in your web browser. You should see a JSON response indicating the Elasticsearch cluster status.

* Create Elasticsearch Index: Create an index in Elasticsearch to store the target's data. You can use the Elasticsearch API or tools like Kibana to create the index with the desired settings and mappings.



## Features

```

        Caesar Commands
             'guide': [Display Caesar's user commands]
             'clients':['lists clients within ES index']
             'connected':['lists all active connection within ES index']
             'shell (target ES Client_ID)':['selects a target and creates a session between the server and the client machine ']
             'delete (target ES Client_ID)': ['remove specified document from index']
             'delete all': ['remove all document from index']
             'get (target ES Client_ID)': ['retrieves indexed data of specified target ']
             'show fields (target ES Client_ID)': ['displays existing field for specified target']
             'field (target ES Client_ID) (FIELD NAME):  ['displays specified field']

        Client Commands                                                
            'quit':['quits the session and takes user back to Caesar ES interface']           
            'get (filename or path)':['Receieve specified file from target client']
            'send (filename or absolute path)':['send specified file to the target client']      
            'screenshot':['takes a screen shot of the client machine']
            'camshot':['captures an image from the client's webcam']  
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

```

## Example 

Reverse Shell Diagram\
![Picture3](https://github.com/8itwise/Caesar-Reverse-Shell/assets/18365258/01fbe7d9-9871-4f1c-8c1c-71bd657fd40a)



### Clients
Display previously connected clients and clients with an active connection to the server\
![Picture5](https://github.com/8itwise/Caesar-Reverse-Shell/assets/18365258/78420df0-11b1-4671-8dcb-87f66ae29ed4)



### Data Collected
The following Data is extracted from the target's machine when the client script is executed. 
![Screenshot 2023-06-19 011334](https://github.com/8itwise/Caesar-Reverse-Shell/assets/18365258/448a902f-f501-49bc-b148-00f41396f9e2)




### Reverse Shell
Get a reverse shell and interact with the tartget's machine
![Picture6](https://github.com/8itwise/Caesar-Reverse-Shell/assets/18365258/1f4e3bd2-05fd-4fd0-a6d8-7f1d9160c147)



### Display Extracted Data
![Picture2](https://github.com/8itwise/Caesar-Reverse-Shell/assets/18365258/c70617d0-a659-46ac-b31d-86a2c0672fb8)


### Browser History Summary
Get a summary of the target's browsing History
![Picture5](https://github.com/8itwise/Caesar-Reverse-Shell/assets/18365258/ce2b5867-1d96-4228-a34a-0f62f2ae9735)



### Browsing Active Times 
Rank target's most active browsing hour

![Picture3](https://github.com/8itwise/Caesar-Reverse-Shell/assets/18365258/93ba9d95-0fb8-4d72-8033-adf595a42a5d)

![Picture4](https://github.com/8itwise/Caesar-Reverse-Shell/assets/18365258/eeb3b180-0dc7-4de7-8297-406322aefa00)



### Examine Tragets's Browsing Data 
Display the web domains the target has visited and contents on the domain the target has viewed
![Picture2](https://github.com/8itwise/Caesar-Reverse-Shell/assets/18365258/a3f58e1a-a19a-45d4-8340-70439f4cd2e4)

![Picture7](https://github.com/8itwise/Caesar-Reverse-Shell/assets/18365258/6c4d0f54-265f-44b8-961f-ecf2ca8706dd)


### Examine Target's Youtube Data 
Display the youtube channels the target has watched and the videos on the channel the target has viewed
![Screenshot 2023-06-18 172115](https://github.com/8itwise/Caesar-Reverse-Shell/assets/18365258/afee1ef1-5a18-456f-a479-8e6643751461)
![Screenshot 2023-06-18 172438](https://github.com/8itwise/Caesar-Reverse-Shell/assets/18365258/7fc35cef-358a-4d4c-a088-340171860511)



## Installation

Caesar Reverse Shell requires Python 3 and certain dependencies. Use pip to install the required packages:

```
pip install -r requirements.txt
```


## Usage

### Server Component
* Install and configure Elasticsearch on a Linux system.
* Create an index in Elasticsearch specifically for the server program to store target information.
```
curl -X PUT "http://localhost:9200/your_index_name"
```
* Run the Caesar's server script on the Linux system with admin priviledges.

```
    sudo python3 main.py
```

### Client Component

* Run the Caesar's client script on Windows systems.
* Connect to the Caesar-Light server to initiate a reverse shell connection and provide remote access to the target system.


## Disclaimer

This code is intended for educational and informational purposes only. Use it responsibly and ensure compliance with applicable laws and regulations. Respect the privacy and security of others.  
The author of this code assume no liability and is not responsible for misuses or damages caused by any code contained in this repository in any event that, accidentally or otherwise, it comes to be utilized by a threat agent or unauthorized entity as a means to compromise the security, privacy, confidentiality, integrity, and/or availability of systems and their associated resources. In this context the term "compromise" is henceforth understood as the leverage of exploitation of known or unknown vulnerabilities present in said systems, including, but not limited to, the implementation of security controls, human or electronically-enabled.