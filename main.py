import numpy as np
import cv2
import collapse

CM = np.array([[1,1,0,0],\
               [1,1,1,0],\
               [0,1,1,1],\
               [0,0,1,1]])

T = CM.shape[0]

colors = [[125,125,0],[0,255,0],[0,255,255],[255,0,0]]

W = 125
H = 75

def create_map():
    
    TS = [ [list(range(T)) for j in range(W)] for i in range(H)]

    return TS

def show_map(TS):
    
    zoom = 10
    TS_col = np.zeros((H*zoom,W*zoom,3))

    for i in range (H):
        for j in range(W):

            if len(TS[i][j]) == 1:
                
                for c in range(zoom):
                    for d in range(zoom):
                        TS_col[(i-1)*zoom+c,(j-1)*zoom+d] = colors[TS[i][j][0]]

    cv2.imwrite('image___.png', TS_col)

def check_end(TS):

    max_len = 1
    cpt = 0
    for i in range(H):
        for j in range(W):
            if len(TS[i][j])==1:
                cpt += 1 
            if len(TS[i][j])>= max_len:
                max_len= len(TS[i][j])

    return max_len == 1 , cpt

def run():
    TS = create_map()

    finished = False
    progress = 0

    while not finished:
        i,j = collapse.choose_collapse(TS,W,H,T)
        TS,collaspe = collapse.collapse_cell(TS,i,j)
        TS = collapse.propagate_collapse(TS,i,j,W,H,CM)
        
        finished,progress = check_end(TS)
        progress = round(progress / H / W , 6) * 100

        print(progress)
    return TS

TS = run()
show_map(TS)