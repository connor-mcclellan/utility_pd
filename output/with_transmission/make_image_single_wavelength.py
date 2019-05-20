import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from hyperion.model import ModelOutput
from astropy.cosmology import Planck13
import astropy.units as u

# ------------------------
# modifiable header
# ------------------------

path = '/home/cmcclellan1010/pdwork/output/with_transmission/'
filename = 'example.134.rtout.image'


m = ModelOutput(path+filename)
wav = 0.98 #micron
redshift = 3.1
image_width = 200 #kpc

# ------------------------


distance = Planck13.luminosity_distance(redshift).cgs.value


# Extract the image for the first inclination, and scale to 300pc. We
# have to specify group=1 as there is no image in group 0.
image = m.get_image(distance=distance, units='mJy')


# Open figure and create axes
fig = plt.figure()
ax = fig.add_subplot(111)


# Calculate the image width in kpc
w = image.x_max * u.cm
w = w.to(u.kpc)


# Manually combine wavelengths according to filter transmission function
MANUAL_FILTER_CONVOLUTION = False
MANUAL_FILTER_CONVOLUTION_FILE = '/home/cmcclellan1010/powderday/filters/STIS_clear_8.filter'

if MANUAL_FILTER_CONVOLUTION:
    filter_file = np.loadtxt(MANUAL_FILTER_CONVOLUTION_FILE)
    all_wavs = [image.val[0, :, :, i] for i in range(len(image.wav))]
    image = np.average(all_wavs, axis=0, weights=filter_file[:,1])
    image_suffix = 'convolved'
else:
    # Find the closest wavelength
    iwav = np.argmin(np.abs(wav - image.wav))
    image = image.val[0, :, :, iwav]
    image_suffix = str(int(1000*wav))+'nm'

#plot the beast
cax = ax.imshow(np.log(image), cmap=plt.cm.viridis, origin='lower', vmin=0.0,
                extent=[-w.value, w.value, -w.value, w.value])


plt.xlim([-image_width,image_width])
plt.ylim([-image_width,image_width])
    

# Finalize the plot
ax.tick_params(axis='both', which='major', labelsize=10)
ax.set_xlabel('x kpc')
ax.set_xlabel('y kpc')

plt.colorbar(cax,label='Flux (mJy)',format='%.0e')

fig.savefig(path+'images/pd_image_'+image_suffix+'.png', bbox_inches='tight',dpi=150)
