from calendar import c
from gc import unfreeze
from hashlib import new
from random import uniform
from turtle import color
from typing import List
import pandas as pd
import argparse
import matplotlib.pyplot as plt
import numpy as np
import re

tum_colors = {
'TUMBlue': '#0065BD',
'TUMSecondaryBlue': '#005293',
'TUMSecondaryBlue2': '#003359',
'TUMBlack': '#000000',
'TUMWhite': '#FFFFFF',
'TUMDarkGray': '#333333',
'TUMGray': '#808080',
'TUMLightGray': '#CCCCC6',
'TUMAccentGray': '#DAD7CB',
'TUMAccentOrange': '#E37222',
'TUMAccentGreen': '#A2AD00',
'TUMAccentLightBlue': '#98C6EA',
'TUMAccentBlue': '#64A0C8',
}

def get_tum_colors(size=6) -> List[str]:
    if size > 6: size = 6
    return [tum_colors[key] for key in ['TUMBlue', 'TUMAccentOrange', 'TUMAccentGreen', 'TUMAccentBlue', 'TUMGray', 'TUMLightGray'][:size]]

class Arg_Options:

    assessment_file_path: str = None

    test_resource_pattern: str = None
    test_resource_directories: List[str] = []

    def __init__(self, assessment_file_path: str, test_resource_pattern: str = None, test_resource_dirs: List[str]=[]):
        self.assessment_file_path = assessment_file_path
        self.test_resource_directories = test_resource_dirs
        self.test_resource_pattern = test_resource_pattern

assessment_states = ['ADDITION_TESTED_AFTER_LAST_CHANGE',

	'ADDITION_EXECUTED_BEFORE_LAST_CHANGE',

	'ADDITION_NEVER_EXECUTED',

	'MODIFICATION_TESTED_AFTER_LAST_CHANGE',

	'MODIFICATION_EXECUTED_BEFORE_LAST_CHANGE',

	'MODIFICATION_NEVER_EXECUTED',

	'UNCHANGED_EXECUTED',

	'UNCHANGED_NOT_EXECUTED']

def get_file_added() -> List[str]:
    return [assessment_states[i] for i in range(3)]

def get_file_modified() -> List[str]:
    return [assessment_states[i] for i in range(3, 6)]

def get_file_added_or_modified() -> List[str]:
    return get_file_added().extend(get_file_modified())

def get_test_not_needed_assessment_states() -> List[str]:
    return [assessment_states[i] for i in [0, 3, 6]]


def get_test_needed_assessment_states() -> List[str]:
    return [assessment_states[i] for i in [1, 2, 4, 5]]

def get_executed_assessment_states() -> List[str]:
    return [assessment_states[i] for i in [0, 1, 3, 4, 6]]

def get_not_those_states(states: List[str]) -> List[str]:
    return [assessment_state for assessment_state in assessment_states if assessment_state not in states]


def parse_args() -> Arg_Options:
    parser = argparse.ArgumentParser(description='Different tools for the evaluation of a tga assessment solely for non-code-artifacts')
    parser.add_argument('assessment_file_path', type=str, help='The path to the json file to analyse')
    parser.add_argument('--test_resource_directories', '-tr_dirs', nargs='+', default=[], help='Directories containing test resources or files')

    args  = parser.parse_args()

    return Arg_Options(args.assessment_file_path, test_resource_dirs=args.test_resource_directories)


def get_file_type_distribution(assessment: pd.DataFrame) -> pd.DataFrame:
    value_counts = (assessment.loc[:, 'uniformPath']
    .map(lambda uniform_path: (splits:=uniform_path.split('/'))[len(splits)-1])
    .map(lambda filename: (splits:=filename.split('.'))[len(splits)-1])).value_counts()

    distribution_dataframe = value_counts.to_frame()
    distribution_dataframe.columns = ['absolute_file_numbers']
    sum_of_file_types = value_counts.sum()

    distribution_dataframe['relative_file_numbers'] = distribution_dataframe['absolute_file_numbers']/sum_of_file_types

    return distribution_dataframe

