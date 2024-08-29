# 🧩 CTF Maze Challenge

This project contains two Python scripts: one for generating a maze in ASCII format and serving it over a TCP connection, and another for connecting to the server, receiving the maze, and automatically solving it.

## 📋 Requirements

Before running the scripts, make sure you have Python installed on your system. You will also need to install the necessary dependencies using the `requirements.txt` file.

## 🚀 Installation

1. **Create a virtual environment (optional but recommended):**
```
    python -m venv .venv
```

2. **Activate the virtual environment:**
```
    .venv\Scripts\activate
```

3. **Install the required dependencies using pip:**
```
pip install -r requirements.txt
```

## 🛠️ Usage
1. Generate and Serve the Maze  
This script generates a random maze using the mazelib library and serves it over a TCP connection.

Run the following command to start the server:
```
python maze_generator.py
```
The server will listen on `0.0.0.0` and port `9999` by default. You can change these values by editing the script.

2. Solve the Maze   
This script connects to the maze server, receives the maze in ASCII format, and solves it using `mazelib`.

Run the following command to solve the maze:
```
python maze_solver.py
```
This script will connect to the server at localhost:9999 by default. You can modify the host and port as needed by editing the script.

## 🔧 Notes
You can customize the size of the maze and other parameters by modifying the corresponding scripts.  

Make sure the maze server is running before executing the solve script.
Enjoy solving the maze in this CTF challenge! 🧠