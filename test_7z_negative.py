# from checkout import ssh_checkout
from sshcheckers import ssh_checkout_negative
import yaml
import time

with open("config.yaml") as f:
    data = yaml.safe_load(f)

stat_file = open("stat.txt", "a")


def test_step1(clear_folders, make_files, make_badarx):
    # test1
    assert ssh_checkout_negative(data["host"], data["user"], "11",
                        "cd {}; 7z -t{} e badarx.7z -o{} -y".format(data["folder_out"], data["archive_type"],
                                                                    data["folder_ext"]),
                        "ERROR"), "Test1 Fail"
    # Writing stats to stat.txt
    with open("stat.txt", "a") as stat_file:
        stat_file.write(
            "{}, {}, {}, {}\n".format(time.time(), data["count_file"], data["size_file"], open("/proc/loadavg").read()))


def test_step2(clear_folders, make_files, make_badarx):
    # test2
    assert ssh_checkout_negative(data["host"], data["user"], "11",
                        "cd {}; 7z -t{} t badarx.7z".format(data["folder_out"], data["archive_type"]),
                        "ERROR"), "Test2 Fail"
    # Writing stats to stat.txt
    with open("stat.txt", "a") as stat_file:
        stat_file.write(
            "{}, {}, {}, {}\n".format(time.time(), data["count_file"], data["size_file"], open("/proc/loadavg").read()))
