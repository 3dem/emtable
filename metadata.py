# **************************************************************************
# *
# * Authors:  J. M. de la Rosa Trevin (delarosatrevin@gmail.com)
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 3 of the License, or
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

__version__ = '0.0.6'
__author__ = 'Jose Miguel de la Rosa Trevin'


import os
import sys
import argparse
from io import open
from collections import OrderedDict, namedtuple


class Column:
    def __init__(self, name, type=None):
        self._name = name
        # Get the type from the LABELS dict, assume str by default
        self._type = type or str

    def __str__(self):
        return 'Column: %s (type: %s)' % (self._name, self._type)

    def __cmp__(self, other):
        return (self.getName() == other.getName()
                and self.getType() == other.getType())

    def __eq__(self, other):
            return self.__cmp__(other)

    def getName(self):
        return self._name

    def getType(self):
        return self._type

    def setType(self, colType):
        self._type = colType


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
            self._createColumns(kwargs['columns'])

    def clear(self):
        self.Row = None
        self._columns = OrderedDict()
        self._rows = []
        self._inputFile = None
        self._inputLine = None

    def clearRows(self):
        """ Remove all the rows from the table, but keep its columns. """
        self._rows = []

    def addRow(self, *args, **kwargs):
        self._rows.append(self.Row(*args, **kwargs))

    def readStar(self, inputFile, tableName=None,
                 headerOnly=False,
                 guessType=True):
        """
        :param inputFile: Provide the input file from where to read the data.
            The file pointer will be moved until the last data line of the
            requested table.
        :param tableName: star table name
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

        self._createColumns(colNames, line, guessType)

        if not foundLoop:
            self.addRow(*values)
        else:
            if headerOnly:
                self._rows = None  # Mark as an iterator
                self._inputLine = line
                self._inputFile = inputFile
            else:
                for row in self.__iterRows(line, inputFile):
                    self._rows.append(row)

    def read(self, fileName, tableName=None):
        with open(fileName) as f:
            self.readStar(f, tableName)

    def _formatValue(self, v):
        return '%0.6f' % v if isinstance(v, float) else str(v)

    def _getFormatStr(self, v):
        return '.6f' if isinstance(v, float) else ''

    def writeStarLine(self, outputFile, values):
        """ Function to write a single row into the star file.
        The function writeStar should have been called first with
        writeRows=False.
        """
        outputFile.write(self.__lineFormat.format(*values))
        outputFile.write('\n')

    def writeStar(self, outputFile, tableName=None,
                  singleRow=False, writeRows=True):
        """
        Write a Table in Star format to the given file.
        :param outputFile: File handler that should be already opened and
            in the position to write.
        :param tableName: The name of the table to write.
        :param singleRow: If True, don't write loop_, just label - value pairs.
        :param writeRows: write data rows
        """
        outputFile.write("\ndata_%s\n\n" % (tableName or ''))

        if self.size() == 0:
            return

        if singleRow:
            m = max([len(c) for c in self._columns.keys()]) + 5
            lineFormat = "_{:<%d} {:>10}\n" % m
            row = self._rows[0]
            for col, value in row._asdict().items():
                outputFile.write(lineFormat.format(col, value))
            outputFile.write('\n\n')
            return

        outputFile.write("loop_\n")

        # Write column names
        for col in self._columns.values():
            outputFile.write("_%s \n" % col.getName())

        # Take a hint for the columns width from the first row
        widths = [len(self._formatValue(v)) for v in self._rows[0]]
        formats = [self._getFormatStr(v) for v in self._rows[0]]

        n = len(self)
        if n > 1:
            # Check middle and last row, just in case ;)
            for index in [n//2, -1]:
                for i, v in enumerate(self._rows[index]):
                    w = len(self._formatValue(v))
                    if w > widths[i]:
                        widths[i] = w

        self.__lineFormat = " ".join("{:>%d%s} " % (w+1, f) for w, f in zip(widths, formats))

        if writeRows:
            # Write data rows
            for row in self._rows:
                self.writeStarLine(outputFile, row)

            outputFile.write('\n')

    def write(self, output_star, tableName=None):
        with open(output_star, 'w') as output_file:
            self.writeStar(output_file, tableName)

    def printColumns(self):
        print("Columns: ")
        for c in self.getColumns():
            print("   %s" % str(c))

    def printStar(self, tableName=None):
        self.writeStar(sys.stdout, tableName)

    def isIter(self):
        """ Return True if this Table is acting as an Iterator.
        This is the case when only the header is read and then row
        will be parsed while iterating, without loading the whole Table
        in memory.
        """
        return self._rows is None

    def size(self):
        return 0 if self.isIter() else len(self._rows)

    def hasColumn(self, colName):
        """ Return True if a given column exists. """
        return colName in self._columns

    def getColumn(self, colName):
        """ Return the column with that name or
        None if the column does not exist.
        """
        return self._columns.get(colName, None)

    def getColumns(self):
        return self._columns.values()

    def getColumnNames(self):
        return [c.getName() for c in self.getColumns()]

    def addColumns(self, *args):
        """ Add one or many columns.

        Each argument should be in the form:
            columnName=value
        where value can be a constant or another column.

        Examples:
            table.addColumns('rlnDefocusU=rlnDefocusV', 'rlnDefocusAngle=0.0')
        """
        #TODO:
        # Maybe implement more complex value expression,
        # e.g some basic arithmetic operations or functions

        map = {k: k for k in self.getColumnNames()}
        constSet = set()
        newCols = OrderedDict()

        for a in args:
            colName, right = a.split('=')
            if self.hasColumn(right):
                colType = self.getColumn(right).getType()
                map[colName] = right
            elif right in newCols:
                colType = newCols[right].getType()
                map[colName] = map[right]
            else:
                colType = self._guessType(right)
                value = colType(right)
                map[colName] = value
                constSet.add(value)

            newCols[colName] = Column(colName, colType)

        # Update columns and create new Row class
        self._columns.update(newCols)
        self._createRowClass()

        # Update rows with new column values
        oldRows = self._rows
        self.clearRows()

        def _get(row, colName):
            # Constants are passed as tuple
            mapped = map[colName]
            return mapped if mapped in constSet else getattr(row, mapped)

        colNames = self.getColumnNames()
        for row in oldRows:
            self._rows.append(self.Row(**{k: _get(row, k) for k in colNames}))

    def removeColumns(self, *args):
        """ Remove columns with these names. """
        # Check if any argument is a list and flatten into a single one
        rmCols = []
        for a in args:
            if isinstance(a, list):
                rmCols.extend(a)
            else:
                rmCols.append(a)

        oldColumns = self._columns
        oldRows = self._rows

        # Remove non desired columns and create again the Row class
        self._columns = {k: v for k, v in oldColumns.items() if k not in rmCols}
        self._createRowClass()

        # Recreate rows without these column values
        cols = self.getColumnNames()
        self.clearRows()

        for row in oldRows:
            self._rows.append(self.Row(**{k: getattr(row, k) for k in cols}))


    def getColumnValues(self, colName):
        """
        Return the values of a given column
        :param colName: The name of an existing column to retrieve values.
        :return: A list with all values of that column.
        """
        if colName not in self._columns:
            raise Exception("Not existing column: %s" % colName)
        return [getattr(row, colName) for row in self._rows]


    def sort(self, key, reverse=False):
        """ Sort the table in place using the provided key.
        If key is a string, it should be the name of one column. """
        keyFunc = lambda r: getattr(r, key) if isinstance(key, str) else key
        self._rows.sort(key=keyFunc, reverse=reverse)

    @staticmethod
    def iterRows(fileName, key=None, reverse=False, **kwargs):
        """
        Convenience method to iterate over the rows of a given table.

        Args:
            fileName: the input star filename, it migth contain the '@'
                to specify the tableName
            key: key function to sort elements, it can also be an string that
                will be used to retrieve the value of the column with that name.
            reverse: If true reverse the sort order.
        """
        if '@' in fileName:
            tableName, fileName = fileName.split('@')
        else:
            tableName = kwargs.get('tableName', None)

        # Create a table iterator
        tableIter = Table()
        with open(fileName) as f:
            tableIter.readStar(f, tableName, headerOnly=True)
            if key is None:
                for row in tableIter:
                    yield row
            else:
                if isinstance(key, str):
                    keyFunc = lambda r: getattr(r, key)
                else:
                    keyFunc = key
                for row in sorted(tableIter, key=keyFunc, reverse=reverse):
                    yield row

    def __len__(self):
        return self.size()

    def __iterRows(self, line, inputFile):
        """ Internal method to iter through rows. """
        typeList = [c.getType() for c in self.getColumns()]
        while line:
            yield self.Row(*[t(v) for t, v in zip(typeList, line.split())])
            line = inputFile.readline().strip()

    def __iter__(self):
        if self.isIter():
            source = self.__iterRows(self._inputLine, self._inputFile)
        else:
            source = self._rows

        for row in source:
            yield row

    def __getitem__(self, item):
        return self._rows[item]

    def __setitem__(self, key, value):
        self._rows[key] = value

    # --------- Internal implementation methods ------------------------

    def _addColumn(self, nameOrTuple, colType):
        """
        :param nameOrTuple: This parameter should be either a string or
            a tuple (string, type).
        """
        if isinstance(nameOrTuple, str):
            col = Column(nameOrTuple)
        elif isinstance(nameOrTuple, tuple):
            col = Column(nameOrTuple[0], nameOrTuple[1])
        elif isinstance(nameOrTuple, Column):
            col = nameOrTuple
        else:
            raise Exception("Invalid input as column, "
                            "should be either string or tuple.")
        col.setType(colType)
        self._columns[col.getName()] = col

    def _guessType(self, strValue):
        try:
            int(strValue)
            return int
        except ValueError:
            try:
                float(strValue)
                return float
            except ValueError:
                return str

    def _guessTypesFromLine(self, line):
        return [self._guessType(v) for v in line.split()]

    def _createColumns(self, columnList, line=None, guessType=False):
        """ Create the columns, optionally, a data line can be passed
        to infer the Column type.
        """
        self.clear()
        if line and guessType:
            typeList = self._guessTypesFromLine(line)
        else:
            typeList = [str] * len(columnList)

        for col, colType in zip(columnList, typeList):
            self._addColumn(col, colType)
        self._createRowClass()

    def _createRowClass(self):
        self.Row = namedtuple('Row', [c for c in self._columns.keys()])

    def _findDataLine(self, inputFile, dataStr):
        """ Raise an exception if the desired data string is not found.
        Move the line pointer after the desired line if found.
        """
        line = inputFile.readline()
        while line:
            if line.startswith(dataStr):
                return line
            line = inputFile.readline()

        raise Exception("'%s' block was not found" % dataStr)

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

    # add("-v", "--verbosity", action="count", default=0)

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
        if 0 < limit == i:
            break

        tableOut.addRow(*row)

    if args.output:
        tableOut.write(args.output, tableName)
    else:
        tableOut.printStar(tableName)