def expand_dataframe_with_file_types(assessment: pd.DataFrame) -> pd.DataFrame:
    assessment['file_ending'] = assessment.apply(lambda row: row['uniformPath'].split('/')[-1].split('.')[-1], axis=1)
    return assessment

def expand_dataframe_with_test_resource(frame: pd.DataFrame, test_resource_dirs: List[re.Pattern]) -> pd.DataFrame:
    frame['is_test_resource'] = frame.apply(lambda row: any([re.search(regex, row['uniformPath']) for regex in test_resource_dirs]), axis=1)
    return frame

def get_distribution_weight_for_file_ending(file_ending: str, distribution_dataframe: pd.DataFrame) -> int:
    return distribution_dataframe.loc[file_ending]['relative_file_numbers']

def draw_samples(assessment: pd.DataFrame, number_of_samples: int) -> pd.DataFrame:
    copy_to_work_with = assessment.copy()
    expand_dataframe_with_file_types(copy_to_work_with)
    distribution_dataframe = get_file_type_distribution(copy_to_work_with)

    sum_of_samples = 0

    new_frame = pd.DataFrame([], columns=copy_to_work_with.columns)

    for file_ending, row in distribution_dataframe.iterrows():
        weight = row['relative_file_numbers']
        n = round(number_of_samples*weight)
        sum_of_samples += n
        #print(f'Number of samples for file_ending"{file_ending}": {n} - percentage {weight*100}%')
        new_frame = pd.concat([new_frame, copy_to_work_with.loc[copy_to_work_with['file_ending'] == file_ending].sample(n)], axis=0)

    #print(f'Final sum of samples: {sum_of_samples}')
    return new_frame


def get_test_not_needed_files(assessment: pd.DataFrame) -> pd.DataFrame:
    return assessment[assessment['assessment'].isin(get_test_not_needed_assessment_states())]
    

def get_test_needed_files(assessment: pd.DataFrame) -> pd.DataFrame:
    return assessment[assessment['assessment'].isin(get_test_needed_assessment_states())]


def get_executed_files(assessment: pd.DataFrame) -> pd.DataFrame:
    return assessment[assessment['assessment'].isin(get_executed_assessment_states())] 


def get_never_executed_files(assessment: pd.DataFrame) -> pd.DataFrame:
    return assessment[assessment['assessment'].isin(get_not_those_states(get_executed_assessment_states()))]

def get_test_resources_by_regex(assessment_frame: pd.DataFrame, test_resource_dirs: List[re.Pattern], complement: bool=False) -> pd.DataFrame:
    
    def regex_filter(val: str, regex_list: List[re.Pattern]) -> bool:
        if val:
            ret_val = any([re.search(regex, val) for regex in regex_list])
            return ret_val if not complement else not ret_val
        
        return False
                
    return assessment_frame[assessment_frame['uniformPath'].apply(regex_filter, regex_list=test_resource_dirs)]

# returns the percentage of test resources in the given dataframe (which has to have the column 'uniformPath'!)
def get_test_resources_in_dataframe(assessment: pd.DataFrame, test_resource_dirs: List[str] = []) -> pd.DataFrame:
    if test_resource_dirs == []:
        return pd.DataFrame([], columns=assessment.columns)

    new_content = []
    for _, row in assessment.iterrows():
        directory = '/'.join((tmp_ls:=row['uniformPath'].split('/'))[:len(tmp_ls)-1])
        # still misses subdirectories
        if directory in test_resource_dirs:
            new_content.append(row)
    
    return pd.DataFrame(new_content, columns=assessment.columns)
    
def show_file_distribution_pie_chart(assessment: pd.DataFrame, filename: str, n_largest=5) -> None:
    
    sizes = assessment.loc[:, 'absolute_file_numbers']
    sum_of_all = sizes.sum()
    n_largest_sizes = sizes.nlargest(n=n_largest)
    sum_of_nlargest_sizes = n_largest_sizes.sum()

    n_largest_sizes = pd.concat([n_largest_sizes, pd.Series({'Others':sum_of_all-sum_of_nlargest_sizes})])
    labels = ["*."+index if index != 'Others' else index for index in n_largest_sizes.index]

    figure, axis = plt.subplots()

    plt.rcParams.update({
            "text.usetex": True,
            "font.family": "sans-serif",
            "font.sans-serif": "Helvetica",
        }
    )

    def make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            val = int(round(pct*total/100.0))
            if pct < 2:
                return ''
            return '{p:.2f}\%'.format(p=pct)
        return my_autopct

    axis.pie(n_largest_sizes, labels=labels, autopct=make_autopct(n_largest_sizes), startangle=90, colors=get_tum_colors())
    axis.axis('equal')

    plt.savefig(filename)


