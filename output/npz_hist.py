import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathch import pathch
import argparse
import os

parser = argparse.ArgumentParser(description='Plot data (.npz format) as a histogram.')
parser.add_argument('filenames', metavar='filenames', type=str, nargs='+', help='Filenames of one or more data files')
parser.add_argument('-o', '--outfile', metavar='outfile', type=str, help='name of output matplotlib savefig file')
parser.add_argument('--xmin', type=float, help='x-axis minimum in units of log flux')
parser.add_argument('--xmax', type=float, help='x-axis maximum in units of log flux')
parser.add_argument('-b', '--bins', type=int, default=75, help='number of bins in the histogram')
args = parser.parse_args()

fig = plt.figure()
ax = fig.add_subplot(111)

alldata = []

for i in range(len(args.filenames)):

    if i==0:
        outfile_str = os.path.splitext(args.filenames[i])[0]
    else:
        outfile_str += '_&_'+os.path.splitext(os.path.basename(args.filenames[i]))[0]

    image_data = np.ndarray.flatten(np.load(args.filenames[i])['arr_0'])
    nonzero = image_data[image_data != 0.0]
    alldata.append(nonzero)

outfile = pathch(args.outfile, outfile_str+'_histogram.png')
print('Outfile: '+outfile)

flatdata = [value for image_data in alldata for value in image_data]

mindata = np.min(flatdata)
maxdata = np.max(flatdata)

xmin = np.log(args.xmin) if args.xmin is not None else np.log(mindata)
xmax = np.log(args.xmax) if args.xmax is not None else np.log(maxdata)

for i in range(len(alldata)):
    name = os.path.basename(args.filenames[i]).split('.npz')[0]
    ax.hist(alldata[i], bins=np.logspace(xmin, xmax, args.bins, base=np.e), 
            alpha=0.5, label=name, histtype='step')
    ax.text(0.01,0.95-0.05*i, '{} sum: {:.2f}'.format(name, np.sum(alldata[i])), transform=ax.transAxes)

ax.set_xlabel('Value (Units)')
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_ylabel('n')
plt.title('{}'.format(os.path.basename(outfile)))

box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height])

plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)

if os.path.isfile(outfile):
    os.remove(outfile)
fig.savefig(outfile, bbox_inches='tight', dpi=150)
