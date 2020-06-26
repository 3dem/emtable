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
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'delarosatrevin@gmail.com'
# *
# **************************************************************************

try:
    from StringIO import StringIO  # for Python 2
except ImportError:
    from io import StringIO  # for Python 3

import unittest
from metadata import Table


particles_3d_classify = """

data_Particles

loop_
_rlnEnabled #1
_rlnCoordinateX #2
_rlnCoordinateY #3
_rlnMicrographName #4
_rlnMicrographId #5
_rlnImageId #6
_rlnImageName #7
_rlnDefocusU #8
_rlnDefocusV #9
_rlnDefocusAngle #10
_rlnAmplitudeContrast #11
_rlnSphericalAberration #12
_rlnVoltage #13
_rlnGroupName #14
_rlnGroupNumber #15
_rlnAngleRot #16
_rlnAngleTilt #17
_rlnAnglePsi #18
_rlnOriginX #19
_rlnOriginY #20
_rlnClassNumber #21
_rlnNormCorrection #22
_rlnLogLikeliContribution #23
_rlnMaxValueProbDistribution #24
_rlnNrOfSignificantSamples #25
           1   307.000000   195.000000 14sep05c_00024sq_00003hl_00002es.frames.out.mrc            1            1 000001@Runs/000632_XmippProtExtractParticles/extra/14sep05c_00024sq_00003hl_00002es.frames_aligned_mic_DW.stk 12339.183594 12294.791992    99.198835     0.100000     2.700000   300.000000          1            1    68.622382    83.727084   -61.370416     1.791925     6.791925            4     0.663729 28037.624716     0.973726            7
           1   391.000000   184.000000 14sep05c_00024sq_00003hl_00002es.frames.out.mrc            1            2 000002@Runs/000632_XmippProtExtractParticles/extra/14sep05c_00024sq_00003hl_00002es.frames_aligned_mic_DW.stk 12339.183594 12294.791992    99.198835     0.100000     2.700000   300.000000          1            1    85.002533    90.029103   -61.560479     0.791925    -1.208075            4     0.684473 28120.382070     0.929493            4
           1   466.000000   193.000000 14sep05c_00024sq_00003hl_00002es.frames.out.mrc            1            3 000003@Runs/000632_XmippProtExtractParticles/extra/14sep05c_00024sq_00003hl_00002es.frames_aligned_mic_DW.stk 12339.183594 12294.791992    99.198835     0.100000     2.700000   300.000000          1            1    97.516821    30.331327   -36.788472    -1.208075    -3.208075            2     0.627209 28278.526381     0.857908           13
           1   531.000000   151.000000 14sep05c_00024sq_00003hl_00002es.frames.out.mrc            1            4 000004@Runs/000632_XmippProtExtractParticles/extra/14sep05c_00024sq_00003hl_00002es.frames_aligned_mic_DW.stk 12339.183594 12294.791992    99.198835     0.100000     2.700000   300.000000          1            1    94.360810    55.036777    57.300314     2.791925     3.791925            3     0.644296 28262.683878     0.947963            9
           1   509.000000    62.000000 14sep05c_00024sq_00003hl_00002es.frames.out.mrc            1            5 000005@Runs/000632_XmippProtExtractParticles/extra/14sep05c_00024sq_00003hl_00002es.frames_aligned_mic_DW.stk 12339.183594 12294.791992    99.198835     0.100000     2.700000   300.000000          1            1    96.205573    91.063145    73.546648     3.791925   -14.208075            4     0.666954 28189.046177     0.977995            2
           1   577.000000    66.000000 14sep05c_00024sq_00003hl_00002es.frames.out.mrc            1            6 000006@Runs/000632_XmippProtExtractParticles/extra/14sep05c_00024sq_00003hl_00002es.frames_aligned_mic_DW.stk 12339.183594 12294.791992    99.198835     0.100000     2.700000   300.000000          1            1    85.002533    90.029103   -84.060479     3.791925    -6.208075            4     0.635305 28170.108867     0.553587            4
           1   449.000000   260.000000 14sep05c_00024sq_00003hl_00002es.frames.out.mrc            1            7 000008@Runs/000632_XmippProtExtractParticles/extra/14sep05c_00024sq_00003hl_00002es.frames_aligned_mic_DW.stk 12339.183594 12294.791992    99.198835     0.100000     2.700000   300.000000          1            1   108.585187    37.526950    17.903647    -0.208075     0.791925            2     0.667233 28163.049866     0.911731            2
           1   352.000000   296.000000 14sep05c_00024sq_00003hl_00002es.frames.out.mrc            1            8 000009@Runs/000632_XmippProtExtractParticles/extra/14sep05c_00024sq_00003hl_00002es.frames_aligned_mic_DW.stk 12339.183594 12294.791992    99.198835     0.100000     2.700000   300.000000          1            1    91.961962    76.133892    58.309014     0.791925     0.791925            4     0.656658 28158.309552     1.000000            3
           1   341.000000   160.000000 14sep05c_00024sq_00003hl_00002es.frames.out.mrc            1            9 000010@Runs/000632_XmippProtExtractParticles/extra/14sep05c_00024sq_00003hl_00002es.frames_aligned_mic_DW.stk 12339.183594 12294.791992    99.198835     0.100000     2.700000   300.000000          1            1    79.795684    28.676110   -52.021531     0.791925    -3.208075            2     0.659256 28053.390888     0.927243           52
           1   246.000000   259.000000 14sep05c_00024sq_00003hl_00002es.frames.out.mrc            1           10 000011@Runs/000632_XmippProtExtractParticles/extra/14sep05c_00024sq_00003hl_00002es.frames_aligned_mic_DW.stk 12339.183594 12294.791992    99.198835     0.100000     2.700000   300.000000          1            1   102.232415    86.805935    21.169372     4.791925    -4.208075            4     0.687305 28158.010142     0.999999            3
           1   192.000000   233.000000 14sep05c_00024sq_00003hl_00002es.frames.out.mrc            1           11 000012@Runs/000632_XmippProtExtractParticles/extra/14sep05c_00024sq_00003hl_00002es.frames_aligned_mic_DW.stk 12339.183594 12294.791992    99.198835     0.100000     2.700000   300.000000          1            1    79.312466    34.817394   -57.844705    -4.208075     0.791925            2     0.686443 28106.037643     0.955989           11
           1   193.000000   188.000000 14sep05c_00024sq_00003hl_00002es.frames.out.mrc            1           12 000013@Runs/000632_XmippProtExtractParticles/extra/14sep05c_00024sq_00003hl_00002es.frames_aligned_mic_DW.stk 12339.183594 12294.791992    99.198835     0.100000     2.700000   300.000000          1            1    91.044325    85.788883     5.953691    -0.208075    -0.208075            4     0.699492 28022.518889     0.997447            6
           1   175.000000   110.000000 14sep05c_00024sq_00003hl_00002es.frames.out.mrc            1           13 000014@Runs/000632_XmippProtExtractParticles/extra/14sep05c_00024sq_00003hl_00002es.frames_aligned_mic_DW.stk 12339.183594 12294.791992    99.198835     0.100000     2.700000   300.000000          1            1    88.060352    60.170945    80.125610    -0.208075    20.791925            3     0.673482 28024.400421     0.562419            7
           1   620.000000   244.000000 14sep05c_00024sq_00003hl_00002es.frames.out.mrc            1           14 000015@Runs/000632_XmippProtExtractParticles/extra/14sep05c_00024sq_00003hl_00002es.frames_aligned_mic_DW.stk 12339.183594 12294.791992    99.198835     0.100000     2.700000   300.000000          1            1    79.795684    28.676110    22.978469     0.791925    -0.208075            2     0.670751 28268.575829     0.998270           23
           1   548.000000   316.000000 14sep05c_00024sq_00003hl_00002es.frames.out.mrc            1           15 000016@Runs/000632_XmippProtExtractParticles/extra/14sep05c_00024sq_00003hl_00002es.frames_aligned_mic_DW.stk 12339.183594 12294.791992    99.198835     0.100000     2.700000   300.000000          1            1    94.360810    55.036777  -122.699686    -0.208075    -0.208075            3     0.658460 28168.800559     0.976639           17
           1   600.000000   126.000000 14sep05c_00024sq_00003hl_00002es.frames.out.mrc            1           16 000017@Runs/000632_XmippProtExtractParticles/extra/14sep05c_00024sq_00003hl_00002es.frames_aligned_mic_DW.stk 12339.183594 12294.791992    99.198835     0.100000     2.700000   300.000000          1            1    94.179186    36.200886    54.740818    -0.208075    -3.208075            2     0.659461 28086.954253     0.915932            1

"""

