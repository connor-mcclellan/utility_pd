import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from hyperion.model import ModelOutput
from astropy.cosmology import Planck13
import astropy.units as u

image_dat_file_1 = '/home/cmcclellan1010/pdwork/output/manualconv/images/pd_raw_manualconv.dat'
image_dat_file_2 = '/home/cmcclellan1010/pdwork/output/autoconv/images/pd_raw_autoconv.dat'

f1 = np.loadtxt(image_dat_file_1)
f2 = np.loadtxt(image_dat_file_2)

diff = f1 - f2

OUTPUT_DIR = '/home/cmcclellan1010/pdwork/output/'

np.savetxt(OUTPUT_DIR+'difference.dat', diff)

# Image data
path = '/home/cmcclellan1010/pdwork/output/manualconv/'
filename = 'example.134.rtout.image'
m = ModelOutput(path+filename)
redshift = 3.1
image_width = 200 #kpc
distance = Planck13.luminosity_distance(redshift).cgs.value
image = m.get_image(distance=distance, units='mJy')
w = image.x_max * u.cm
w = w.to(u.kpc)

# Plot the figure
fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.imshow(diff, cmap=plt.cm.viridis, origin='lower',
                extent=[-w.value, w.value, -w.value, w.value])
plt.xlim([-image_width,image_width])
plt.ylim([-image_width,image_width])

ax.tick_params(axis='both', which='major', labelsize=10)
ax.set_xlabel('x kpc')
ax.set_xlabel('y kpc')

plt.colorbar(cax,label='Flux (mJy)',format='%.0e')

# Plot title: File 1 - File 2
plt.title('Manual Convolution - Auto Convolution')

# Save figure
fig.savefig(OUTPUT_DIR+'difference.png', bbox_inches='tight',dpi=150)