def get_percent_string(divident: int, divisor: int) -> str:
    return f'{divident/float(divisor)*100:.2f}%'

def print_metrics_for_one_assessment(assessment_frame: pd.DataFrame, test_resource_regex_list: List[re.Pattern]=[]):

    total_num_rows = len(assessment_frame)
    print(f'Total Number of Entries: {total_num_rows}\n')

    executed_dataframe = assessment_frame[assessment_frame['assessment'].isin(get_executed_assessment_states())]
    total_num_executed = len(executed_dataframe)

    print(f'Total Number of Entries that have been detected as executed: {total_num_executed} ({get_percent_string(total_num_executed, total_num_rows)})\n')
    print(f'Total Number of Entries that have not been detected as executed: {(not_excecuted:=total_num_rows - total_num_executed)} ({get_percent_string(not_excecuted, total_num_rows)})\n')


    executed_test_resources = get_test_resources_by_regex(executed_dataframe, test_resource_regex_list)
    num_of_test_resources_executed = len(executed_test_resources)

    not_excecuted_frame = get_never_executed_files(assessment_frame)
    print(len(not_excecuted_frame))
    never_executed_test_resources = get_test_resources_by_regex(not_excecuted_frame, test_resource_regex_list)
    num_of_test_resources_never_executed = len(never_executed_test_resources)

    print(f'Total Number of Entries that are positive and test resources: {num_of_test_resources_executed} ({get_percent_string(num_of_test_resources_executed, total_num_executed)})')
    print(f'Total Number of Entries that are negative and test resources: {num_of_test_resources_never_executed} ({get_percent_string(num_of_test_resources_never_executed, len(not_excecuted_frame))})')


    sufficiently_tested_dataframe = assessment_frame[assessment_frame['assessment'].isin(get_test_not_needed_assessment_states())]
    print(f'Total Number of sufficiently tested Entries: {(sufficiently_tested_num:=len(sufficiently_tested_dataframe))} ({get_percent_string(sufficiently_tested_num, total_num_rows)})\n')

    not_sufficiently_tested_dataframe = assessment_frame[assessment_frame['assessment'].isin(get_test_needed_assessment_states())]
    print(f'Total Number of not sufficiently tested Entries: {(not_sufficiently_tested_num:=len(not_sufficiently_tested_dataframe))} ({get_percent_string(not_sufficiently_tested_num, total_num_rows)})\n')

    added_files_frame = assessment_frame[assessment_frame['assessment'].isin(get_file_added())]
    num_added_files =len(added_files_frame)

    modified_files_frame = assessment_frame[assessment_frame['assessment'].isin(get_file_modified())]
    num_modified_files =len(modified_files_frame)

    print(f'Total Number of Files that have been added and not modified later: {num_added_files} ({get_percent_string(num_added_files, total_num_rows)}) == {get_percent_string(num_added_files, num_added_files+num_modified_files)} of all changed files\n')
    print(f'Total Number of Files that have been added and modified later: {num_modified_files} ({get_percent_string(num_modified_files, total_num_rows)}) == {get_percent_string(num_modified_files, num_added_files+num_modified_files)} of all changed files\n')

    test_resources_frame = get_test_resources_by_regex(assessment_frame, test_resource_regex_list)
    num_of_test_resources =len(test_resources_frame)
    not_test_resources_frame = get_test_resources_by_regex(assessment_frame, test_resource_regex_list, complement=True)
    num_of_not_test_resources = len(not_test_resources_frame)
    if not test_resource_regex_list:
        print("No test resource directory regexes given\n")
    else:
        print(f'Total Number Test Resources Files in the Assessment: {num_of_test_resources} ({get_percent_string(num_of_test_resources, total_num_rows)})\n')
        print(f'Total number of Test Resource Files detected executed: {(total_num_test_resource_executed:=len(test_resources_frame[test_resources_frame["assessment"].isin(get_executed_assessment_states())]))} ({get_percent_string(total_num_test_resource_executed, num_of_test_resources)})\n')
        print(f'Total Number of Not Test Resources in the Assessment: {num_of_not_test_resources} ({get_percent_string(num_of_not_test_resources, total_num_rows)})\n')
        print(f'Total Number of Not Test Resources detected executed: {(num_not_test_resource_executed:=len(not_test_resources_frame[not_test_resources_frame["assessment"].isin(get_executed_assessment_states())]))} ({get_percent_string(num_not_test_resource_executed, num_of_not_test_resources)})\n')


