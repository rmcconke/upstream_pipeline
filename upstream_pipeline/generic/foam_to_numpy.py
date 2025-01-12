from dataFoam.utilities.MLDatasetFromFoamCase import MLDatasetFromFoamCase
import argparse
 
parser = argparse.ArgumentParser()
parser.add_argument("-case", "--case",  help="case")
parser.add_argument("-foam_parent_dir", "--foam_parent_dir",  help="case")
parser.add_argument("-data_save_dir", "--data_save_dir",  help="case")
parser.add_argument("-case_type", "--case_type", help="case type, e.g. komega, komegasst, LES")
parser.add_argument("-write_fields_application", "--write_fields_application", help="foam application called when writing fields, e.g. writeFields_RANS")
parser.add_argument("-no_overwrite", "--no_overwrite", action='store_false', help="skip overwriting currently written fields (e.g., just read)")
parser.add_argument("-dataset_prefix", "--dataset_prefix", help="prefix for numpy binaries")

args = parser.parse_args()

print(f'No overwrite:{args.no_overwrite}')

RANSCase = MLDatasetFromFoamCase(data_save_path = args.data_save_dir,
                                    foam_parent_dir = args.foam_parent_dir,
                                    case_name =  args.case,
                                    case_type = args.case_type,
                                    write_fields_application = args.write_fields_application,
                                    write_fields_flag = args.no_overwrite
                                    ) 
RANSCase.writeFields()
RANSCase.saveDataset(f'{args.dataset_prefix}_{args.case}')
