import rhinoscriptsyntax as rs
import math
import random

def distanceBetweenPoints(p1,p2):
    return math.sqrt(((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2)+((p1[2]-p2[2])**2)) 

def packSpheres(xP, yP, zP, bXsize, bYsize, bZsize, rMin, rMax):
#    xP= rs.GetReal("X = ", 0, 0)
#    yP= rs.GetReal("Y = ", 0, 0)
#    zP= rs.GetReal("Z = ", 0, 0)
#    
#    bXsize= rs.GetReal("X size = ", 50, 0)
#    bYsize= rs.GetReal("Y size = ", 50, 0)
#    bZsize= rs.GetReal("Z size = ", 75, 0)
    
    #tch=cmds.checkBox('touch',q=1, v=1)
    
    #sLim=cmds.checkBox( 'sLimit',q=1, v=1)
    #sizeLimit=cmds.floatField('szLimit',q=1, v=1)
    sLim = 1;
    tch=1;
    
    bXmin=xP-(bXsize/2)
    bYmin=yP-(bYsize/2)
    bZmin=zP-(bZsize/2)
    
    bXmax=xP+(bXsize/2)
    bYmax=yP+(bYsize/2)
    bZmax=zP+(bZsize/2) 
    
    bMin=[bXmin,bYmin,bZmin]
    bMax=[bXmax,bYmax,bZmax]
    
#    rMin= rs.GetReal("Min radius = ", 2, 0)
#    rMax= rs.GetReal("Max radius = ", 3, 0)
    closestPoint=random.uniform(rMin,rMax)
    
    if sLim==0:
    	sizeLimit=rMax
    else:
    	sizeLimit=10.0 #hack todo think about this
    
    iterations = 10000
    numSpheres = 1000
    #iterations= rs.GetReal("Iterations = ", 100000, 1000)
    #numSpheres= rs.GetReal("Number of spheres = ", 1000, 100)
    sphereCount=0
    
    killIt=0
    fitInside=1
    
    temp=[0.0,0.0,0.0]
    posList = [temp]*int(iterations)
    radList=[0.0]*int(iterations)
    
    print "Start packing ..."
    
    for i in range (iterations):
    	if i >0:
    		closestPoint=1000000000000.0
    		killIt=0
    	if i==0:
    		newPos=[random.uniform(bXmin+rMax,bXmax-rMax),random.uniform(bYmin+rMax,bYmax-rMax), random.uniform(bZmin+rMax,bZmax-rMax)]
    	else:
    		newPos=[random.uniform(bXmin,bXmax),random.uniform(bYmin,bYmax), random.uniform(bZmin,bZmax)]
    	for j in range (sphereCount):
    		if killIt==1:
    			#print sphereCount ,' number of spheres were drawn.'
    			break
    		distToEdge=(distanceBetweenPoints(newPos,posList[j]) -radList[j])
    		if distToEdge<rMin:
    			killIt=1
    			#print sphereCount ,' number of spheres were drawn.'
    			break
    		if distToEdge<closestPoint:
    			closestPoint=distToEdge
    		if fitInside==1:
    			for k in range (3):
    				if (newPos[k]-distToEdge)<bMin[k]:
    					distToEdge= newPos[k]-bMin[k]
    					if distToEdge<closestPoint:
    						if tch==0:
    							closestPoint=distToEdge
    						else:
    							killIt=1;
    					if closestPoint<rMin:
    						killIt=1
    						#print sphereCount ,' number of spheres were drawn.'
    						break
    				if (distToEdge+newPos[k])>bMax[k]:
    					distToEdge= bMax[k]-newPos[k]
    					if distToEdge<closestPoint:
    						if tch==0:
    							closestPoint=distToEdge
    						else:
    							killIt=1;
    	if rMax<closestPoint:
    		if tch==1:
    			killIt=1
    		else :
    			closestPoint=rMax   
    	if killIt==0:
    		if rMin<=closestPoint<=rMax:
    			posList[sphereCount]=newPos
    			radList[sphereCount]=closestPoint
    			if closestPoint <= sizeLimit:
    				centerPt = (posList[sphereCount][0],posList[sphereCount][1],posList[sphereCount][2]) 
    				rs.AddSphere(centerPt, closestPoint)
    			sphereCount=sphereCount+1
    			killIt=1
    
    	if sphereCount==numSpheres:
    		#print sphereCount ,' number of spheres were drawn.'
    		break
    print sphereCount ,' of spheres were drawn.'