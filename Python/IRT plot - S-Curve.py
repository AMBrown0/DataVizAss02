# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 16:28:27 2021

@author: andy
"""

#import section
from matplotlib import pylab
import pylab as plt
import numpy as np

#sigmoid = lambda x: 1 / (1 + np.exp(-x))
def sigmoid(x):
    return (1 / (1 + np.exp(-x)))


#1/(1+e^(−a(θ−b)))  Derivitive = d/dθ(1/(1 + e^θ)) = -e^θ/(1 + e^θ)^2

def IRT_P2(a,b,theta):
    #a is the discrimination parameter
    #b is the difficulty parameter
    
    #theta ability level
    L=-a*(theta-b)
    print(L)

    return (1 / (1 + (np.exp(L))))

def IRT_P2_gradient(a,b,theta):
    
    #a=(np.exp(theta))**2
    #ePowTh=-np.exp(L)
    #IRT_P2_Gradient=
    
    #IRT_P2_Gradient=(np.exp(theta)/((1+(np.exp(theta))**2))
    #IRT_P2_Gradient=(1/(np.exp(a*(theta-b))   +1))
    
    
    #d/dx(1/(1 + e^(a (x - b)))) = -(a e^(a (x - b)))/(e^(a (x - b)) + 1)^2
    numerator=a*( np.exp(a*(theta-b))  )
    denominator=(np.exp(a*(theta-b)) + 1  )**2
    IRT_P2_Gradient=numerator/denominator
    print("Gradient={}".format(IRT_P2_Gradient))
    return IRT_P2_Gradient
    
    #derivative calculator | 
    #function to differentiate | 1/(e^(a (θ - b)) + 1)
    #differentiation variable | (invalid value)
#1/(1+e^(−a(θ−b)))  Derivitive = d/dθ(1/(1 + e^θ)) = -e^θ/(1 + e^θ)^2

def calc_line(m,x,c):
    y=(m*x)+c
    return y

mySamples = []
mySigmoid = []



range={"x_min":-3,"x_max":3,"y-min":0,"y-max":1}
resolution=100


#Rasch's model 1/(1+e^(−a(θ−b) ) )
#Item difficutlty 

b=0
a=-1




# generate an Array with value ???
# linespace generate an array from start and stop value
# with requested number of elements. Example 10 elements or 100 elements.
# 
#x = plt.linspace(range.get('x_min'),range.get('x_max'),10)
theta = plt.linspace(range.get('x_min'),range.get('x_max'),resolution)

# prepare the plot, associate the color r(ed) or b(lue) and the label 
plt.plot(theta, IRT_P2(a,b,theta), 'r', label='Reponse')
#plt.plot(y, sigmoid(y), 'b', label='linspace(-10,10,100)')

#Calcualte the gradient line at Theta=0
#Calculate the value of Sigmoid at Theta - this give c
c=IRT_P2(a,b,b)
m=IRT_P2_gradient(a,b,b)

gradient_line = plt.linspace(-1.0,1.0,resolution)
plt.plot(gradient_line+b, calc_line(m,gradient_line,c), 'b--', label='Gradient')


# Draw the grid line in background.
plt.grid()

# Title & Subtitle
#plt.title('P2')
plt.suptitle('Item Response Theory curve')

# place the legen boc in bottom right of the graph
plt.legend(loc='lower right')

# write the Sigmoid formula
plt.text(4, 0.8, r'$P(\theta)=\frac{1}{1+e^-Da{(\theta-b)}}$', fontsize=16)
value_text="a={}, b={}".format(a,b)
value_text="a={}".format(a)
plt.text(4, 0.6,  value_text, fontsize=14)

#resize the X and Y axes
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(1))
plt.gca().yaxis.set_major_locator(plt.MultipleLocator(0.1))
 
#Draw vriticle and horizontal line
#plt.plot([-3, b], [c, c], 'b--')
#plt.plot([b, b], [0, c], 'b--')


# plt.plot(x)
plt.xlabel(r'Ability ($\theta$)')
plt.ylabel('Probability (P)')

# create the graph
plt.show()