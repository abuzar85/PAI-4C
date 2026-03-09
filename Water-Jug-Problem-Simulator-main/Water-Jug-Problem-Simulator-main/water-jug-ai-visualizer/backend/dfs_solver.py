class DFSSolver:
    def __init__(self, jug1_cap, jug2_cap, target):
        self.jug1_cap = jug1_cap
        self.jug2_cap = jug2_cap
        self.target = target
        self.visited = []
        self.visited_set = set()

    def solve(self):
        # stack stores (state, path)
        stack = [((0, 0), [((0, 0), "Initial State")])]
        self.visited = []
        self.visited_set = set()
        
        while stack:
            (curr_j1, curr_j2), path = stack.pop()
            
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
            
            # Generate next states (reversed to maintain order if desired)
            possible_moves = self.get_moves(curr_j1, curr_j2)
            
            for next_state, rule in reversed(possible_moves):
                if next_state not in self.visited_set:
                    new_path = path + [(next_state, rule)]
                    stack.append((next_state, new_path))
                    
        return {"solution": [], "visited": self.visited}

    def get_moves(self, j1, j2):
        moves = [
            ((self.jug1_cap, j2), "Fill Jug 1"),
            ((j1, self.jug2_cap), "Fill Jug 2"),
            ((0, j2), "Empty Jug 1"),
            ((j1, 0), "Empty Jug 2"),
            ((max(0, j1 - (self.jug2_cap - j2)), min(self.jug2_cap, j2 + j1)), "Pour Jug 1 → Jug 2"),
            ((min(self.jug1_cap, j1 + j2), max(0, j2 - (self.jug1_cap - j1))), "Pour Jug 2 → Jug 1")
        ]
        return [m for m in moves if m[0] != (j1, j2)]
