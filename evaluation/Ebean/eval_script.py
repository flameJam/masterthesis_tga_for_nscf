import tga_assessment_evaluation_tools as tga_utils
import pandas as pd
import re
import argparse
import datetime
import matplotlib.pyplot as plt


no_real_read_report_json_path = "assessments/report_no_real_read.json"
real_read_report_json_path = "assessments/real_read_report_2022-10-29.json"

test_resources_regex_list = [re.compile(".*/test/resources/.+"), re.compile("ebean-test/testconfig/.+")]

figure_location='<hardcoded_figure_location>'

def main():
    no_real_read_frame = pd.read_json(no_real_read_report_json_path)
    real_read_frame = pd.read_json(real_read_report_json_path)

    print("# Evaluation metrics for Jabref Assessments")
    print("## General Metrics for Jabref Assessment, no real read:")
    tga_utils.print_metrics_for_one_assessment(no_real_read_frame, test_resources_regex_list)
    
    print("")

    print("## General Metrics for Jabref Assessment, real read:")
    tga_utils.print_metrics_for_one_assessment(real_read_frame, test_resources_regex_list)

def false_positives(n_of_samples):
    no_real_read_frame = pd.read_json(no_real_read_report_json_path)
    real_read_frame = pd.read_json(real_read_report_json_path)

    no_real_read_positives = tga_utils.get_test_not_needed_files(no_real_read_frame)
    real_read_positives = tga_utils.get_test_not_needed_files(real_read_frame)

    no_real_read_sample_frame = tga_utils.draw_samples(no_real_read_positives, n_of_samples)
    print("Positive Samples for no real read:")
    print(no_real_read_sample_frame)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    no_real_read_sample_frame.to_csv(f"../samples/no_real_read_samples_{timestamp}", index=False)

    real_read_sample_frame = tga_utils.draw_samples(real_read_positives, n_of_samples)
    print("Positive Samples for no real read:")
    print(real_read_sample_frame)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    real_read_sample_frame.to_csv(f"../samples/real_read_samples_{timestamp}", index=False)

def draw_figure(figure_arg: str):
    no_real_read_frame = pd.read_json(no_real_read_report_json_path)
    real_read_frame = pd.read_json(real_read_report_json_path)

    if figure_arg == 'file_distribution_all':
        tga_utils.show_file_distribution_pie_chart(
            tga_utils.get_file_type_distribution(no_real_read_frame),
            figure_location+ '/' + figure_arg + "_no_real_read.png"
            )
        tga_utils.show_file_distribution_pie_chart(
            tga_utils.get_file_type_distribution(real_read_frame),
            figure_location+ '/' + figure_arg + "real_read.png"
            )
    elif figure_arg == 'file_distribution_positives':
        no_real_read_positives = tga_utils.get_test_not_needed_files(no_real_read_frame)
        real_read_positives = tga_utils.get_test_not_needed_files(real_read_frame)

        tga_utils.show_file_distribution_pie_chart(
            tga_utils.get_file_type_distribution(no_real_read_positives),
            figure_location+ '/' + figure_arg + "_no_real_read.png"
            )
        tga_utils.show_file_distribution_pie_chart(
            tga_utils.get_file_type_distribution(real_read_positives),
            figure_location+ '/' + figure_arg + "_real_read.png"
            )
    elif figure_arg == 'file_distribution_negatives':
        no_real_read_negatives = tga_utils.get_test_needed_files(no_real_read_frame)
        real_read_negatives = tga_utils.get_test_needed_files(real_read_frame)

        tga_utils.show_file_distribution_pie_chart(
            tga_utils.get_file_type_distribution(no_real_read_negatives),
            figure_location+ '/' + figure_arg + "_no_real_read.png"
            )
        tga_utils.show_file_distribution_pie_chart(
            tga_utils.get_file_type_distribution(real_read_negatives),
            figure_location+ '/' + figure_arg + "_real_read.png"
            )
    elif figure_arg == 'distributions_test_resources':
        no_real_read_positives = tga_utils.get_test_not_needed_files(no_real_read_frame)
        real_read_positives = tga_utils.get_test_not_needed_files(real_read_frame)
        no_real_read_negatives = tga_utils.get_test_needed_files(no_real_read_frame)
        real_read_negatives = tga_utils.get_test_needed_files(real_read_frame)

        nrrp_test_resources = tga_utils.get_test_resources_by_regex(no_real_read_positives, test_resources_regex_list)
        rrp_test_resources = tga_utils.get_test_resources_by_regex(real_read_positives, test_resources_regex_list)

        nrrn_test_resources = tga_utils.get_test_resources_by_regex(no_real_read_negatives, test_resources_regex_list)
        rrn_test_resources = tga_utils.get_test_resources_by_regex(real_read_negatives, test_resources_regex_list)

        
        draw_pie([(val_1:=(float(len(nrrp_test_resources))/len(no_real_read_positives)*100.0)), 100.0-val_1], ["Test Resources", "Others"], figure_location + "/no_real_read_positives_test_resource_pie.png")
        draw_pie([(val_1:=(float(len(rrp_test_resources))/len(real_read_positives)*100.0)), 100.0-val_1], ["Test Resources", "Others"], figure_location + "/real_read_positives_test_resource_pie.png")
        draw_pie([(val_1:=(float(len(nrrn_test_resources))/len(no_real_read_negatives)*100.0)), 100.0-val_1], ["Test Resources", "Others"], figure_location + "/no_real_read_negatives_test_resource_pie.png")
        draw_pie([(val_1:=(float(len(rrn_test_resources))/len(real_read_negatives)*100.0)), 100.0-val_1], ["Test Resources", "Others"], figure_location + "/real_read_negatives_test_resource_pie.png")
        
        
def draw_pie(relative_values, labels, filename):
    figure, axis = plt.subplots()

    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "sans-serif",
        "font.sans-serif": "Helvetica",
        }
    )

    axis.pie(relative_values, labels=labels, autopct=lambda p:f'{p:.2f}\%', startangle=90, colors=tga_utils.get_tum_colors())
    axis.axis('equal')

    plt.savefig(filename)
    
def print_frame_with_type(frame: pd.DataFrame, type: str, file_name: str):
    copy_to_work_with = frame.copy()
    tga_utils.expand_dataframe_with_file_types(copy_to_work_with)

    copy_to_work_with[copy_to_work_with['file_ending'] == type].to_csv(file_name)

def print_not_in_ral_read():
    no_real_read_frame = pd.read_json(no_real_read_report_json_path)
    real_read_frame = pd.read_json(real_read_report_json_path)

    not_in_real_read = tga_utils.get_positives_not_in_real_read(no_real_read_frame, real_read_frame)

    not_in_real_read.to_csv("positives_not_in_real_read_for_manual_exploration_3.csv")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--false_positive_samples', '-fps', nargs=1, default=[0], help='Samples to draw from each assessment', type=int)
    parser.add_argument('--figure', '-f', nargs=1, default=['None'], help='draw, output and safe a certain figure', type=str)

    args  = parser.parse_args()

    if (n_of_samples:=int(args.false_positive_samples[0])) > 0:
        false_positives(n_of_samples)
    elif (figure_arg:=args.figure[0]) != 'None':
        draw_figure(figure_arg)
    else:
        main()