# ♟️ gomoku-ai

An AI-powered Gomoku (Five in a Row) game with Minimax and Alpha-Beta Pruning algorithms.

## 🧠 AI Functions Overview

### 🔍 `evaluate_window(window, ai_symbol, opp_symbol)`
- Scores a line of 5 consecutive cells.
- Positive score → AI advantage.
- Negative score → Opponent advantage.

---

### 🧮 `evaluate_board(board_obj, ai_symbol)`
- Evaluates the entire board.
- Scans rows, columns, and diagonals.
- Uses `evaluate_window()` for scoring.

---

### 📍 `get_candidate_moves(board_obj, radius=1)`
- Returns empty cells within a given radius of existing moves.
- Reduces the search space for the AI to improve performance.

---

### 🤖 `minimax(board_obj, depth, maximizing, ai_symbol)`
- Classic Minimax algorithm for decision making.
- Recursively explores all possible game states up to a given depth.

---

### ⚡ `alphaBeta(board_obj, depth, alpha, beta, maximizing, ai_symbol)`
- Enhanced Minimax with Alpha-Beta Pruning.
- Skips branches that can't affect the final decision.
- More efficient than basic Minimax.

---
### Note 
  - if you want to change the way the ai plays go and change the depth if you increase it it will be slow because it will take time to explore the moves.