optimiser_3d_classify = """
# RELION optimiser
# --gpu --pool 30 --angpix 2.62 --dont_combine_weights_via_disc --ref Runs/001015_ProtRelionClassify3D/tmp/model_00_01.00.mrc --scale --offset_range 5.0 --ini_high 60.0 --offset_step 2.0 --healpix_order 2 --tau2_fudge 4 --ctf --oversampling 1 --o Runs/001015_ProtRelionClassify3D/extra/relion --i Runs/001015_ProtRelionClassify3D/input_particles.star --iter 25 --zero_mask --norm --firstiter_cc --sym d7 --K 4 --flatten_solvent --particle_diameter 250 --j 2

data_optimiser_general

_rlnOutputRootName                                    Runs/001015_ProtRelionClassify3D/extra/relion
_rlnModelStarFile                                     Runs/001015_ProtRelionClassify3D/extra/relion_it024_model.star
_rlnExperimentalDataStarFile                          Runs/001015_ProtRelionClassify3D/extra/relion_it024_data.star
_rlnOrientSamplingStarFile                            Runs/001015_ProtRelionClassify3D/extra/relion_it024_sampling.star
_rlnCurrentIteration                                            24
_rlnNumberOfIterations                                          25
_rlnDoSplitRandomHalves                                          0
_rlnJoinHalvesUntilThisResolution                        -1.000000
_rlnAdaptiveOversampleOrder                                      1
_rlnAdaptiveOversampleFraction                            0.999000
_rlnRandomSeed                                          1534860268
_rlnParticleDiameter                                    250.000000
_rlnWidthMaskEdge                                                5
_rlnDoZeroMask                                                   1
_rlnDoSolventFlattening                                          1
_rlnSolventMaskName                                   None
_rlnSolventMask2Name                                  None
_rlnTauSpectrumName                                   None
_rlnCoarseImageSize                                             24
_rlnMaximumCoarseImageSize                                     120
_rlnHighresLimitExpectation                              -1.000000
_rlnIncrementImageSize                                          10
_rlnDoMapEstimation                                              1
_rlnDoStochasticGradientDescent                                  0
_rlnSgdMuFactor                                           0.000000
_rlnSgdSigma2FudgeInitial                                 8.000000
_rlnSgdSigma2FudgeHalflife                                      -1
_rlnSgdNextSubset                                                1
_rlnSgdSubsetSize                                               -1
_rlnSgdWriteEverySubset                                         -1
_rlnSgdMaxSubsets                                               -1
_rlnSgdStepsize                                           0.500000
_rlnHighresLimitSGD                                      20.000000
_rlnDoAutoRefine                                                 0
_rlnAutoLocalSearchesHealpixOrder                                4
_rlnNumberOfIterWithoutResolutionGain                            1
_rlnBestResolutionThusFar                                 0.117684
_rlnNumberOfIterWithoutChangingAssignments                       8
_rlnDoSkipAlign                                                  0
_rlnDoSkipRotate                                                 0
_rlnOverallAccuracyRotations                              2.097000
_rlnOverallAccuracyTranslations                           0.490000
_rlnChangesOptimalOrientations                            8.929285
_rlnChangesOptimalOffsets                                 0.690718
_rlnChangesOptimalClasses                                 0.029112
_rlnSmallestChangesOrientations                           7.252972
_rlnSmallestChangesOffsets                                0.653341
_rlnSmallestChangesClasses                                       0
_rlnLocalSymmetryFile                                 None
_rlnDoHelicalRefine                                              0
_rlnIgnoreHelicalSymmetry                                        0
_rlnHelicalTwistInitial                                   0.000000
_rlnHelicalRiseInitial                                    0.000000
_rlnHelicalCentralProportion                              0.300000
_rlnHelicalMaskTubeInnerDiameter                         -1.000000
_rlnHelicalMaskTubeOuterDiameter                         -1.000000
_rlnHelicalSymmetryLocalRefinement                               0
_rlnHelicalSigmaDistance                                 -1.000000
_rlnHelicalKeepTiltPriorFixed                                    0
_rlnHasConverged                                                 0
_rlnHasHighFscAtResolLimit                                       0
_rlnHasLargeSizeIncreaseIterationsAgo                            0
_rlnDoCorrectNorm                                                1
_rlnDoCorrectScale                                               1
_rlnDoCorrectCtf                                                 1
_rlnDoRealignMovies                                              0
_rlnDoIgnoreCtfUntilFirstPeak                                    0
_rlnCtfDataArePhaseFlipped                                       0
_rlnCtfDataAreCtfPremultiplied                                   0
_rlnDoOnlyFlipCtfPhases                                          0
_rlnRefsAreCtfCorrected                                          1
_rlnFixSigmaNoiseEstimates                                       0
_rlnFixSigmaOffsetEstimates                                      0
_rlnMaxNumberOfPooledParticles                                  60

"""

