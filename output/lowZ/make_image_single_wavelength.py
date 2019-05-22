import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from hyperion.model import ModelOutput
from astropy.cosmology import Planck13
import astropy.units as u
import os

# ------------------------
# modifiable header
# ------------------------

path = '/home/cmcclellan1010/pdwork/output/lowZ/'
outpath = '/home/cmcclellan1010/pdwork/output/lowZ/'
filename = 'example.134.rtout.image'


m = ModelOutput(path+filename)
wav = 0.66 #micron
redshift = 0.001
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
MANUAL_FILTER_CONVOLUTION = True
MANUAL_FILTER_CONVOLUTION_FILE = '/home/cmcclellan1010/powderday/filters/STIS_clear_8.filter'

if MANUAL_FILTER_CONVOLUTION:
    filter_file = np.loadtxt(MANUAL_FILTER_CONVOLUTION_FILE)
    images = [image.val[0, :, :, i] for i in range(len(image.wav))]
    weights = filter_file[:,1]
    image_data = np.average(images, axis=0, weights=weights)
    image_suffix = 'manualconv'
else:
    # Find the closest wavelength
    iwav = np.argmin(np.abs(wav - image.wav))
    image_data = image.val[0, :, :, iwav]
    if len(image.wav) == 1:
        image_suffix = 'autoconv'
    else:
        image_suffix = str(int(1000*wav))+'nm'

# Save .dat file with image data
SAVE = True

output_file_path = outpath+'pd_'+image_suffix+'_'+os.path.splitext(MANUAL_FILTER_CONVOLUTION_FILE)[0].split('/')[-1]
file_path = 'pd_'+image_suffix+'_'+os.path.splitext(MANUAL_FILTER_CONVOLUTION_FILE)[0].split('/')[-1]

if SAVE:
    np.savetxt(output_file_path+'.dat', image_data)

#plot the beast
cax = ax.imshow(np.log(image_data), cmap=plt.cm.viridis, origin='lower', extent=[-w.value, w.value, -w.value, w.value])

plt.xlim([-image_width,image_width])
plt.ylim([-image_width,image_width])
    

# Finalize the plot
ax.tick_params(axis='both', which='major', labelsize=10)
ax.set_xlabel('x kpc')
ax.set_xlabel('y kpc')


plt.colorbar(cax,label='Flux (mJy)',format='%.0e')
plt.title(file_path+'.png')
fig.savefig(output_file_path+'.png', bbox_inches='tight',dpi=150)
