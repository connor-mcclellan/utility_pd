import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from hyperion.model import ModelOutput
from astropy.cosmology import Planck13
import astropy.units as u
import os
import argparse

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

parser = argparse.ArgumentParser(description='Synthesize an image at either a single wavelength or by convolving many wavelengths with a filter.')
parser.add_argument('infile', type=str, help='Filename of the ".image" file.')
parser.add_argument('-w', '--wav', type=float, help='A single wavelength in nm, if producing a monochromatic image.')
parser.add_argument('-f', '--filterfile', type=str, help='The ".filter" file to be used if convolving multiple wavelengths.')
parser.add_argument('-d', '--dat', action='store_true', help='If enabled, saves a ".dat" file with image data.')
parser.add_argument('--vmin', type=float, help='Minimum of colorbar scale, in units of flux.')
parser.add_argument('--vmax', type=float, help='Maximum of colorbar scale, in units of flux.')


args = parser.parse_args()


path = os.path.dirname(args.infile)+'/'
if path == '':
    path = './'
filename = os.path.basename(args.infile)

m = ModelOutput(path+filename)

try:
    wav = args.wav/1000. #micron
except TypeError:
    pass

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



if args.filterfile is not None:
    # Manually combine wavelengths according to filter transmission function
    filter_file = np.loadtxt(args.filterfile)
    images = [image.val[0, :, :, i] for i in range(len(image.wav))]
    weights = filter_file[:,1]
    image_data = np.average(images, axis=0, weights=weights)
    image_suffix = os.path.splitext(args.filterfile)[0].split('/')[-1]
else:
    # Find the closest wavelength
    iwav = np.argmin(np.abs(args.wav - image.wav))
    image_data = image.val[0, :, :, iwav]
    image_suffix = str(int(args.wav))+'nm'

outfile = 'pdimageout_'+image_suffix
outfile_path = path+outfile

if args.dat:
    np.savetxt(outfile_path+'.dat', image_data)

#plot the beast
cax = ax.imshow(np.log(image_data), cmap=plt.cm.viridis, origin='lower', 
                extent=[-w.value, w.value, -w.value, w.value], vmin=args.vmin,
                vmax=args.vmax)

plt.xlim([-image_width,image_width])
plt.ylim([-image_width,image_width])
    

# Finalize the plot
ax.tick_params(axis='both', which='major', labelsize=10)
ax.set_xlabel('x kpc')
ax.set_xlabel('y kpc')


plt.colorbar(cax,label='log Flux (mJy)',format='%.0e')
plt.title(outfile+'.png')
fig.savefig(outfile_path+'.png', bbox_inches='tight',dpi=150)
