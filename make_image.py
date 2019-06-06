import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from hyperion.model import ModelOutput
from pathch import pathch
import astropy.units as u
import os
import argparse


parser = argparse.ArgumentParser(description='Synthesize an image at either a single wavelength or by convolving many wavelengths with a filter.')
parser.add_argument('infile', type=str, help='Filename of the ".image" file.')
parser.add_argument('-o', '--outfile', type=str, help='Path and filename of the outputs.')
parser.add_argument('-w', '--wav', type=float, help='A single wavelength in microns, if producing a monochromatic image.')
parser.add_argument('-d', '--dat', action='store_true', help='If enabled, saves a ".dat" file with image data.')
parser.add_argument('--vmin', type=float, help='Minimum of colorbar scale, in units of ergs/s.')
parser.add_argument('--vmax', type=float, help='Maximum of colorbar scale, in units of ergs/s.')

args = parser.parse_args()

m = ModelOutput(pathch(args.infile))

if args.outfile is None:
    args.outfile = os.path.dirname(args.infile)

# Extract the image for the first inclination, and scale to 300pc. We
# have to specify group=1 as there is no image in group 0.
image = m.get_image(units='ergs/s')

# Open figure and create axes
fig = plt.figure()
ax = fig.add_subplot(111)

# Calculate the image width in kpc
w = image.x_max * u.cm
w = w.to(u.kpc)

# Find the closest wavelength
iwav = np.argmin(np.abs(args.wav - image.wav))
print('Input wavelength: {}'.format(args.wav))
print('Closest: {}'.format(image.wav[iwav]))
image_data = image.val[0, :, :, iwav]
default_image_suffix = '{:.4f}um'.format(image.wav[iwav])

# Save a .dat file, if desired
if args.dat:
    outf = pathch(args.outfile, 'pdimageout_'+default_image_suffix+'.dat')
    print('.dat outfile: {}'.format(outf))
    np.savetxt(outf, image_data)

#plot the beast
cax = ax.imshow(np.log(image_data), cmap=plt.cm.magma, origin='lower', 
                extent=[-w.value, w.value, -w.value, w.value], vmin=args.vmin,
                vmax=args.vmax)

# Finalize the plot
ax.tick_params(axis='both', which='major', labelsize=10)
ax.set_xlabel('x (kpc)')
ax.set_xlabel('y (kpc)')


plt.colorbar(cax,label='log Luminosity (ergs/s)',format='%.0e')

plot_outfile = pathch(args.outfile, 'pdimageout_'+default_image_suffix+'.png')

plt.title(os.path.basename(plot_outfile))
print('Plot outfile: {}'.format(plot_outfile))
fig.savefig(plot_outfile, bbox_inches='tight',dpi=150)
