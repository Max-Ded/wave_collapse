from locale import LC_ALL
import numpy as np
import random

from sklearn import neighbors

def choose_collapse(TS,W,H,T):

    min_len = T
    min_i = 0
    min_j = 0

    random_sample = []

    for i in range(H):
        for j in range(W):

            if len(TS[i][j]) == min_len :
                random_sample.append((i,j))
            elif len(TS[i][j])<= min_len and len(TS[i][j])>1:

                min_len= len(TS[i][j])

                random_sample = [(i,j)]

                
    return random.sample(random_sample,1)[0]


def propagate_collapse(TS,source_i,source_j,W,H,CM):
    
    histo_source = [(source_i,source_j)]

    while len(histo_source)>0:

        source = histo_source.pop()

        neigh = neighbors(W,H,source[0],source[1])
        random.shuffle(neigh)

        has_changed = False

        for n in neigh: 
            
            sup_source = TS[source[0]][source[1]]
            sup_n = TS[n[0]][n[1]]

            new_sup_source,new_sup_n = merge_superposition(CM,sup_source,sup_n)

            if new_sup_source != sup_source :

                TS[source[0]][source[1]] = new_sup_source
                has_changed = True
            
            if new_sup_n != sup_n :
                
                TS[n[0]][n[1]] = new_sup_n
                has_changed = True

                if [n[0],n[1]] not in histo_source : 
                    histo_source.append([n[0],n[1]])

        if has_changed:
            histo_source.append(source)

    return TS

def neighbors(W,H,rowNumber, colNumber):
    result = []
    for rowAdd in range(-1, 2):
        newRow = rowNumber + rowAdd
        if newRow >= 0 and newRow <= H-1:
            for colAdd in range(-1, 2):
                newCol = colNumber + colAdd
                if newCol >= 0 and newCol <= W-1:
                    if (newCol == colNumber and newRow == rowNumber) or abs(colAdd) + abs(rowAdd) > 1 :
                        continue
                    result.append([newRow,newCol])
    return result

def merge_superposition(CM,sup_1,sup_2):

    new_sup_1 = []
    new_sup_2 = []  

    merged_matrix = np.array([[CM[a][b] for b in sup_2] for a in sup_1])

    for i in range(len(sup_1)):
        if not np.array_equal(merged_matrix[i,:] , np.zeros_like(sup_2)):

            new_sup_1.append(sup_1[i])

    
    for j in range(len(sup_2)):

        if not np.array_equal(merged_matrix[:,j] , np.zeros_like(sup_1)):

            new_sup_2.append(sup_2[j])
        

    return new_sup_1,new_sup_2


def collapse_cell(TS,i,j):

    superposition  =  TS[i][j]
    value = random.sample(list(superposition),1)[0]

    TS[i][j] = [value]

    return TS,value
