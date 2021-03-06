import sys
import os
import getopt
from bs4 import BeautifulSoup


BRESEQ_OUTPUT_DIR = "output"
BRESEQ_OUTPUT_HTML = "index.html"
BRESEQ_OUTPUT_LOG = "log.txt"
BRESEQ_LOG_OUTPUT_NAME_FLAG = "-o"
BRESEQ_MUT_TR_TAG = "normal_table_row"


def main(argv):
    # check which index.html files exist in current dir.
    parent_dir = ""

    try:
        opts, args = getopt.getopt(argv,
                                   "i:",
                                   ["input"])
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-i", "--input"):
            parent_dir = arg

    sample_artf_count_dict = {}
    if parent_dir != "":
        sample_dir_list = get_dir_list(parent_dir)
        sample_html_path_dict = get_sample_html_path_dict(sample_dir_list)
        for sample in sample_html_path_dict.keys():
            sample_artf_count_dict[sample] = get_sample_artf_count_dict(sample_html_path_dict[sample])


def get_sample_artf_count_dict(sample_html_path):
    sample_artf_count_dict = {}
    soup_html = get_beautifulsoup_html(sample_html_path)
    all_table_row_list = soup_html.find_all('tr')
    mutation_count = 0
    for table_row in all_table_row_list:
        if BRESEQ_MUT_TR_TAG in str(table_row):
            mutation_count += 1
    return sample_artf_count_dict


def get_beautifulsoup_html(sample_html_path):
    with open(sample_html_path) as infile:
        bs_html_file = BeautifulSoup(infile, "html.parser")
    return bs_html_file


def get_dir_list(parent_dir):
    dirs = [parent_dir+d for d in os.listdir(parent_dir) if os.path.isdir(parent_dir+d)]
    return dirs


def get_sample_html_path_dict(dir_list):
    sample_dict = {}
    for dir in dir_list:
        breseq_log_path = dir + '/' + BRESEQ_OUTPUT_DIR + '/' + BRESEQ_OUTPUT_LOG
        breseq_html_path = dir + '/' + BRESEQ_OUTPUT_DIR + '/' + BRESEQ_OUTPUT_HTML
        if os.path.exists(breseq_log_path) and os.path.exists(breseq_html_path):
            sample_name = get_sample_name(breseq_log_path)
            sample_dict[sample_name] = breseq_html_path

    return sample_dict


def get_sample_name(breseq_log_path):
    sample_name = ""
    with open(breseq_log_path) as input_log:
        for line in input_log:
            if BRESEQ_LOG_OUTPUT_NAME_FLAG in line:
                item_list = line.split(' ')
                for idx, item in enumerate(item_list):
                    if item == BRESEQ_LOG_OUTPUT_NAME_FLAG:
                        sample_name = item_list[idx+1]
    return sample_name


if __name__ == "__main__":
    main(sys.argv[1:])