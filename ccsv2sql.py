#!/usr/bin/env python
"""
ccsv2sql
Utility to convert a CSV file to a SQL dump.

Copyright 2015 Sam Saint-Pettersen.
Licensed under the MIT/X11 License.

Use -h switch for usage information.
"""
import sys
import csv
import os
import re
import datetime
import argparse

signature = 'ccsv2sql 1.0.3 (https://github.com/stpettersens/ccsv2sql)'

def displayVersion():
	print('\n' + signature)

def displayInfo():
	print(__doc__)

def ccsv2sql(file, out, separator, db, comments, verbose, version, info):
	
	if len(sys.argv) == 1:
		displayInfo()
		sys.exit(0)

	if file == None and out == None:
		if verbose == False and version == True and info == False:
			displayVersion()

		elif verbose == False and version == False and info == True:
			displayInfo()

		sys.exit(0)

	if out == None: out = re.sub('.csv', '.sql', file)

	if file.endswith('.csv') == False:
		print('Input file is not a CSV file.')
		sys.exit(1)

	if out.endswith('.sql') == False:
		print('Output file is not a SQL file.')
		sys.exit(1)

	head, tail = os.path.split(file)
	table = re.sub('.csv', '', tail)

	if separator == None: separator = ','
	if comments == None: comments = True

	fields = []
	rows = []
	with open(file, 'r') as csvfile:
		f = csv.reader(csvfile, delimiter=separator)
		headers = True
		for row in f:
			if headers:
				fields = separator.join(row).split(separator)
				headers = False
			else:
				rows.append(row)

		csvfile.close()

	dtable = 'DROP TABLE IF EXISTS `{0}`;'.format(table)
	ctable = 'CREATE TABLE IF NOT EXISTS `{0}` (\n'.format(table)
	insert = 'INSERT INTO `{0}` VALUES (\n'.format(table) 
	inserts = []
	x = 0
	for value in rows[0]:

		key = fields[x]

		fvalue = re.sub('\'|\"', '', value)
		tvalue = re.sub('\.', '', fvalue)

		if value.startswith('ObjectId('):
			ctable += '`{0}` VARCHAR(24),\n'.format(key)

		elif tvalue.isdigit() == False:
			pattern = re.compile('\d{4}\-\d{2}\-\d{2}')
			if pattern.match(value):
				ctable += '`{0}` TIMESTAMP,\n'.format(key)
			else:
				length = 50
				if key == 'description': length = 100
				ctable += '`{0}` VARCHAR({1}),\n'.format(key, length)

		else: ctable += '`{0}` NUMERIC(15, 2),\n'.format(key)

		x = x + 1

	x = 0
	for row in rows:

		ii = ''
		for value in rows[x]:

			fvalue = re.sub('ObjectId|\(|\)|\'|\"', '', value)
			tvalue = re.sub('\.', '', value)

			if tvalue.isdigit() == False:
				pattern = re.compile('\d{4}\-\d{2}\-\d{2}')
				if pattern.match(value):
					fvalue = re.sub('\T', ' ', fvalue)
					fvalue = re.sub('\.\d{3}Z', '', fvalue)
					fvalue = re.sub('\.\d{3}\+\d{4}', '', fvalue)

				ii += '\'{0}\',\n'.format(fvalue)

			else: ii += '{0},\n'.format(fvalue)

		ii = ii[:-2]
		inserts.append(insert + ii + ');\n\n')
		ii = ''
		x = x + 1

	ctable = ctable[:-2]
	ctable += ');'

	if verbose:
		print('\nGenerating SQL dump file: \'{0}\' from\nCSV file: \'{1}\'\n'
		.format(out, file))

	f = open(out, 'w')
	f.write('--!\n')
	if comments:
	    f.write('-- SQL table dump from CSV file: {0} ({1} -> {2})\n'
        .format(re.sub('.csv', '', file), file, out))
	    f.write('-- Generated by: {0}\n'.format(signature))
	    f.write('-- Generated at: {0}\n\n'.format(datetime.datetime.now()))
	if db != None: f.write('USE `{0}`;\n'.format(db))
	f.write('{0}\n'.format(dtable))
	f.write('{0}\n\n'.format(ctable))

	for insert in inserts:
		f.write(insert)

	f.close()


# Handle any command line arguments.
parser = argparse.ArgumentParser(description='Utility to convert a CSV file to a SQL dump.')
parser.add_argument('-f', '--file', action='store', dest='file', metavar="FILE")
parser.add_argument('-o', '--out', action='store', dest='out', metavar="OUT")
parser.add_argument('-s', '--separator', action='store', dest='separator', metavar="SEPARATOR")
parser.add_argument('-d', '--db', action='store', dest='db', metavar="DB")
parser.add_argument('-n', '--no-comments', action='store_false', dest='comments')
parser.add_argument('-l', '--verbose', action='store_true', dest='verbose')
parser.add_argument('-v', '--version', action='store_true', dest='version')
parser.add_argument('-i', '--info', action='store_true', dest='info')
argv = parser.parse_args()

ccsv2sql(argv.file, argv.out, argv.separator, argv.db, argv.comments, argv.verbose, argv.version, argv.info)
