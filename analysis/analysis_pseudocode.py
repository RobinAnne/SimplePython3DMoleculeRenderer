# ===========================
# ===========================
# INIT OPTIONS
# ===========================
# ===========================


# ===========================
# 1. brute force every init
# ===========================

init = all bonds, all bondangles in range(0, 180, step)

bondcount ~= 100
bondOptions = 180/step
bondcombinations = (180/step)^100
=> ridiculous

=> only an option if excepting many good solutions and stopping after one or more solutions with goodness > G 
or if running for I iterations and chosing best one out of that.

# ===========================
# 2. exclude worst joint dims from init
# ===========================

init = all atoms, solve for non_worst joint dimensions analytically

# ===========================
# 3. exclude worst joint dim tetrahedrons from init
# ===========================

init = all tetrahedral atoms, solve for non_worst joint dimensions analytically


# ===========================
# ===========================
# BACKTRACKING OPTIONS
# ===========================
# ===========================

# ===========================
# 1. 
# ===========================





