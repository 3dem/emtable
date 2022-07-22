=======
emtable
=======

Emtable is a STAR file parser originally developed to simplify and speed up metadata conversion between Scipion and Relion. It is available as a small self-contained Python module (https://pypi.org/project/emtable/) and can be used to manipulate STAR files independently from Scipion.

How to cite
-----------

Please cite the code repository DOI: `10.5281/zenodo.4303966 <https://zenodo.org/record/4303966>`_

Authors
-------

 * Jose Miguel de la Rosa-Trevín, Department of Biochemistry and Biophysics, Science for Life Laboratory, Stockholm University, Stockholm, Sweden
 * Grigory Sharov, MRC Laboratory of Molecular Biology, Cambridge Biomedical Campus, England
 
Testing
-------

``python3 -m unittest discover emtable/tests``

Examples
--------

To start using the package, simply do:

.. code-block:: python

    from emtable import Table

Each table in STAR file usually has a *data\_* prefix. You only need to specify the remaining table name:

``Table(fileName=modelStar, tableName='perframe_bfactors')``

Be aware that from Relion 3.1 particles table name has been changed from "data_Particles" to "data_particles".

Reading
#######

For example, we want to read the whole *rlnMovieFrameNumber* column from modelStar file, table *data_perframe_bfactors*.

The code below will return a list of column values from all rows:

.. code-block:: python

    table = Table(fileName=modelStar, tableName='perframe_bfactors')
    frame = table.getColumnValues('rlnMovieFrameNumber')

We can also iterate over rows from "data_particles" Table:

.. code-block:: python

    table = Table(fileName=dataStar, tableName='particles')
        for row in table:
            print(row.rlnRandomSubset, row.rlnClassNumber)

Alternatively, you can use **iterRows** method which also supports sorting by a column:

.. code-block:: python

    mdIter = Table.iterRows('particles@' + fnStar, key='rlnImageId')

If for some reason you need to clear all rows and keep just the Table structure, use **clearRows()** method on any table.

There is a special case when a column field contains several items and it is delimited by quotes:

.. code-block::

    # XMIPP_STAR_1 *
    #
    data_noname
    loop_
     _anglePsi
     _angleRot
     _angleTilt
     _cost
     _enabled
     _image
     _itemId
     _nmaDisplacements
     _shiftX
     _shiftY
     -180.009437   -96.153255   243.098777 8.055914e-04                    1 000021@Runs/000088_ProtImportParticles/extra/img.stk                   21 '    -2.733360    -2.468260    -0.090721 '    -4.306965    -0.040850
        0.225648   206.555090     9.899219 7.811945e-04                    1 000002@Runs/000088_ProtImportParticles/extra/img.stk                    2 '   -41.891100   -41.568300     0.332499 '    -4.426523    -1.497812

For such cases, you need to pass **shlex=True** to the Table, so that each string of columns is splited using shlex library. However, this requires emtable v0.0.14+

Writing
#######

If we want to create a new table with 3 pre-defined columns, add rows to it and save as a new file:

.. code-block:: python

    tableShifts = Table(columns=['rlnCoordinateX',
                                 'rlnCoordinateY',
                                 'rlnAutopickFigureOfMerit',
                                 'rlnClassNumber'])
    tableShifts.addRow(1024.54, 2944.54, 0.234, 3)
    tableShifts.addRow(445.45, 2345.54, 0.266, 3)

    tableShifts.write(f, tableName="test", singleRow=False)

*singleRow* is **False** by default. If *singleRow* is **True**, we don't write a *loop_*, just label-value pairs. This is used for "one-column" tables, such as below:


.. code-block:: bash

    data_general

    _rlnImageSizeX                                     3710
    _rlnImageSizeY                                     3838
    _rlnImageSizeZ                                       24
    _rlnMicrographMovieName                    Movies/20170629_00026_frameImage.tiff
    _rlnMicrographGainName                     Movies/gain.mrc
    _rlnMicrographBinning                          1.000000
    _rlnMicrographOriginalPixelSize                0.885000
    _rlnMicrographDoseRate                         1.277000
    _rlnMicrographPreExposure                      0.000000
    _rlnVoltage                                  200.000000
    _rlnMicrographStartFrame                              1
    _rlnMotionModelVersion                                1
