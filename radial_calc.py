import pynrc
import numpy as np
import pysynphot as S
import pdb
from astropy.table import Table
pynrc.setup_logging('WARN', verbose=False)

rGrid = np.arange(0,1.6,0.1)
#rGrid = np.arange(0,0.1,0.01)

spFlat = S.FlatSpectrum(5,fluxunits='flam')

bpK = S.ObsBandpass('johnson,k')

#for oneFilt in ['F444W','F200W']:
oneFilt = 'F444W'

satArr, sensArr = [], []
for onePt in rGrid:
    print('Working on r={}'.format(onePt))
    nrc = pynrc.NIRCam(filter=oneFilt,pupil='CIRCLYOT',mask='MASK430R',
                       wind_mode='WINDOW',xpix=320,ypix=320,offset_r=onePt,
                       offset_theta=90,read_mode='RAPID',ngroup=2,nint=1)
    
    sat = nrc.sat_limits(unit='vegamag',sp=spFlat)
    
    nrc.update_detectors(ngroup=11,read_mode='DEEP8',nint=16)

    sens = nrc.sensitivity(units='vegamag',nsig=200,sp=spFlat,bp=bpK)
    
    outString = "Filt={}, R={} arcsec, Saturation={:.3f} K mag, Sensitivity 200sig {:.3f} K mag"
#    print(outString.format(oneFilt,onePt,sat['satmag'],sens[0]['sensitivity']))
    
    satArr.append(np.round(sat['satmag'],3))
    sensArr.append(np.round(sens[0]['sensitivity'],3))

t=Table()
t['Rad (arcsec)'] = rGrid
t['Sat Mag Ks'] = satArr
t['Sens Mag Ks'] = sensArr

print(t)
t.write('output/coron_sat_sens_{}.csv'.format(oneFilt),overwrite=True)
