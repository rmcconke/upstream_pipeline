from dataFoam.preprocessing.map_coarse_fine import interpolate_fields_fine_coarse_DUCT
import argparse
 
parser = argparse.ArgumentParser(description='map_coarse_fine wrapper')
parser.add_argument("-case", "--case",  help="case")
parser.add_argument("-field", "--field",  help="field")
parser.add_argument("-coarse_field_dir", "--coarse_field_dir",  help="field")
parser.add_argument("-fine_field_dir", "--fine_field_dir",  help="field")
parser.add_argument("-output_dir", "--output_dir",  help="field")

args = parser.parse_args()

interpolate_fields_fine_coarse_DUCT(args.fine_field_dir,
                           args.coarse_field_dir,
                           args.output_dir,
                           'DNS_squareDuct_Re_'+args.case,
                           'komegasst_squareDuctAve_Re_'+args.case, 
                           'DNS_squareDuctAve_Re_'+args.case,
                            [args.field],
                           'linear'
                            )