corrected_micrographs_mc = """
# RELION; version 3.0-beta-2

data_

loop_
_rlnMicrographNameNoDW #1
_rlnMicrographName #2
_rlnMicrographMetadata #3
_rlnAccumMotionTotal #4
_rlnAccumMotionEarly #5
_rlnAccumMotionLate #6
MotionCorr/job019/Movies/14sep05c_00024sq_00003hl_00002es_frames_out_noDW.mrc MotionCorr/job019/Movies/14sep05c_00024sq_00003hl_00002es_frames_out.mrc MotionCorr/job019/Movies/14sep05c_00024sq_00003hl_00002es_frames_out.star    22.132552     4.247538    17.885014
MotionCorr/job019/Movies/14sep05c_00024sq_00003hl_00005es_frames_out_noDW.mrc MotionCorr/job019/Movies/14sep05c_00024sq_00003hl_00005es_frames_out.mrc MotionCorr/job019/Movies/14sep05c_00024sq_00003hl_00005es_frames_out.star    13.562005     2.960148    10.601857
MotionCorr/job019/Movies/14sep05c_00024sq_00004hl_00002es_frames_out_noDW.mrc MotionCorr/job019/Movies/14sep05c_00024sq_00004hl_00002es_frames_out.mrc MotionCorr/job019/Movies/14sep05c_00024sq_00004hl_00002es_frames_out.star    18.007865     3.779594    14.228271
MotionCorr/job019/Movies/14sep05c_00024sq_00006hl_00003es_frames_out_noDW.mrc MotionCorr/job019/Movies/14sep05c_00024sq_00006hl_00003es_frames_out.mrc MotionCorr/job019/Movies/14sep05c_00024sq_00006hl_00003es_frames_out.star    20.770114     6.949991    13.820123


"""


