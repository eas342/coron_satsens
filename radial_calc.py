import pynrc
import numpy as np

rGrid = np.arange(0,1.5,0.1)
#rGrid = np.arange(0,0.1,0.01)

for onePt in rGrid:
    print('Working on r={}'.format(onePt))
    nrc = pynrc.NIRCam(filter='F444W',pupil='CIRCLYOT',mask='MASK430R',
                       wind_mode='WINDOW',xpix=320,ypix=320,offset_r=onePt,
                       offset_theta=90)
    
