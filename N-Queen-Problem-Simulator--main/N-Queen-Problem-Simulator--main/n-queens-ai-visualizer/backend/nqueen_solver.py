import time

class NQueenSolver:
    def __init__(self, n):
        self.n = n
        self.solutions = []
        self.steps = []
        self.visited_states = 0
        self.node_count = 0
        self.board = [-1] * n  # board[row] = col
        self.backtracks = 0

    def is_safe(self, row, col):
        # Check this column on previous rows
        for i in range(row):
            if self.board[i] == col or \
               abs(self.board[i] - col) == abs(i - row):
                return False
        return True

    def solve(self):
        start_time = time.time()
        # Initial node (root)
        root_id = 0
        self.steps.append({
            'type': 'visit',
            'id': root_id,
            'parent_id': None,
            'description': 'Start Search',
            'board': [-1] * self.n
        })
        self.node_count += 1
        
        self._backtrack(0, root_id)
        
        runtime = round((time.time() - start_time) * 1000, 2)
        return {
            'solutions': self.solutions,
            'steps': self.steps,
            'visited_states': self.visited_states,
            'total_solutions': len(self.solutions),
            'runtime': runtime,
            'total_backtracks': self.backtracks
        }

    def _backtrack(self, row, parent_id):
        if row == self.n:
            # Found a solution
            solution = list(self.board)
            self.solutions.append(solution)
            self.steps.append({
                'type': 'solution',
                'description': 'Valid Solution Found!',
                'board': solution
            })
            return

        for col in range(self.n):
            self.visited_states += 1
            node_id = self.node_count
            self.node_count += 1

            # Step: Attempt placement
            self.steps.append({
                'type': 'attempt',
                'id': node_id,
                'parent_id': parent_id,
                'row': row,
                'col': col,
                'description': f'Trying Row {row}, Col {col}',
                'board': self.board[:row] + [col] + [-1] * (self.n - row - 1)
            })

            if self.is_safe(row, col):
                self.board[row] = col
                # Step: Success placing
                self.steps.append({
                    'type': 'success',
                    'id': node_id,
                    'row': row,
                    'col': col,
                    'description': f'Placed Queen at ({row}, {col})'
                })
                
                # Recurse
                self._backtrack(row + 1, node_id)
                
                # Backtrack
                self.backtracks += 1
                self.board[row] = -1
                self.steps.append({
                    'type': 'backtrack',
                    'row': row,
                    'col': col,
                    'description': f'Backtracking from ({row}, {col})'
                })
            else:
                # Step: Conflict
                self.steps.append({
                    'type': 'conflict',
                    'id': node_id,
                    'row': row,
                    'col': col,
                    'description': f'Conflict at ({row}, {col})'
                })
