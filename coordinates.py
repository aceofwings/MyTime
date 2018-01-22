import math

Norig,Worig=43.092245, -77.685703#N lat, W long
Nend,Wend=43.079104, -77.653637#N
LatSize=Norig-Nend#Image Height in Decimal Degrees
LongSize=math.fabs(Worig-Wend)#Width
ImgWidth=1850
ImgHeight=984
xfix,yfix=-20,-10

#test coordinates
t1x,t1y=43.082182, -77.675866
t2x,t2y=43.084906, -77.681390
t3x,t3y=43.087068, -77.670777


#Degrees to Pixels
def deg2pix(lat,lon):
    x = math.trunc(ImgWidth * (lon-Worig) / LongSize) + xfix
    y = math.trunc(ImgHeight * (Norig-lat) / LatSize) + yfix
    return (x,y)

#decimal degree to Degree Minute Second
def dd2dms(x,y=0):
    d = math.trunc(x)
    m = math.trunc((math.fabs(x)*60)%60)
    s = (math.fabs(x)*3600)%60
    return (d,m,s)

#print('1: '+str(deg2pix(t1x,t1y)))
#print('2: '+str(deg2pix(t2x,t2y)))
#print('3: '+str(deg2pix(t3x,t3y)))
