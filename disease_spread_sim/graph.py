import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import random
from functools import partial

style.use('fivethirtyeight')
fig=plt.figure()
ax1=fig.add_subplot(1,1,1)

X=[0]
Y=[0]
def get_update(x,y):
    global X,Y
    X.append(x)
    Y.append(y)

def plotter(i):
    global X,Y

    ax1.clear()

    ax1.plot(X,Y,c='g')    #healthy
    ax1.plot(Y,X,c='r')    #dead
    #ax1.plot(X[:-1],Y[:-1],c='b')    #infected

ani=animation.FuncAnimation(fig,ploter,interval=10)
plt.show()
