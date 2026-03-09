# AI N-Queens Search Visualizer

A professional, interactive visualization tool for the N-Queens problem using Dynamic Backtracking. This project demonstrates how AI search algorithms explore state spaces, handle conflicts, and backtrack to find valid solutions.

## Features

- **Dynamic Board Size**: Support for board sizes from 4x4 up to 12x12.
- **Interactive Chessboard**: Real-time animation of queen placements and removals using GSAP.
- **State-Space Search Tree**: Dynamic visualization of the search process using D3.js.
- **Step-by-Step Backtracking**: Detailed explanation for every move (attempt, conflict, success, backtrack).
- **Playback Controls**: Play, Pause, Step Forward/Backward, and Speed adjustment.
- **Solution Viewer**: Browse all found solutions after the algorithm completes.
- **PDF Report Generation**: Download a comprehensive summary of the search results and statistics.
- **Statistics Panel**: Real-time tracking of visited states, backtracks, solutions found, and runtime.

## Tech Stack

- **Backend**: Python, Flask, Flask-CORS
- **Frontend**: HTML5, CSS3 (TailwindCSS), JavaScript (ES6+)
- **Animations**: GSAP (GreenSock Animation Platform)
- **Visualization**: D3.js (Data-Driven Documents)
- **PDF Generation**: jsPDF

## Project Structure

```
n-queens-ai-visualizer/
├── backend/
│   ├── app.py             # Flask API entry point
│   ├── nqueen_solver.py   # N-Queens logic with state capture
├── frontend/
│   ├── index.html         # Dashboard structure
│   ├── style.css          # Custom styling & animations
│   ├── main.js            # App controller & API handling
│   ├── board.js           # Chessboard rendering logic
│   ├── graph.js           # D3.js Tree visualization
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

## Setup and Installation

### Prerequisites
- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, or Edge)

### 1. Set up the Backend
Navigate to the project directory and install dependencies:
```bash
pip install -r requirements.txt
```

Run the Flask server:
```bash
python backend/app.py
```
The server will start on `http://localhost:5000`.

### 2. Set up the Frontend
Since this is a static frontend with CDN dependencies, you can simply open the `frontend/index.html` file in your browser.

*Note: For the best experience, use a local development server like Live Server (VS Code extension) or search for your index file via the filesystem.*

## How to Use
1. **Select N**: Choose the size of the board (default is 4).
2. **Solve**: Click the 'SOLVE' button to start the algorithm.
3. **Control Playback**: Use the Play/Pause buttons or Step Forward/Backward to analyze the algorithm's performance.
4. **Adjust Speed**: Use the slider to slow down or speed up the visualization.
5. **View Solutions**: Once solved, use the dropdown menu at the bottom to jump to specific board solutions.
6. **Export**: Click 'PDF REPORT' to save the results.


