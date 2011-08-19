# -*- coding: utf-8 -*-
from PIL import Image
import cv,numpy,pylab,os,sys,glob
import scipy.signal as sig

l=[]
c=glob.glob('!*.jpg')
l=l+c
p=glob.glob('00*.jpg')
l=l+p
    
def resizeImage(filename,box):#up left point and down right point
    img=Image.open(filename)
    rim=img.crop(box)
    file,ext=os.path.splitext(filename)
    if rim.mode!='RGB':
        rim=rim.convert('RGB')
    rim.save(file+'d.jpg','JPEG')
        
    
    
def getMinWH():
    #get the minimum width and  height
    #os.chdir(dir)
   
    img=cv.LoadImageM(l[-1],cv.CV_LOAD_IMAGE_GRAYSCALE)
    pi=Image.fromstring("L",cv.GetSize(img),img.tostring())
    (w,h)=pi.size
    px=numpy.zeros([w,],dtype=float)
    py=numpy.zeros([h,],dtype=float)   
    for p in l:
        img=cv.LoadImageM(p,cv.CV_LOAD_IMAGE_GRAYSCALE)
        pi=Image.fromstring("L",cv.GetSize(img),img.tostring())
        imga=numpy.asarray(pi,dtype=float)
        #print imga.size
        imgapx=imga.sum(axis=0)
        print imgapx.size
        imgapy=imga.sum(axis=1)
        print imgapy.size
        imgapx=imgapx/(h*255)
        imgapy=imgapy/(w*255)
        px=numpy.add(px,imgapx)
        py=numpy.add(py,imgapy)
    
    px=px/len(l) 
    py=py/len(l)  
 
    #===========================================================================
    # get the index to resize the pictures
    # different strategy for x and y
    #===========================================================================
    pxm=sig.medfilt(px,101)
    pxmd=numpy.diff(pxm)
    pxmdm=sig.medfilt(pxmd,11)
    for i in range(pxmdm.size):
        if abs(pxmdm[i])<=0.001:
            pxmdm[i]=0
        else:
            pxmdm[i]=1
    xl=pxmdm[0:w/8].argmax()
    tmp=pxmdm[-w/8:]
    xr=w-tmp[::-1].argmax()
    
    pym=sig.medfilt(py,101)
    pymd=numpy.diff(pym)
    pymdm=sig.medfilt(pymd,11)
    for i in range(pymdm.size):
        if abs(pymdm[i])<=0.001:
            pymdm[i]=0
        else:
            pymdm[i]=1
    yu=pymdm[0:h/8].argmax()
    tmp=pymdm[-h/8:]
    yd=h-tmp[::-1].argmax()
#===============================================================================
# pxdd=abs(numpy.diff(px,2)).
# pydd=abs(numpy.diff(py,2))
# xl=pxdd[0:w/8].argmin()
# xr=pxdd[-w/8:].argmin()+7*w/8
# yu=pydd[0:h/8].argmin()
# yd=pydd[-h/8:].argmin()+7*h/8
#===============================================================================
    
    #===========================================================================
    # pxl=px[0:w/10]
    # pxlm=pxl.mean()
    # pxr=px[-w/10:]
    # pxrm=pxr.mean()
    # pxl=abs(pxl-pxlm)
    # xl=pxl.argmin()
    # pxr=abs(pxr-pxrm)
    # xr=9*w/10+pxr.argmin()
    # 
    # pyl=py[0:h/10]
    # pylm=pyl.mean()
    # pyr=py[-h/10:]
    # pyrm=pyr.mean()
    # pyl=abs(pyl-pylm)
    # yu=pyl.argmin()
    # pxr=abs(pyr-pyrm)
    # yd=9*h/10+pxr.argmin()
    #===========================================================================
    
    box=(xl,yu,xr,yd)
    return box

def testResize(): 
    box=getMinWH()
    print box
    for p in l:
        #print 'processing'+p 
        resizeImage(p,box)
        
def mergejpg(r,c):
    pl=glob.glob('*.jpg')
    img=Image.open(pl[0])
    ow=img.size[0]
    oh=img.size[1]
    nw=ow*c
    nh=oh*r
    
    j=0#col
    i=0#row
    
    for k in range(len(pl)):
        xl=ow*j
        xr=ow*(j+1)
        yu=oh*i
        yd=oh*(i+1)
        
        box=(xl,yu,xr,yd)
        if k%(c*r)==0:
            nim=Image.new(img.mode,(nw,nh),(255,255,255))
            
        tim=Image.open(pl[k])
        nim.paste(tim,box)
        
        if (k+1)%(c*r)==0:
            nim.save('new'+'0'*(6-len(str(k)))+str(k)+'.jpg','JPEG')
        
        j=(j+1)%c
        i=(i+1)%r

    
    
    
     
        