#!/usr/bin/env python

import csv, sys

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
    print 'hello'
