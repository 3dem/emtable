# **************************************************************************
# *
# * Authors:  J. M. de la Rosa Trevin (delarosatrevin@gmail.com)
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 2 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# **************************************************************************

__version__ = '0.0.3'
__author__ = 'Jose Miguel de la Rosa Trevin'


import os
import sys
import argparse
from collections import OrderedDict, namedtuple


class Column:
    def __init__(self, name, type=None):
        self._name = name
        # Get the type from the LABELS dict, assume str by default
        self._type = type

    def __str__(self):
        return self._name

    def __cmp__(self, other):
        return self._name == str(other)


class Table:
    """
    Class to hold and manipulate tabular data for EM processing programs.
    """
    def __init__(self, **kwargs):
        self.clear()

        if 'fileName' in kwargs:
            if 'columns' in kwargs:
                raise Exception("Please provide either 'columns' or 'fileName',"
                                " but not both.")
            fileName = kwargs.get('fileName')
            tableName = kwargs.get('tableName', None)
            self.read(fileName, tableName)
        elif 'columns' in kwargs:
            self._createColums(kwargs['columns'])

    def clear(self):
        self.Row = None
        self._columns = OrderedDict()
        self._rows = []

    def clearRows(self):
        """ Remove all the rows from the table, but keep its columns. """
        self._rows = []

    def addRow(self, *args, **kwargs):
        self._rows.append(self.Row(*args, **kwargs))

    def readStar(self, inputFile, tableName=None):
        """
        :param inputFile: Provide the input file from where to read the data.
            The file pointer will be moved until the last data line of the
            requested table.
        :return:
        """
        self.clear()
        dataStr = 'data_%s' % (tableName or '')

        self._findDataLine(inputFile, dataStr)

        # Find first column line and parse all columns
        line, foundLoop = self._findLabelLine(inputFile)
        colNames = []
        values = []

        while line.startswith('_'):
            parts = line.split()
            colNames.append(parts[0][1:])
            if not foundLoop:
                values.append(parts[1])
            line = inputFile.readline().strip()

        self._createColums(colNames)

        if not foundLoop:
            self.addRow(*values)
        else:
            # Parse all data lines
            while line:
                self.addRow(*line.split())
                line = inputFile.readline().strip()

    def read(self, fileName, tableName=None):
        with open(fileName) as f:
            self.readStar(f, tableName)

    def writeStar(self, outputFile, tableName=None, singleRow=False):
        """
        Write a Table in Star format to the given file.
        :param outputFile: File handler that should be already opened and
            in the position to write.
        :param tableName: The name of the table to write.
        :param singleRow: If True, don't write loop_, just label - value pairs.
        """
        outputFile.write("\ndata_%s\n\n" % (tableName or ''))

        if self.size() == 0:
            return

        if singleRow:
            m = max([len(c) for c in self._columns.keys()]) + 5
            lineFormat = "_{:<%d} {:>10}\n" % m
            row = self._rows[0]
            for col, value in row._asdict().iteritems():
                outputFile.write(lineFormat.format(col, value))
            outputFile.write('\n\n')
            return

        outputFile.write("loop_\n")

        # Write column names
        for col in self._columns.values():
            outputFile.write("_%s \n" % col)

        # Take a hint for the columns width from the first row

        widths = [len(str(v)) for v in self._rows[0]]
        # Check middle and last row, just in case ;)
        for index in [len(self)/2, -1]:
            for i, v in enumerate(self._rows[index]):
                w = len(str(v))
                if w > widths[i]:
                    widths[i] = w

        lineFormat = " ".join("{:>%d} " % (w + 1) for w in widths)

        # Write data rows
        for row in self._rows:
            outputFile.write(lineFormat.format(*row))
            outputFile.write('\n')

        outputFile.write('\n')

    def write(self, output_star, tableName=None):
        with open(output_star, 'w') as output_file:
            self.writeStar(output_file, tableName)

    def printStar(self, tableName=None):
        self.writeStar(sys.stdout, tableName)

    def size(self):
        return len(self._rows)

    def getColumns(self):
        return self._columns.values()

    def getColumnValues(self, colName):
        """
        Return the values of a given column
        :param colName: The name of an existing column to retrieve values.
        :return: A list with all values of that column.
        """
        if colName not in self._columns:
            raise Exception("Not existing column: %s" % colName)
        return [getattr(row, colName) for row in self._rows]

    def __len__(self):
        return self.size()

    def __iter__(self):
        for item in self._rows:
            yield item

    def __getitem__(self, item):
        return self._rows[item]

    def __setitem__(self, key, value):
        self._rows[key] = value

    # --------- Internal implementation methods ------------------------

    def _addColumn(self, nameOrTuple):
        """
        :param nameOrTuple: This parameter should be either a string or
            a tuple (string, type).
        """
        if isinstance(nameOrTuple, str):
            col = Column(nameOrTuple)
        elif isinstance(nameOrTuple, tuple):
            col = Column(nameOrTuple[0], nameOrTuple[1])
        else:
            raise Exception("Invalid input as column, "
                            "should be either string or tuple.")
        self._columns[str(col)] = col

    def _createColums(self, columnList):
        self.clear()
        for col in columnList:
            self._addColumn(col)
        self._createRowClass()

    def _createRowClass(self):
        self.Row = namedtuple('Row', [str(c) for c in self._columns])

    def _findDataLine(self, inputFile, dataStr):
        """ Raise an exception if the desired data string is not found.
        Move the line pointer after the desired line if found.
        """
        line = inputFile.readline()
        while line:
            if line.startswith(dataStr):
                return line
            line = inputFile.readline()

        raise Exception("%s block was not found")

    def _findLabelLine(self, inputFile):
        line = ''
        foundLoop = False

        l = inputFile.readline()
        while l:
            if l.startswith('_'):
                line = l
                break
            elif l.startswith('loop_'):
                foundLoop = True
            l = inputFile.readline()

        return line.strip(), foundLoop


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Script to manipulate metadata files.")

    add = parser.add_argument  # shortcut
    add("input", help="Input metadata filename. ", nargs='?', default="")
    add("output",
        help="Output metadata filename, if no provided, print to stdout. ",
        nargs='?', default="")

    add("-l", "--limit", type=int, default=0,
        help="Limit the number of rows processed, useful for testing. ")

    #add("-v", "--verbosity", action="count", default=0)

    args = parser.parse_args()

    if '@' in args.input:
        tableName, fileName = args.input.split('@')
    else:
        tableName, fileName = None, args.input

    if not os.path.exists(fileName):
        raise Exception("Input file '%s' does not exists. " % fileName)

    tableIn = Table(fileName=fileName, tableName=tableName)

    # Create another table with same columns
    tableOut = Table(columns=[str(c) for c in tableIn.getColumns()])

    limit = args.limit

    for i, row in enumerate(tableIn):
        if limit > 0 and i == limit:
            break

        tableOut.addRow(*row)

    if args.output:
        tableOut.write(args.output, tableName)
    else:
        tableOut.printStar(tableName)