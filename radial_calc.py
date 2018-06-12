import matplotlib
matplotlib.use('Agg')
import pynrc
import numpy as np
import pysynphot as S
import pdb
from astropy.table import Table
import os
import matplotlib.pyplot as plt


pynrc.setup_logging('WARN', verbose=False)

innerGrid = np.arange(0,1.6,0.1)
#innerGrid = np.arange(1.5,1.6,0.1)
outerGrid = np.arange(1.6,3.2,0.2)

rGrid = np.hstack([innerGrid,outerGrid])

spFlat = S.FlatSpectrum(5,fluxunits='flam')

bpK = S.ObsBandpass('johnson,k')

for oneFilt,oneMask in zip(['F444W','F200W'],['MASK430R','MASK210R']):
    
   satArr, sensArr = [], []
   for onePt in rGrid:
#       print('Working on r={}'.format(onePt))
       nrc = pynrc.NIRCam(filter=oneFilt,pupil='CIRCLYOT',mask=oneMask,
                          wind_mode='WINDOW',xpix=320,ypix=320,offset_r=onePt,
                          offset_theta=90,read_mode='RAPID',ngroup=2,nint=1,
                          fov_pix=321)
       
       sat = nrc.sat_limits(unit='vegamag',sp=spFlat,force_full_fov=True,bp=bpK)
       
       nrc.update_detectors(ngroup=11,read_mode='DEEP8',nint=16)
       
       sens = nrc.sensitivity(units='vegamag',nsig=200,sp=spFlat,bp=bpK,
                              force_full_fov=True,use_bg_psf=False)
       
       outString = "Filt={}, R={} arcsec, Saturation={:.3f} K mag, Sensitivity 200sig {:.3f} K mag"
       print(outString.format(oneFilt,onePt,sat['satmag'],sens[0]['sensitivity']))
       
       satArr.append(np.round(sat['satmag'],3))
       sensArr.append(np.round(sens[0]['sensitivity'],3))

       dirName = "images_{}".format(oneFilt)
       if os.path.exists(dirName) == False:
          os.mkdir(dirName)
       
       outImgName = os.path.join(dirName,"psf_{}_{}.png".format(oneFilt,onePt))
       #fig, ax = plt.subplots()
       #ax.imshow(nrc.gen_psf())
       #fig.savefig(outImgName)

   ## Calculate direct image sat & sens
   nrc = pynrc.NIRCam(filter=oneFilt,wind_mode='WINDOW',xpix=320,ypix=320,
                      read_mode='RAPID',ngropu=2,nint=1)
   satDirect = nrc.sat_limits(unit='vegamag',sp=spFlat)
   nrc.update_detectors(ngroup=11,read_mode='DEEP8',nint=16)
   sensDirect = nrc.sensitivity(units='vegamag',nsig=200,sp=spFlat,bp=bpK)
   
   t=Table()
   t['Rad (arcsec)'] = np.round(rGrid,2)
   t['Sat Mag Ks'] = satArr
   t['Sens Mag Ks'] = sensArr
   t['Direct Sat Mag Ks'] = satDirect
   t['Direct Sens Mag Ks'] = sensDirect
   
   print(t)
   t.write('output/coron_sat_sens_{}.csv'.format(oneFilt),overwrite=True)
   
