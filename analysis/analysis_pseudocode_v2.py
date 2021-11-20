# Structure of analysis program

# ==============================
# CONSTANTS
# ==============================

tolerance_function = f(alpha)
'''
    where
        f(0) = 0
        f(x) > 0 for all x element of (0, pi/2]
        e.g. (x*(b*PI/180)^(-1))^a
            where b is the angle at which f = 1 and a > 1 shapes the function
'''
max_tolerance = X #(optional)
    #solutions with at least one tolerance larger than this are discarded

# ==============================
# FUNCTIONS
# ==============================

def main(tolerances):
    inits = generate_init_sols()
    solve(inits)
    evaluate()
    printer()

def generate_init_sols():
    pass

def solve():
    e = examine()
    if   e == DONE:
        collect()
    elif e == CONTINUE:
        extend()
    elif e == ABORT:
        pass

def extend():
    for s in p_sol.active_sites:
        extend p_sol on active sites in all directions
        solve(p_sol)

def examine():
    if duplicate bonds:
        return ABORT
    if all bonds included:
        return DONE
    return CONTINUE

def evaluate():
    jointDifficulty, totalPieces = [], []
    for sol in allSols:
        jointDifficulty, totalPieces.append([sol])
        for joints in sol:
            if jointDim == 4:
                append 0
            if jointDim == 3:
                append 0.3
            if jointDim == 2:
                append 0.7
            if jointDim == 1:
                append 1
    
        tolerance_stats = []
        for tolerances in sol:
            sort(tolerances)
            tolerance_stats.append([mean, maximum, tolerances, weighted_mean, weighted_maximum, weighted_tolerances])
        
        append joint_difficulty
        append tolerance_stats
        append num_total_pieces

def printer():
    pass
    
# ==============================
# EXECUTION
# ==============================

main()
