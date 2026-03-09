from collections import deque

class BFSSolver:
    def __init__(self, jug1_cap, jug2_cap, target):
        self.jug1_cap = jug1_cap
        self.jug2_cap = jug2_cap
        self.target = target
        self.visited = []  # List of states in order of visiting
        self.visited_set = set() # For quick lookup

    def solve(self):
        # queue stores (state, path)
        # state is (jug1, jug2)
        # path is list of (state, rule)
        queue = deque([((0, 0), [((0, 0), "Initial State")])])
        self.visited = []
        self.visited_set = set()
        
        while queue:
            (curr_j1, curr_j2), path = queue.popleft()
            
            if (curr_j1, curr_j2) in self.visited_set:
                continue
                
            self.visited.append({
                "state": (curr_j1, curr_j2),
                "rule": path[-1][1] if path else "Start"
            })
            self.visited_set.add((curr_j1, curr_j2))
            
            if curr_j1 == self.target or curr_j2 == self.target:
                return {
                    "solution": [{"state": s, "rule": r} for s, r in path],
                    "visited": self.visited
                }
            
            # Generate next states
            possible_moves = self.get_moves(curr_j1, curr_j2)
            
            for next_state, rule in possible_moves:
                if next_state not in self.visited_set:
                    new_path = path + [(next_state, rule)]
                    queue.append((next_state, new_path))
                    
        return {"solution": [], "visited": self.visited}

    def get_moves(self, j1, j2):
        moves = [
            ((self.jug1_cap, j2), "Fill Jug 1"),
            ((j1, self.jug2_cap), "Fill Jug 2"),
            ((0, j2), "Empty Jug 1"),
            ((j1, 0), "Empty Jug 2"),
            # Pour J1 -> J2
            ((max(0, j1 - (self.jug2_cap - j2)), min(self.jug2_cap, j2 + j1)), "Pour Jug 1 → Jug 2"),
            # Pour J2 -> J1
            ((min(self.jug1_cap, j1 + j2), max(0, j2 - (self.jug1_cap - j1))), "Pour Jug 2 → Jug 1")
        ]
        # Filter out moves that don't change the state
        return [m for m in moves if m[0] != (j1, j2)]
