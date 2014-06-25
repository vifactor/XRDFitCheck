#!/usr/bin/env python

from Tkinter import Tk
from tkFileDialog import askopenfilename
import csv, sys
import xrayutilities as xu
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

class fit_viewer(object):
    def __init__(self):
        self.fig=plt.figure()
        #layout
        self.fig.subplots_adjust(0.06,0.06,0.97,0.97,0.25,0.2)
        self.rsm_ax=plt.subplot2grid((8,4),(1,0),rowspan=7,colspan=2)
        self.qx_ax=plt.subplot2grid((8,4),(0,2),rowspan=4,colspan=2)
        self.qz_ax=plt.subplot2grid((8,4),(4,2),rowspan=4,colspan=2)
        
        button_ax = plt.subplot2grid((8,4),(0,0),colspan=2)
        self.load_button = Button(button_ax,'Load')
        self.load_button.on_clicked(self.do_work)
        
        #data gridder
        self.gridder = xu.Gridder2D(25, 25)
    
    def do_work(self, event):
        path = askopenfilename()
        x, y, zexp, zini, zfin = self.load_csv(path)
        self.draw_graphs(x, y, zexp, zini, zfin)
        
    def load_csv(self, path):
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
        
    def clear_subplots(self):
        """Clears the subplots."""
        for j in [self.rsm_ax, self.qx_ax, self.qz_ax]:
            j.cla()
    
    def draw_graphs(self, x, y, zexp, zini, zfin):
        
        self.clear_subplots()
        
        self.gridder(x, y, zexp)
        #Experimental map
        LOGINT = xu.maplog(self.gridder.data.transpose(),6,0)
        cs = self.rsm_ax.contourf(self.gridder.xaxis, self.gridder.yaxis, LOGINT, 25, extend='min')
        self.rsm_ax.set_xlabel(r'$q_{x}$')
        self.rsm_ax.set_ylabel(r'$q_{z}$')
        
        #qx exp scan
        qx,qxint = xu.analysis.line_cuts.get_qx_scan(self.gridder.xaxis,
                                                    self.gridder.yaxis,
                                                    self.gridder.data, 0.0)
        self.qx_ax.semilogy(qx, qxint, "k-")
        self.qx_ax.set_xlabel(r'$q_{x}$')
        self.qx_ax.set_ylabel(r'Intensity')
        #qz exp scan
        qz,qzint = xu.analysis.line_cuts.get_qz_scan(self.gridder.xaxis,
                                                    self.gridder.yaxis,
                                                    self.gridder.data, 0.0)
        self.qz_ax.semilogy(qz, qzint, "k-")
        self.qz_ax.set_xlabel(r'$q_{z}$')
        self.qz_ax.set_ylabel(r'Intensity')
        
        
        self.gridder(x, y, zfin)
        #Fit map
        LOGINT = xu.maplog(self.gridder.data.transpose(),6,0)
        #draw rsm
        cs = self.rsm_ax.contour(self.gridder.xaxis, self.gridder.yaxis, LOGINT, 25, extend='min')
        
        #qx fit scan
        qx,qxint = xu.analysis.line_cuts.get_qx_scan(self.gridder.xaxis,
                                                    self.gridder.yaxis,
                                                    self.gridder.data, 0.0)
        self.qx_ax.semilogy(qx, qxint, "g-")
        #qz fit scan
        qz,qzint = xu.analysis.line_cuts.get_qz_scan(self.gridder.xaxis,
                                                    self.gridder.yaxis,
                                                    self.gridder.data, 0.0)
        self.qz_ax.semilogy(qz, qzint, "g-")
        
        plt.draw()

if __name__ == '__main__':
    viewer = fit_viewer()
    plt.show()
