from dataFoam.preprocessing.assemble_dataframe import assemble_dataframe
import os

cases=['fp_1000', 'fp_1410', 'fp_2000', 'fp_2540', 'fp_3030', 'fp_3270', 'fp_3630', 'fp_3970', 'fp_4060',
       'case_0p5','case_0p8','case_1p0','case_1p2','case_1p5','h20','h26','h31','h38','h42','convdiv12600','convdiv20580','cbfs13700',
       'squareDuctAve_Re_1100',
       'squareDuctAve_Re_1150',
       'squareDuctAve_Re_1250',
       'squareDuctAve_Re_1300',
       'squareDuctAve_Re_1350',
       'squareDuctAve_Re_1400',
       'squareDuctAve_Re_1500',
       'squareDuctAve_Re_1600',
       'squareDuctAve_Re_1800',
       'squareDuctAve_Re_2000',
       'squareDuctAve_Re_2205',
       'squareDuctAve_Re_2400',
       'squareDuctAve_Re_2600',
       'squareDuctAve_Re_2900',
       'squareDuctAve_Re_3200',
       'squareDuctAve_Re_3500']


field_dict = {
              'kepsilonphitf': ['U',
                                'k',
                                'epsilon',
                                'phit',
                                'f',
                                'nut',
                                'p',

                                'gradU',
                                'gradk',
                                'gradepsilon',
                                'gradphit',
                                'gradf',
                                'gradnut',
                                'gradp',

                                'v2',
                                'gradv2',

                                'turbR',
                                'divturbR',

                                'DUDt',
                                'wallDistance',
                                'S',
                                'R',
                                'skewness',
                                'C',
                                'Uplus',
                                'kplus',
                                'yplus'
                                ],
              }

assemble_dataframe(os.getenv('ML_NUMPY_DATASET'),
                field_dict,
                   cases,
                   os.path.join(os.getenv('ML_DATAFRAME_OUTPUT'),'kepsilonphitf.csv'))

field_dict = {'REF':['U',
                            'tau',
                            'k',
                            'a',
                            'b',
                                          
                            'gradU',
                            'divtau',
                            
                            'tauplus',
                            'Uplus',
                            'yplus'
                            ]
              }
    
assemble_dataframe(os.getenv('ML_NUMPY_DATASET'),
                field_dict,
                   cases,
                   os.path.join(os.getenv('ML_DATAFRAME_OUTPUT'),'REF.csv'))


field_dict = {
              'komegasst': ['U',
                                'k',
                                'epsilon',
                                'omega',
                                'nut',
                                'p',

                                'gradU',
                                'gradk',
                                'gradepsilon',
                                'gradomega',
                                'gradnut',
                                'gradp',

                                'turbR',
                                'divturbR',
                                'DUDt',
                                'wallDistance',
                                'S',
                                'R',
                                'skewness',
                                'C',
                                'Uplus',
                                'kplus',
                                'yplus'
                                ],
              }

assemble_dataframe(os.getenv('ML_NUMPY_DATASET'),
                field_dict,
                   cases,
                   os.path.join(os.getenv('ML_DATAFRAME_OUTPUT'),'komegasst.csv'))

field_dict = {
              'komega': ['U',
                                'k',
                                'epsilon',
                                'omega',
                                'nut',
                                'p',

                                'gradU',
                                'gradk',
                                'gradepsilon',
                                'gradomega',
                                'gradnut',
                                'gradp',

                                'turbR',
                                'divturbR',
                                'DUDt',
                                'wallDistance',
                                'S',
                                'R',
                                'skewness',
                                'C',
                                'Uplus',
                                'kplus',
                                'yplus'
                                ],
              }

assemble_dataframe(os.getenv('ML_NUMPY_DATASET'),
                field_dict,
                   cases,
                   os.path.join(os.getenv('ML_DATAFRAME_OUTPUT'),'komega.csv'))


