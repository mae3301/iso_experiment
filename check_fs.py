# Usage: python3 check_fs.py

import os
import hashlib
import logging

# set log level to info if you want to refrain from reporting
# sockets that won't open
# alternative: level=logging.DEBUG
logging.basicConfig(filename="report.log",
                    encoding='utf-8', level=logging.DEBUG)


def strip_top_dir(path):
    elements = path.split('/')
    # this index only works if you place iso_experiment in your home folder!
    elements = elements[5:]
    reconstituted = '/'.join(elements)
    reconstituted = '/' + reconstituted
    return reconstituted


def make_directory_dictionary(name, path, my_dict):
    if not os.path.isdir(path):
        if not os.path.islink(path):
            key = strip_top_dir(path)
            my_dict[key] = path
    else:
        for name in os.listdir(path):
            childpath = os.path.join(path, name)
            make_directory_dictionary(name, childpath, my_dict)


def collect_md5_info(truncated_to_full_filepath):
    cicada_only = ['/usr/local/bin/cicada',
                   '/tmp/wisdom',
                   '/usr/local/bin/message.txt',
                   '/usr/local/bin/prime_echo',
                   '/tmp/folly',
                   '/usr/local/bin/message.txt.asc']
    skip = ['/dev/fd/0',
            '/dev/fd/1',
            '/dev/fd/2',
            '/dev/fd/4',
            '/dev/stderr',
            '/dev/stdin',
            '/dev/stdout']
    skip = skip + cicada_only
    md5sum_dict = {}
    for short_filepath, full_filepath in truncated_to_full_filepath.items():
        if short_filepath in skip:
            continue
        try:
            contents = open(full_filepath, 'rb').read()
        except (PermissionError, OSError) as e:
            logging.debug("%s: Could not open %s" % (e, full_filepath))
            continue
        res = hashlib.md5(contents).hexdigest()
        md5sum_dict[short_filepath] = res
    return md5sum_dict


def report_difference(cicada_dict, tinycore_dict):
    num_cicada_files = len(cicada_dict.keys())
    num_tinycore_files = len(tinycore_dict.keys())
    log_str = "There are %s cicada OS files and %s tinycore OS files." % (num_cicada_files, num_tinycore_files)
    logging.info(log_str)
    difference_one = set(cicada_dict.keys()) - set(tinycore_dict.keys())
    difference_two = set(tinycore_dict.keys()) - set(cicada_dict.keys())
    diff_one_files = '\n'.join(difference_one)
    log_str = "The following files are in the cicada OS and not the tinycore OS:\n%s." % diff_one_files
    logging.info(log_str)
    diff_two_files = '\n'.join(difference_two)
    log_str = "The following files are in the tinycore OS and not the cicada OS:\n%s." % diff_two_files
    logging.info(log_str)



if __name__ == "__main__":
    tinycore_dict = {}
    cicada_dict = {}
    cicada_folderpath = '%s/iso_experiment/cicada' % os.environ['HOME']
    tinycore_folderpath = '%s/iso_experiment/tinycore' % os.environ['HOME']
    make_directory_dictionary('tinycore', tinycore_folderpath, tinycore_dict)
    make_directory_dictionary('cicada', cicada_folderpath, cicada_dict)
    report_difference(cicada_dict, tinycore_dict)
    tinycore_md5 = collect_md5_info(tinycore_dict)
    cicada_md5 = collect_md5_info(cicada_dict)
    for file, tinycore_md5hash in tinycore_md5.items():
        cicada_md5hash = cicada_md5[file]
        if tinycore_md5hash != cicada_md5hash:
            report_str = "The following file on the two operating systems is different: %s." % file
            logging.info(report_str)
