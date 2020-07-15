from  math import *


def distance(p,q):

	
	#calculate the ditance between 2 points
	
	d = sqrt(p**2 + q**2)
	
	return(d) 



def convert(x,y,w,h):


	#obtain the rectangle angles

	w=w/2
	x1 = int(round(x-w))
	x2 = int(round(x+w))
	
	h=h/2
	y1 = int(round(y-h))
	y2 = int(round(y+h))


	return x1, y1, x2, y2