def get_positives_not_in_real_read(no_real_read_frame: pd.DataFrame, real_read_frame: pd.DataFrame) -> pd.DataFrame:
    prrf = get_test_not_needed_files(real_read_frame)
    pnrrf = get_test_not_needed_files(no_real_read_frame)

    df_all = pnrrf.merge(prrf.drop_duplicates(), on=['uniformPath'], how='left', indicator=True)
    return df_all[df_all['_merge'] == 'left_only']

def get_positives_not_in_real_read_2(no_real_read_frame: pd.DataFrame, real_read_frame: pd.DataFrame) -> List[str]:
    prrf = get_test_not_needed_files(real_read_frame)
    pnrrf = get_test_not_needed_files(no_real_read_frame)

    uniformPaths_in_prrf = np.unique(prrf['uniformPath'].values)
    uniformPaths_in_pnrrf = np.unique(pnrrf['uniformPath'].values)

    not_in_prrf = []
    for uniform_path in uniformPaths_in_pnrrf:
        if uniform_path not in uniformPaths_in_prrf:
            not_in_prrf.append(uniform_path)

    return not_in_prrf

def extend_frame_for_manual_exploration(frame: pd.DataFrame, test_resource_dirs: List[re.Pattern]) -> pd.DataFrame:
    frame = expand_dataframe_with_test_resource(frame, test_resource_dirs)
    frame = expand_dataframe_with_file_types(frame)
    return frame

def stacked_bar_chart_read_intent():
    labels = ['Jabref', 'Teamscale', 'Ebean']

    no_real_read_vals = [550, 3029, 277]
    real_read_vals = [543, 0, 70]

    width = 0.35

    fig, ax = plt.subplots()

    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "sans-serif",
        "font.sans-serif": "Helvetica",
        }
    )

    colors = get_tum_colors(2)

    ax.bar(labels, no_real_read_vals, width, label='Evaluation', color=colors[0])
    ax.bar(labels, real_read_vals, width, label='Evaluation Variant "Only Read"', color=colors[1])

    ax.set_ylabel('\#Positives')
    ax.legend()

    plt.show()

def main() -> None:

    arg_options: Arg_Options = parse_args()
    json_file_path = arg_options.assessment_file_path
    dataframe: pd.DataFrame = pd.read_json(json_file_path)

    tested_sufficiently = get_test_not_needed_files(dataframe)
    not_tested_sufficiently = get_test_needed_files(dataframe)
    executed = get_executed_files(dataframe)
    not_executed = get_never_executed_files(dataframe)
    all_files = dataframe


    print(f'Percentage of overall test_resources: {(get_test_resources_in_dataframe(dataframe, ["src/test/resources"]).loc[:, "uniformPath"].unique().size/dataframe.loc[:, "uniformPath"].unique().size*100):.2f}%')
    print(f'Percentage of test_resources in tested_sufficiently: {(get_test_resources_in_dataframe(tested_sufficiently, ["src/test/resources"]).loc[:, "uniformPath"].unique().size/tested_sufficiently.loc[:, "uniformPath"].unique().size*100):.2f}%')
    print(f'Percentage of test_resources in not_tested_sufficiently: {(get_test_resources_in_dataframe(not_tested_sufficiently, ["src/test/resources"]).loc[:, "uniformPath"].unique().size/not_tested_sufficiently.loc[:, "uniformPath"].unique().size*100):.2f}%')


    plt.show()

if __name__ == '__main__':
    main()