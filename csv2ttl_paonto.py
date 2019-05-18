#!/usr/bin/env python3
"""convert standardized csv files to turtle"""

import csv
from os import listdir
import sys

DIR = 'csvsPAonto/'

def find_csv_filenames(path_dir, suffix=".csv"):
    """get all filenames with suffix .csv from the specified directory"""
    filenames = listdir(path_dir)
    return [filename for filename in filenames if filename.endswith(suffix)]

def csv_to_array(csv_name):
    """import data from csv and return as an array"""
    file_path = DIR+csv_name
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file)
        return list(csv_reader)

def prefixes(array, x_offset=3, y_offset=2):
    """import all prefixes specified for ontology"""
    for i in range(x_offset, len(array)):
        print('@prefix ' + array[i][y_offset] + ' <' + array[i][y_offset+1] + '> . ')

def meta(array, x_offset=2, y_offset=4):
    """convert meta taxonomy sheet"""
    for col in range(x_offset, len(array[0]), 2):
        for row in range(y_offset, len(array)):
            if not array[row][col]:
                break
            print(':' + array[row][col] + ' \t' + array[y_offset-2][col]
                  + '\t' + array[y_offset-1][col] + ' . ')

def metamatrix(array, x_offset=3, y_offset=3):
    """convert matrix with meta relations"""
    for i in array:
        for idxj, j in enumerate(i):
            if j == 'x':
                print(':' + i[y_offset] + '\t rdfs:subClassOf [rdf:type owl:Restriction ; ')
                print('\t\towl:onProperty ' + array[x_offset-1][y_offset-1] + '; ')
                print('\t\towl:someValuesFrom' + '\t:' + array[x_offset][idxj] + ' ] . ')

def props(array, x_offset=3, y_offset=4):
    """convert detailed object and datatype definitions on TBox level"""
    for i in range(y_offset, len(array)):
        for j in range(x_offset, len(array[0])):
            if array[2][j]:
                if array[i][j] == 'x':
                    print(':' + array[i][2] + ' ' + array[2][j] + ' ' + array[3][j] + ' . ')
            elif array[3][j]:
                if array[i][j]:
                    print(':' + array[i][2] + ' ' + array[3][j] + ' ' + array[i][j] + ' . ')
            else:
                print('error: missing data')
                sys.exit(1)

def taxo(array, x_offset=2, y_offset=4):
    """convert sheet with taxonomies to ttl - subClassOf relations only"""
    for col in range(x_offset, len(array[0]), 3):
        for row in range(y_offset, len(array)):
            if not array[row][col+1]:
                break
            if array[row][col]:
                superclass = array[row][col]
            print(':' + array[row][col+1] + ' \t' + array[y_offset-2][col+1]
                  + '\t' + array[y_offset-2][col] + superclass + ' . ')

def nonfc(array, x_offset=2, y_offset=4):
    """convert sheet with self-defined non-functional relations to ttl"""
    for col in range(x_offset, len(array[0]), 3):
        for row in range(y_offset, len(array)):
            if not array[row][col+1]:
                break
            if array[row][col]:
                subject = array[row][col]
            print(':' + subject + ' \t' + array[y_offset-2][col+1]
                  + '\t' + array[y_offset-2][col] + array[row][col+1] + ' . ')

def matrix(array, x_offset=3, y_offset=3):
    """convert matrix with instance relations"""
    for i in array:
        for idxj, j in enumerate(i):
            if j == 'x':
                print(':' + i[y_offset] + '\t ' + array[y_offset-1][x_offset-1]
                      + '\t:' + array[y_offset][idxj] + ' . ')

def func(array, x_offset=4, y_offset=4):
    """convert sheet with (quasi) functional relationships to ttl"""
    for idxi in range(x_offset, len(array)):
        for idxj in range(y_offset, len(array[0]), 2):
            if array[idxi][idxj]:
                print(':' + array[idxi][2] + ' \t' + array[2][idxj]
                      + '\t\"' + array[idxi][idxj] + '\"' + array[3][idxj] + ' . ')

def print_csv_types(files, sheet_type):
    """transform csvs according to type; type can be general, tbox or abox"""
    for filename in files:
        array = csv_to_array(filename)
        if array[0][1] == sheet_type:
            print('# ' + filename)
            funcs = {'prefixes': prefixes,
                     'meta': meta,
                     'props': props,
                     'metamatrix': metamatrix,
                     'taxo': taxo,
                     'nonfc': nonfc,
                     'matrix': matrix,
                     'func': func}
            try:
                funcs[array[0][0]](array)
            except KeyError:
                print(filename + ' causes an error - unknown sheet type')
                sys.exit(1)

def main():
    """transform all suitable csv sheets to ttl format"""
    filenames = find_csv_filenames(DIR)

    print('# Prefixes')
    print_csv_types(filenames, 'general')

    print('\n')
    print('# TBox')
    print_csv_types(filenames, 'tbox')

    print('\n')
    print('# ABox')
    print_csv_types(filenames, 'abox')

main()
