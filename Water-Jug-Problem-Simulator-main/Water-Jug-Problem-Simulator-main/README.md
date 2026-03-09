# AI Water Jug Search Visualizer

A professional interactive web application that solves the classic **Water Jug Problem** using AI search algorithms (**BFS** and **DFS**). It features a modern 3D simulation of the jugs and a real-time state-space graph visualization.

## 🚀 Features

-   **3D Jug Simulation**: Visually see water filling, emptying, and pouring between jugs using Three.js and GSAP.
-   **State-Space Graph**: Observe the search tree grow as the algorithm explores different states using D3.js.
-   **Interactive Controls**: Play, pause, step forward/backward, and adjust simulation speed.
-   **Algorithm Comparison**: Compare Breadth-First Search vs. Depth-First Search in terms of path length and states visited.
-   **PDF Report**: Download a detailed solution report containing all the steps taken to reach the target.
-   **Modern UI**: Built with TailwindCSS for a sleek, dark-mode dashboard experience.

## 🛠️ Technology Stack

-   **Backend**: Python, Flask, Flask-CORS
-   **Frontend**: HTML5, CSS3, JavaScript (ES6+)
-   **Libraries**:
    -   [Three.js](https://threejs.org/) (3D Graphics)
    -   [D3.js](https://d3js.org/) (Network Graph)
    -   [GSAP](https://greensock.com/gsap/) (Animations)
    -   [TailwindCSS](https://tailwindcss.com/) (Styling)
    -   [jsPDF](https://github.com/parallax/jsPDF) (PDF Export)

## 📁 Project Structure

```text
water-jug-ai-visualizer/
├── backend/
│   ├── app.py           # Flask API Entry Point
│   ├── dfs_solver.py    # DFS Implementation
│   ├── bfs_solver.py    # BFS Implementation
├── frontend/
│   ├── index.html       # Main UI 
│   ├── style.css        # Custom Styles
│   ├── main.js          # App Logic & API Integration
│   ├── jug3d.js         # 3D Simulation Logic
│   ├── graph.js         # D3 Graph Logic
├── requirements.txt     # Python Dependencies
└── README.md            # Project Documentation
```

## ⚙️ Setup & Installation

### 1. Prerequisite
Ensure you have **Python 3.x** installed on your system.

### 2. Backend Setup
Navigate to the `backend` directory and install dependencies:
```bash
pip install -r requirements.txt
```

Run the Flask server:
```bash
python backend/app.py
```
The API will start at `http://localhost:5000`.

### 3. Frontend Setup
Simply open `frontend/index.html` in any modern web browser. 

> **Note**: For the best experience and to avoid potential CORS issues with local files, it's recommended to serve the frontend using a local server (e.g., Live Server in VS Code or `python -m http.server`).

## 🧠 Solvers Logic

-   **BFS**: Guarantees the shortest path to the solution by exploring all neighbors at the current depth before moving deeper.
-   **DFS**: Explores one path as deeply as possible before backtracking. Often finds a solution faster in terms of memory if the goal is deep, but doesn't guarantee the shortest path.

## 📄 Rules Applied
1. Fill Jug 1
2. Fill Jug 2
3. Empty Jug 1
4. Empty Jug 2
5. Pour Jug 1 → Jug 2
6. Pour Jug 2 → Jug 1


