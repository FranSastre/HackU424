# 🧠 Brainfuck Challenge - Find the Flag!

In this challenge, you're given a mysterious piece of **Brainfuck** code that hides a secret flag. Your goal is to decode and execute the Brainfuck code to reveal the flag! 🏁

## 📋 Requirements

Before you start, make sure you have a Brainfuck interpreter installed. You can either:

1. Use an **online Brainfuck interpreter** (simply search "Brainfuck interpreter" in your browser).
2. Install a local interpreter like **Python's Brainfuck interpreter**.

To install the Brainfuck interpreter in Python, run:
```
pip install bf-interpreter
```

Alternatively, you can use any Brainfuck interpreter you prefer.

## 🚀 Instructions

1. **Get the Brainfuck Code**  
   You'll be given a string of Brainfuck code, like the one below. Your mission is to execute this code to uncover the hidden flag.

   Example Brainfuck code:
   ```
   +++++ [ > ++++++ <- ] > +++++ . 
   ```

   This simple Brainfuck code prints the character `A`. Similarly, the challenge code will print the flag once executed correctly.

2. **Run the Brainfuck Code**  
   Use your interpreter to run the code. Here are two ways to do it:

   ### Option 1: Use an Online Interpreter

   - Copy and paste the Brainfuck code into an online Brainfuck interpreter.
   - Run the code and observe the output—it should be your flag! 🚩

   ### Option 2: Use a Local Interpreter

   - Save the Brainfuck code in a file, say `challenge.bf`.
   - Run it using your interpreter. For example, using Python:
     ```
     bf-interpreter challenge.bf
     ```

   - The output will be displayed in your terminal, revealing the flag.

## 🛠️ Example

The Brainfuck code you receive is:
```
++++++++++[>+>+++>+++++++>++++++++++<<<<-]>>>++.-------.++.++++++++.<++++++++++++++++++++++.>++++++++++.>+++++++++++++++++++++++.<+++++++++++++++++.>---------.<<---.++.>--.-----.+++.>.<<+.---.>>----.<---.>++++++++++++....<<----------------.>>+++.
```

You can decode it [here](https://www.dcode.fr/brainfuck-language)



## Good luck, and may the Brainfuck be with you! 🧩
