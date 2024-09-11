# 🧩 CTF Maze Challenge

This project contains two main folders:

1. **Challenges**: which contains a Dockerfile that deploys three scripts in separate containers, each one listening on a different port (9997, 9998, and 9999).
2. **Solutions**: which contains three scripts to solve the three challenges.

## 📋 Requirements

Before running the scripts, ensure you have Docker installed on your system. You can also use Python if you prefer running the scripts from the **Solutions** folder directly.

## 🚀 Installation

### Option 1: Use Docker for the Challenges

1. **Navigate to the `Challenges` folder**:
```
cd Challenges
```

2. **Build the Docker image**:
```
docker build -t ctf-maze-challenges .
```

3. **Run the container**:
```
docker run -d -p 9997:9997 -p 9998:9998 -p 9999:9999 ctf-maze-challenges
```

This will launch the three scripts, each listening on ports 9997, 9998, and 9999.

### Option 2: Run the Scripts Manually

1. **Navigate to the `Solutions` folder**:
```
cd Solutions
```

2. **Create a virtual environment (optional but recommended)**:
```
python -m venv .venv
```

3. **Activate the virtual environment**:
   - On Windows:
     ```
     .venv\Scripts\activate
     ```
   - On Linux/MacOS:
     ```
     source .venv/bin/activate
     ```

4. **Install the required dependencies**:
```
pip install -r requirements.txt
```

## 🛠️ Usage

### 1. Deploy the challenges from the `Challenges` folder
Each challenge script is deployed on a specific port:

- Challenge 1: `0.0.0.0:9997`
- Challenge 2: `0.0.0.0:9998`
- Challenge 3: `0.0.0.0:9999`

### 2. Solve the challenges from the `Solutions` folder

Each solution script in the **Solutions** folder is designed to connect to its respective challenge and automatically solve it.

#### Solve Challenge 1:
```
python maze_challenge1_solution.py
```

This script will connect to port `9997` by default.

#### Solve Challenge 2:
```
python maze_challenge2_solution.py
```

This script will connect to port `9998` by default.

#### Solve Challenge 3:
```
python maze_challenge3_solution.py
```

This script will connect to port `9999` by default.

You can modify the scripts to change the IP address or port if necessary.

## 🔧 Notes
- Make sure the challenge containers are running before attempting to solve them.
- You can modify the scripts to adjust specific challenge parameters.

Have fun solving these challenges in the CTF! 🧠
