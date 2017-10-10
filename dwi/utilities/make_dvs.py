#!/usr/bin/env python

import pandas
import argparse
import numpy as np


parser = argparse.ArgumentParser(description='A script for putting multishell gradient tables into Siemens format. The gradient vectors will be scaled to acheive the desired b values. This is primarily design to handle files generated at http://www.emmanuelcaruyer.com/q-space-sampling.php')

parser.add_argument('infile', type=str, help='input table with shell, x, y and z columns')
parser.add_argument('outfile', type=str,  help='filename to write the gradient directions to')
parser.add_argument('--bvals', nargs='+', type=int, help='list of b values for each shell (e.g. 1000 2000 3000', default=1000)
parser.add_argument('--nb0', type=int, default=1, help='number of b0 acquisitions to intersperse in the sequence')

args = parser.parse_args()

table=pandas.read_table(args.infile,comment="#",header=None,names=['shell', 'x','y','z'])

shells = table.shell.unique()
shells.sort()

if len(args.bvals) != len(shells):
	raise Exception('The number of shells and b values must match') 

#relabel shells with b values
for i in range(len(shells)):
	table.loc[table.shell==shells[i], 'shell'] = args.bvals[i]*1.0

#scale each vector 
table.x = np.sqrt(table.shell/np.max(args.bvals))*table.x
table.y = np.sqrt(table.shell/np.max(args.bvals))*table.z
table.z = np.sqrt(table.shell/np.max(args.bvals))*table.z

#reindex existing directions and insert the b0 volumes
b0_idxs = np.arange(0,len(table), np.floor(len(table)/args.nb0))
new_idx = np.arange(0, len(table))

for i in b0_idxs:
	new_idx[int(i):]=new_idx[int(i):]+1
	table=table.append({'shell':0, 'x':0, 'y':0, 'z':0},ignore_index=True )


new_idx = np.hstack((new_idx,b0_idxs))
new_idx = new_idx.astype('int')

table['idx']=new_idx

table.set_index('idx',drop=False,inplace=True)
table.sort_index(inplace=True)


#save the table

fp = open(args.outfile,'w+')

fp.write("#intended b value: %d\n" % np.max(args.bvals))

fp.write("[directions=%d]\nCoordinateSystem=xyz\nNormalisation=none\n" % len(table))

for i,row in table.iterrows():
	fp.write("Vector[%d] = ( %f, %f, %f )\n" % (row.idx,row.x,row.y,row.z))

fp.close()
