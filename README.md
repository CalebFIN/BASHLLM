# BASHLLM

This tool automates the execution of Bash commands using AI, looping through tasks until successful completion is confirmed. It integrates with an AI model running on an LM Studio server to generate and verify commands, ensuring efficient task execution.

## Features

- **Automated Bash Command Execution**: Provides and executes AI-generated Bash commands for user-defined tasks.
- **Task Completion Verification**: Verifies if a task is completed, preventing redundant command execution.
- **Environment Variable Configuration**: Easily configurable via environment variables for LLM server details.

## Dependencies

- **LM Studio Server**: Ensure you have an LM Studio server running, which this tool communicates with to generate and verify Bash commands.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/CalebFIN/BASHLLM.git
   ```
2. Navigate to the directory:
   ```bash
   cd BASHLLM
   ```
3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Set up your environment variables in a `.env` file:
   ```
   LLM_SERVER_IP=your_server_ip
   LLM_SERVER_PORT=your_server_port
   ```
2. Run the tool:
   ```bash
   python main.py
   ```

3. Enter the task you want to perform when prompted.

## Example
```ps 
sudo python3 main.py
```

```ps
Enter the task you want to perform: install nmap and quickly check if port 22 on 192.168.1.1 is running anything

[Executing Command]: sudo apt-get update && sudo apt-get install -y nmap && nmap -p 22 192.168.1.1

[Bash Output]:
Reading package lists...
Reading package lists...
Building dependency tree...
Reading state information...
nmap is already the newest version (7.91+dfsg1+really7.80+dfsg1-2ubuntu0.1).
0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.
Starting Nmap 7.80 ( https://nmap.org ) at 2024-08-20 16:50 CDT
Nmap scan report for routerlogin.net (192.168.1.1)
Host is up (0.00088s latency).

PORT   STATE SERVICE
22/tcp open  ssh

Nmap done: 1 IP address (1 host up) scanned in 0.32 seconds


[INFO] The task has already been completed. Exiting loop.
Enter the task you want to perform:sudo python3 main.py
Enter the task you want to perform: install nmap and quickly check if port 22 on 192.168.1.1 is running anything
sudo apt-get update && sudo apt-get install -y nmap && nmap -p 22 192.168.1.1
[Executing Command]: sudo apt-get update && sudo apt-get install -y nmap && nmap -p 22 192.168.1.1
Executing command: echo 'y' | sudo apt-get update && sudo apt-get install -y nmap && nmap -p 22 192.168.1.1

[Bash Output]:
Reading package lists...
Reading package lists...
Building dependency tree...
Reading state information...
nmap is already the newest version (7.91+dfsg1+really7.80+dfsg1-2ubuntu0.1).
0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.
Starting Nmap 7.80 ( https://nmap.org ) at 2024-08-20 16:50 CDT
Nmap scan report for routerlogin.net (192.168.1.1)
Host is up (0.00088s latency).

PORT   STATE SERVICE
22/tcp open  ssh

Nmap done: 1 IP address (1 host up) scanned in 0.32 seconds


[INFO] The task has already been completed. Exiting loop.
Enter the task you want to perform:


```
