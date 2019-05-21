import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import argparse
import os

parser = argparse.ArgumentParser(description='Plot a raw image file (.dat format) as a histogram of fluxes.')
parser.add_argument('filename', metavar='filename', type=str, help='filename of the .dat file')
parser.add_argument('-o', '--outfile', metavar='outfile', type=str, help='name of output matplotlib savefig file')
args = parser.parse_args()

if args.outfile is None:
    outfile = os.path.splitext(args.filename)[0]+'_histogram.png'
else:
    outfile = args.outfile
print('Outfile: '+outfile)

image_data = np.ndarray.flatten(np.loadtxt(args.filename))

fig = plt.figure()
ax = fig.add_subplot(111)

ax.hist(image_data[image_data != 0.0])
ax.set_xlabel('Flux (mJy)')
ax.set_ylabel('n')
plt.title('Histogram of Fluxes ({})'.format(args.filename))

if os.path.isfile(outfile):
    os.remove(outfile)
fig.savefig(outfile, bbox_inches='tight', dpi=150)
