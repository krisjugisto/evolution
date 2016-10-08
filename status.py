#!/usr/bin/python

import re, argparse
from os import listdir
from os.path import isfile, isdir


conf_file = "evolution.conf"
log_file  = "evolution.log"


def get_number_of_cur_trials(path):
    log = path+"/"+log_file
    if not isfile(log):
        return 0
    return sum(1 for line in open(log))


def is_experiment(path):
    return isdir(path) \
        and isfile(path+"/"+conf_file) \
        and isfile(path+"/"+log_file)

def get_number_of_max_trials(path):
    conf = path+"/"+conf_file
    with open(conf) as f:
        data = f.read()
    m = re.search("MAX_TRIALS = (\d+)", data)
    if m:
        return int(m.groups()[0])
    print("ERROR: Did not find max. trials entry in {0}".format(conf))
    return 1 # avoid devision by zero


def find_experiments(path, filt):
    total = 0
    number = 0
    dirs = [d for d in listdir(path)]
    dirs.sort()
    for d in dirs:
        if filt and filt not in d:
            continue
        exp_path = path+"/"+d
        if not is_experiment(exp_path):
            return

        max_trials = get_number_of_max_trials(exp_path)
        cur_trials = get_number_of_cur_trials(exp_path)
        result = int(cur_trials*100.0/max_trials)
        print("{0:32} {1:3d}% ({2:6d}/{3:6d}) {4}".format(d, result, cur_trials, max_trials, "OK." if result==100 else ""))
        number += 1
        total += result
    if number > 0:
        print("-"*37)
        print("{0:32} {1:3d}% {2}".format("Total: ", total/number, "COMPLETE." if int(total/number)==100 else ""))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filter' , default='')
    parser.add_argument('-p', '--path'   , default='../data/exp')
    args = parser.parse_args()

    filt = str(args.filter)
    path  = str(args.path)
    if isdir(path):
        find_experiments(path, filt)
    else:
        print("ERROR: Wrong path.")
        exit(-1)

    print("____\nDONE.")

if __name__ == "__main__": main()

