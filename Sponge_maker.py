import rhinoscriptsyntax as rs
import math
import random
import packSphere as ps


numCurves = 0
numDivX = 12
numDivY = 8
numDivZ = 12

objectIds = rs.GetObjects("Pick some curves", rs.filter.curve)

#browse through all the curves
if objectIds:
    for id in objectIds: 
        #if numCurves == 5:
            #rs.SelectObject(id)
        numCurves+=1
    print "Number of curves", numCurves
    
box = rs.BoundingBox(objectIds)
if box:
    for i, point in enumerate(box):
        #rs.AddTextDot( i, point )
        if i == 0:
            minX = point[0]
            minY = point[1]
            minZ = point[2]
        if i == 6:
            maxX = point[0]
            maxY = point[1]
            maxZ = point[2]
            
print "BOUNDS:\nMin:", minX, minY, minZ, "\nMax:", maxX, maxY, maxZ, "\n"

stepX = (maxX - minX) / numDivX
stepY = (maxY - minY) / numDivY
stepZ = (maxZ - minZ) / numDivZ

boxes = rs.AddGroup("Boxes")

for x in range(numDivX):
    for y in range(numDivY):
        for z in range(numDivZ):
            # add box
            box = rs.AddBox(([minX+x*stepX,minY+y*stepY,minZ+z*stepZ],
            [minX+(x+1)*stepX,minY+y*stepY,minZ+z*stepZ],
            [minX+(x+1)*stepX,minY+(y+1)*stepY,minZ+z*stepZ],
            [minX+x*stepX,minY+(y+1)*stepY,minZ+z*stepZ],
            [minX+x*stepX,minY+y*stepY,minZ+(z+1)*stepZ],
            [minX+(x+1)*stepX,minY+y*stepY,minZ+(z+1)*stepZ],
            [minX+(x+1)*stepX,minY+(y+1)*stepY,minZ+(z+1)*stepZ],
            [minX+x*stepX,minY+(y+1)*stepY,minZ+(z+1)*stepZ]))
            
            # Group boxes
#            boxes = rs.AddObjectsToGroup(box, "Boxes")
            boxFaces = rs.ExplodePolysurfaces(box)
            
            # Calculate density
            density = 0
            for curveId in objectIds:
                 for faceId in boxFaces: 
                    intersection_list = rs.CurveSurfaceIntersection(curveId, faceId)
                    if intersection_list:
                        density += len(intersection_list)
            # Map density to radius
            topBound = min(stepX, stepY, stepZ) / 4
            dRad = topBound * (density / numCurves)
            
            # Density at a point
            print x, " ", y, " ", z, " >> ", density
            rs.AddSphere([minX+(x+0.5)*stepX,minY+(y+0.5)*stepY,minZ+(z+0.5)*stepZ],dRad)
            # ps.packSpheres(minX+x*stepX, 
            #                            minY+y*stepY,
            #                            minZ+z*stepZ,
            #                            stepX, stepY, stepZ,
            #                            0.1, # min radius
            #                            dRad) # max radius
            
            # Clean-up
            rs.DeleteObjects(boxFaces)
            #rs.DeleteObject(box)