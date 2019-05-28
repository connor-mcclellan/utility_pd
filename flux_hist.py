import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import argparse
import os

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

parser = argparse.ArgumentParser(description='Plot a raw image file (.dat format) as a histogram of fluxes.')
parser.add_argument('filename', metavar='filename', type=str, help='filename of the .dat file')
parser.add_argument('-o', '--outfile', metavar='outfile', type=str, help='name of output matplotlib savefig file')
parser.add_argument('--xmin', type=float, help='x-axis minimum in units of log flux')
parser.add_argument('--xmax', type=float, help='x-axis maximum in units of log flux')

args = parser.parse_args()

if args.outfile is None:
    outfile = os.path.splitext(args.filename)[0]+'_histogram.png'
else:
    outfile = args.outfile
print('Outfile: '+outfile)

image_data = np.ndarray.flatten(np.loadtxt(args.filename))

fig = plt.figure()
ax = fig.add_subplot(111)

nonzero = image_data[image_data != 0.0]

ax.hist(nonzero, bins=np.logspace(np.log(np.min(nonzero)), np.log(np.max(nonzero)), 75, base=np.e))

ax.set_xlabel('log Flux (mJy)')
ax.set_xscale('log')
ax.set_xlim(xmin=args.xmin, xmax=args.xmax)
ax.set_ylabel('n')
plt.title('{}'.format(args.filename))

if os.path.isfile(outfile):
    os.remove(outfile)
fig.savefig(outfile, bbox_inches='tight', dpi=150)
