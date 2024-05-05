import numpy as np
import matplotlib.pyplot as plt

def f(x):  #Define the function
    return x**2 - 2 * x     #Takes the input and returns an output.


if __name__ == '__main__':
    print('x , f(x):\n'+10*'-') #Print more readable values
    x = []
    fx  = []
    for i in range(-100,100):   #Run the function from -100 to 100
        print(i,f(i))           #Print the function input and output number.

        x.append(i)
        fx.append(f(i))


    plt.figure()
    plt.title('Function')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.plot(x,fx,label='x^2 -2*x')
    plt.legend()
    plt.show()