import pandas as pd
import re
import tga_assessment_evaluation_tools as tga_utils

# script I used to build the large tables in evaluation chapter
# info on Teamscale is missing since it is closed-source

no_real_read_paths = {
    'JabRef': "../evaluation/JabRef/assessments/no_real_read_2022-10-28.json",
    'Ebean': "../evaluation/Ebean/assessments/report_no_real_read.json",
}

test_resources_regexes = {
    'JabRef': [re.compile("^src/test/resources/.+")],
    'Ebean': [re.compile(".*/test/resources/.+"), re.compile("ebean-test/testconfig/.+")],
}

no_real_read_frames = {}

for study_object in no_real_read_paths.keys():
    no_real_read_frames[study_object] = tga_utils.extend_frame_for_manual_exploration(pd.read_json(no_real_read_paths[study_object]), test_resources_regexes[study_object])

table_head = '''
\\begin{table}[]
\\begin{tabular}{@{}llllllll@{}}
\\toprule
\\multicolumn{1}{c}{\shortstack[l]{Study\\\\Object}} & \shortstack[l]{File\\\\Type} & \#Files& \% & \shortstack[l]{\#Test\\\\Resources} & \% & \shortstack[l]{\#Other\\\\Resources} & \% \\\\ \midrule\n
'''

table_end = '''
\end{tabular}
\end{table}
'''

def build_table(frame, study_object, top_n):
    file_type_distr = tga_utils.get_file_type_distribution(frame)

    sizes = file_type_distr.loc[:, 'absolute_file_numbers']
    sum_of_all = sizes.sum()
    n_largest = sizes.nlargest(n=top_n)
    test_resources = frame[frame['is_test_resource'] == True]

    total_sum_test_resources = len(test_resources)
    total_sum_not_test_resources = sum_of_all - total_sum_test_resources

    lines = '\\multirow{' + str(top_n) + '}{*}{' + study_object + "}"
    for file_type in n_largest.index:
        line = f' & *.{file_type} & {sizes[file_type]} & {(sizes[file_type]/sum_of_all)*100:.2f}\%'
        
        test_resources_of_type = test_resources[test_resources['file_ending'] == file_type]
        num_of_test_resources_of_type = len(test_resources_of_type)
        percent_test_resources_of_type = num_of_test_resources_of_type/total_sum_test_resources*100
        line += f' & {num_of_test_resources_of_type} & {percent_test_resources_of_type:.2f}\%'

        num_not_test_resources_of_type = sizes[file_type] - num_of_test_resources_of_type
        percent_not_test_resources_of_type = num_not_test_resources_of_type/total_sum_not_test_resources*100
        line += f' & {num_not_test_resources_of_type} & {percent_not_test_resources_of_type:.2f}\%'

        lines += line + '\\\\\n'

    return lines + '\\hline'

def build_tables(top_n=5):

    positives_table = table_head
    negatives_table = table_head


    for study_object in no_real_read_frames:
        nrrf = no_real_read_frames[study_object]

    
        positives = tga_utils.get_test_not_needed_files(nrrf)
        negatives = tga_utils.get_test_needed_files(nrrf)

        positives_table += build_table(positives, study_object, top_n)
        negatives_table += build_table(negatives, study_object, top_n)

    positives_table += table_end
    negatives_table += table_end

    print(positives_table)
    print(negatives_table)

    
if __name__ == '__main__':
    build_tables()