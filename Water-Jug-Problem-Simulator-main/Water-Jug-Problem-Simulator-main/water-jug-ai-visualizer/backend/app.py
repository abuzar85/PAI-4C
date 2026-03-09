from flask import Flask, request, jsonify
from flask_cors import CORS
from dfs_solver import DFSSolver
from bfs_solver import BFSSolver

app = Flask(__name__)
CORS(app)

@app.route('/solve', methods=['POST'])
def solve():
    data = request.json
    jug1 = int(data.get('jug1', 4))
    jug2 = int(data.get('jug2', 3))
    target = int(data.get('target', 2))
    algorithm = data.get('algorithm', 'bfs').lower()
    
    if algorithm == 'dfs':
        solver = DFSSolver(jug1, jug2, target)
    else:
        solver = BFSSolver(jug1, jug2, target)
        
    result = solver.solve()
    
    # Check if a solution was found
    if not result['solution']:
        return jsonify({
            "error": "No solution possible with given parameters.",
            "solution": [],
            "visited": result['visited']
        }), 200

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
