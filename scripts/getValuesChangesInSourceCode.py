import pandas as pd

# script I used to get the "MODIFICATIONS" and "ADDITIONS" in the source code of the study objects
# info on teamscale is missing since it is closed-source

report_paths = {
    'JabRef': '../evaluation/JabRef/resource_tga_report_only_java_source_code.json',
    'Ebean': '../evaluation/Ebean/resource_tga_report_only_java_source_files.json',
}

report_frames = {}

def print_values_for_one_study_object(study_object: str):
    print(f"Values for {study_object}:")
    frame = report_frames[study_object]
    total_num = len(frame)
    print(f"Total num source-code-files: {total_num}")
    modifications = frame[frame['assessment'].str.contains('MODIFICATION')]
    num_mods = len(modifications)
    num_adds = total_num - num_mods
    print(f"Num of modifications: {num_mods} ({num_mods/total_num*100.0:.2f}\%)")
    print(f"num of additions (not modified): {num_adds} ({num_adds/total_num*100.0:.2f}\%)")
    print('')

for study_object in report_paths.keys():
    report_frames[study_object] = pd.read_json(report_paths[study_object])
    print_values_for_one_study_object(study_object)

