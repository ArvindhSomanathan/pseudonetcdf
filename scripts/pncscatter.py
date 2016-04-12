#!/usr/bin/env python
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from PseudoNetCDF.coordutil import gettimes
import numpy as np
import os

def plot_scatter(ifiles, args):
    fig = plt.figure()
    sax = fig.add_subplot(111)#add_axes([.1, .15, .8, .8])
    split = 25
    ifilex = ifiles[0]
    ifiley = ifiles[1]
    for target in args.variables:
        sax.set_xlabel('Time (UTC)')
        varx = ifilex.variables[target]
        varxdesc = getattr(varx, 'description', None)
        vary = ifiley.variables[target]
        varydesc = getattr(vary, 'description', None)
        sax.set_ylabel(varydesc)
        sax.set_xlabel(varxdesc)
        del sax.lines[:]
        vmin = np.minimum(varx[:].min(), vary[:].min())
        vmax = np.maximum(varx[:].max(), vary[:].max())
        sax.plot([vmin, vmax], [vmin, vmax], color = 'k')
        varb = sax.plot(varx[:], vary[:], ls = 'none', marker = 'o', markeredgecolor = 'none')
        sax.set_xlim(vmin, vmax)
        sax.set_ylim(vmin, vmax)
        #plt.setp(sax.xaxis.get_ticklabels(),rotation = 45)
        figpath = args.outpath + target + '_scatter.png'
        fig.savefig(figpath)
        print figpath

if __name__ == '__main__':
    from PseudoNetCDF.pncparse import getparser, pncparse
    parser = getparser(plot_options = True, has_ofile = True)
    parser.epilog += """
    -----
box.py inobs inmod target [target ...]
inobs - path to obs
inmod - path to mod
target - variable name
"""
    ifiles, args = pncparse(plot_options = True, has_ofile = True, parser = parser)
    plot_scatter(ifiles, args)
