import argparse
import wget
import numpy as np
import astropy.units as u
import os
from pathch import pathch

parser = argparse.ArgumentParser(description='Grab and format a COSMOS filter file from a web address.')
parser.add_argument('-u', '--urls', type=str, nargs='+', help='Web address of one or more COSMOS filters.')
parser.add_argument('-l', '--urllist', type=str, help='name of a .txt file containing urls to use')
parser.add_argument('-o', '--outfile', type=str, help='name of output directory')

args = parser.parse_args()

url_list = []

if args.urllist is not None:
    with open(args.urllist, 'r') as txtfile_of_urls:
        url_list = txtfile_of_urls.readlines()
    url_list = [line.strip() for line in url_list]

if args.urls is not None:
    for url in args.urls:
        url_list.append(url)

existing_unit = u.Unit('angstrom')
desired_unit = u.Unit('micron')

for url in url_list:
    filename = wget.download(url)
    data = np.loadtxt(filename)
    data[:, 0] = data[:, 0]*existing_unit.to(desired_unit)
    new_filename = pathch(args.outfile, 
                          os.path.splitext(filename)[0]+'.filter', force=True)

    np.savetxt(new_filename, data)
    os.remove(filename)
    print('\nSaved {}'.format(new_filename))
