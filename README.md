# TicTacToe-AI 🧠🎮

![Python](https://img.shields.io/badge/Python-3.6+-blue) ![AI](https://img.shields.io/badge/AI-Minimax-green) ![Algorithm](https://img.shields.io/badge/Algorithm-Alpha--Beta--Pruning-orange)

A Tic-Tac-Toe game implemented using the **Minimax algorithm** with **Alpha-Beta pruning**.  
The AI plays optimally, ensuring it either **wins or draws every game**.

---

## Project Overview

This project is a **Tic-Tac-Toe game** where a human player can play against an AI.  
The AI uses the **Minimax algorithm** to evaluate all possible game states and choose the optimal move.  
**Alpha-Beta pruning** is applied to reduce the number of unnecessary evaluations, improving performance.

This project was completed as a **second-year undergraduate assignment** and includes a detailed report explaining the algorithms, implementation, and design choices.

---

## Features

- Play against an **intelligent AI** that never loses.
- Single-player mode.
- Command-line interface, easy to run.
- Includes a **project report** explaining algorithms and logic.
- Optimized performance using **Alpha-Beta pruning**.

---

## Project Structure<p>
TicTacToe-AI<p>
 1.Tic_tac_toe.py # Main Python code for the game<br>
 2.Report.pdf # Project report detailing implementation<br>
 3.README.md # Project documentation (this file)<br>

 
---

## How to Run

1. Ensure **Python 3.6+** is installed.
2. Clone the repository:
bash
git clone https://github.com/menewranvidu51-netizen/TicTacToe-AI.git
cd TicTacToe-AI

---

## Implementation Details

Minimax Algorithm:
Recursively evaluates all possible moves to determine the best strategy. The AI selects the move that maximizes its chance of winning.

Alpha-Beta Pruning:
Optimizes the Minimax process by pruning branches that will not affect the final decision, improving efficiency.

Game Logic:

Board represented as a 3x3(level 1), 4x4(level 2), 5x5(level 3) grid.<br>
Players take turns until a win, lose, or draw.<br>
AI always plays optimally.<br>

