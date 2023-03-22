r = '\033[21m'+'\033[22m'+'\033[24m'+'\033[25m'+'\033[27m'+'\033[28m'+'\033[39m'+'\033[49m'

def rgb(r=0,g=255,b=50):
    return '\033[38;2;'+str(r)+';'+str(g)+';'+str(b)+'m'

def lrgb(color):
    return '\033[38;2;'+str(color[0])+';'+str(color[1])+';'+str(color[2])+'m'

def brgb(r=0,g=255,b=50):
    return '\033[48;2;'+str(r)+';'+str(g)+';'+str(b)+'m'

def lbrgb(color):
    return '\033[48;2;'+str(color[0])+';'+str(color[1])+';'+str(color[2])+'m'