one_micrograph_mc = """

data_general

_rlnImageSizeX                                     3710
_rlnImageSizeY                                     3838
_rlnImageSizeZ                                       19
_rlnMicrographMovieName                    Movies/14sep05c_00024sq_00003hl_00002es.frames.out.mrc
_rlnMicrographBinning                          1.000000
_rlnMicrographOriginalPixelSize                0.980000
_rlnMicrographDoseRate                         1.000000
_rlnMicrographPreExposure                      0.000000
_rlnVoltage                                  300.000000
_rlnMicrographStartFrame                              1
_rlnMotionModelVersion                                1


data_global_shift

loop_
_rlnMicrographFrameNumber #1
_rlnMicrographShiftX #2
_rlnMicrographShiftY #3
           1     0.000000     0.000000
           2     -0.92947     1.351926
           3     -1.25714     2.649279
           4     -1.48046     3.898302
           5     -1.57214     5.401121
           6     -1.57718     6.602875
           7     -1.53598     7.820991
           8     -1.51119     9.058397
           9     -1.33274    10.382935
          10     -1.19729    11.524827
          11     -1.02812    12.590772
          12     -0.77567    13.707154
          13     -0.47538    14.849956
          14     -0.38857    15.953708
          15     -0.28121    17.071532
          16     -0.12154    18.125245
          17     -0.13039    19.158861
          18     0.325042    20.420224
          19     0.456827    21.571432


data_local_motion_model

loop_
_rlnMotionModelCoeffsIdx #1
_rlnMotionModelCoeff #2
           0     -0.18486
           1     0.013904
           2 -2.92664e-04
           3     -1.70863
           4     0.153590
           5     -0.00463
           6     1.941052
           7     -0.15309
           8     0.003330
           9     0.393906
          10     -0.03863
          11     0.001171
          12     0.244742
          13     -0.00831
          14 -3.14734e-05
          15     -0.07827
          16     -0.04730
          17     0.001907
          18     -0.16209
          19     0.018464
          20 -5.33441e-04
          21     0.191800
          22     -0.02936
          23 9.360878e-04
          24     0.804904
          25     -0.11657
          26     0.004019
          27     -0.79924
          28     0.063983
          29     -0.00189
          30     0.716423
          31     -0.06156
          32 9.240634e-04
          33     0.404810
          34     -0.05272
          35     0.001659

"""