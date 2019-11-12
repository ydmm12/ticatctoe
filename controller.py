from random import randrange

def begin():
    if randrange(2):
        o = first()
    else:
        o = [[0,0,0] for l in range(3)]
    return out(o), o, ''
 
def out(ttt):
    o = ''
    for x in range(3):
        z = [y for y in ttt[x]]
        o += ' {} | {} | {} \n'.format(*z).replace('5','X').replace('3','O').replace('0',' ')
        if x < 2:
            o += '--------------\n'
    return o
    
            
def turn(ttt):
    winner, ttt = process(ttt)
    o = out(ttt)
    w1 = check_win(ttt)
    if type(w1) is str:
        winner = w1
    return o, ttt, winner

def first():
    return (
        [
            [0, 0, 0],
            [0, 3, 0],
            [0, 0, 0]
        ]
    )

def process(ttt):
    winner = check_win(ttt)
    if type(winner) is str:
        if winner == 'draw':
            return winner, ttt
        return 'Win {}'.format(winner), ttt
    elif type(winner) is list:
        return '', create_out(winner, ttt)
    else:
        return '', determinate_turn(ttt)

def create_out(position, ttt):
    ttt[position[0]][position[1]] = 3
    return ttt
    
def check_win(ttt):
    r=create_combinations(ttt)
    n = True
    out = None
    for line in range(len(r)):
        if 0 in r[line]:
            n = False
        winner = probe_array(r[line])
        if winner:
            return winner
        elif sum(r[line]) in [6,10]:
            out = analize_line(r[line], line)
    if n:
        return 'draw'
    elif out:
        return out
    return None

def create_combinations(ttt):
    r=[l for l in ttt]
    for column in range(3):
        r.append([ ttt[0][column], ttt[1][column], ttt[2][column] ])
    r.append(
        [ttt[0][0], ttt[1][1], ttt[2][2]]
    )
    r.append(
        [ttt[0][2], ttt[1][1], ttt[2][0]]
    )
    return r

def probe_array(line):
    if sum(line) == 9:
        return 'System'
    elif sum(line) == 15:
        return 'Player'
    

def analize_line(line, i):
    if i < 3:
        return [i, line.index(0)]
    elif i < 6:
        return [line.index(0), i%3]
    elif i == 6:
        return [line.index(0), line.index(0)]
    else:
        return [line.index(0), (line.index(0)+1)*-1]

def determinate_turn(ttt):
    combinations = create_combinations(ttt)
    response = []
    level = 0
    if not ttt[1][1]:
        response = [1,1]
    else:
        for c in range(len(combinations)):
            response, level = compare_decision(combinations[c], c, response, level)
            if level == 1:
                response = verify_empty(ttt)
            if level == 3:
                response = verify_corners(combinations[c])
    return create_out(response, ttt)

def compare_decision(combination, type_line, response, level):
    if all([x == 0 for x in combination]): #Verify if doesn't exist any value in line
        new_level = 1
        new_response = [0,0]
    elif sum(combination) in [11, 13]: #Verify if line is filled
        new_level = 0
        new_response = []
    elif type_line in [1, 4]: #Verify information in center lines
        if sum(combination) == 5:
            new_level = 0
            new_response = [0,0]
        else:
            new_level = 0
    elif type_line in [6, 7]: #Verify information in diagonal lines
        if sum(combination) == 13:
            new_level = 3
            new_response = []
        else:
            new_level = 0
    elif type_line in [0, 2, 3, 5]:
        if sum(combination) == 8:
            new_level = 2
        else:
            new_level = 0
    response = new_response if new_level > level else response
    level = new_level if new_level > level else level
    return response, level

def verify_corners(combination):
    if combination[0] == combination[2]:
        response = put_in_center(ttt)
    else:
        response = put_in_corner(ttt)
    return response

def put_in_center(ttt):
    for r in [[0,1],[1,0],[1,2],[2,1]]:
        if ttt[r[0]][r[1]] == 0:
            return r
        
def put_in_corner(ttt):
    for r in [[0,0],[0,2],[2,0],[2,2]]:
        if ttt[r[0]][r[1]] == 0:
            return r
        
def verify_empty(ttt):
    for y in range(3):
        if sum(ttt[y]) == 3:
            x = ttt[y].index(0)
    return [y, x]
            