from flask import Flask, request, jsonify
from flask_cors import CORS
from nqueen_solver import NQueenSolver

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend interaction

@app.route('/solve', methods=['POST'])
def solve_nqueens():
    data = request.get_json()
    if not data or 'n' not in data:
        return jsonify({'error': 'Invalid request components'}), 400
    
    n = int(data['n'])
    if n < 4 or n > 12:
        return jsonify({'error': 'N must be between 4 and 12 for visualization'}), 400

    solver = NQueenSolver(n)
    result = solver.solve()
    
    return jsonify({
        'status': 'success',
        'solutions': result['solutions'],
        'steps': result['steps'],
        'visited_states': result['visited_states'],
        'total_solutions': result['total_solutions'],
        'total_backtracks': result['total_backtracks'],
        'runtime': result['runtime']
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
