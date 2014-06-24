#!/usr/bin/env python

import csv, sys
import xrayutilities as xu
import matplotlib.pyplot as plt

def loadCSV(path):
    """loads a special csv-like file, result of RSM fit"""
    x = []; y = []; 
    zexp = []; zini = []; zfin = []; 
    dialect = csv.excel_tab
    commentchar = '#'
    with open(path, 'rb') as csvfile:
        reader = csv.reader(csvfile, dialect = dialect)
        try:
            for row in reader:
                if row[0].startswith(commentchar):
                    continue
                try:
                    x.append(float(row[0]))
                    y.append(float(row[1]))
                    zexp.append(float(row[2]))
                    zini.append(float(row[3]))
                    zfin.append(float(row[4]))
                except IndexError as e:
                    print("Line %d: %s in %s" % (reader.line_num, row, e))
        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % (path, reader.line_num, e))
    
    return x, y, zexp, zini, zfin
    
if __name__ == '__main__':
    path = '/home/vifactor/Research/Samples/9543/XRD/FIT_misfit_threading_v5.0/folder/3.5deg-2.0deg-rsm-5h_6_9543_224_small.ft'
    x, y, zexp, zini, zfin = loadCSV(path)
    
    gridder = xu.Gridder2D(25, 25)
    
    plt.figure()
    
    #Experimental map
    ax = plt.subplot(221)
    gridder(x, y, zexp)
    LOGINT = xu.maplog(gridder.data.transpose(),6,0)
    #draw rsm
    cs = ax.contourf(gridder.xaxis, gridder.yaxis, LOGINT, 25, extend='min')
    #annotate axis
    ax.set_xlabel(r'$Q_{x}$')
    ax.set_ylabel(r'$Q_{z}$')
    
    #Fit map
    ax = plt.subplot(223)
    gridder(x, y, zfin)
    LOGINT = xu.maplog(gridder.data.transpose(),6,0)
    #draw rsm
    cs = ax.contourf(gridder.xaxis, gridder.yaxis, LOGINT, 25, extend='min')
    #annotate axis
    ax.set_xlabel(r'$Q_{x}$')
    ax.set_ylabel(r'$Q_{z}$')
    
    plt.show()
