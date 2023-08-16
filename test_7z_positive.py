from checkout import checkout_positive
import yaml
import time

with open("config.yaml") as f:
    data = yaml.safe_load(f)

stat_file = open("stat.txt", "a")


def test_step1(make_folders, clear_folders, make_files):
    # test1
    res1 = checkout_positive(
        "cd {}; 7z -t{} a {}/arx1.7z".format(data["folder_in"], data["archive_type"], data["folder_out"]),
        "Everything is Ok"), "Test1 Fail"
    res2 = checkout_positive("ls {}".format(data["folder_out"]), "arx.7z"), "Test1 Fail"
    assert res1 and res2, "Test1 Fail"
    # Writing stats to stat.txt
    with open("stat.txt", "a") as stat_file:
        stat_file.write(
            "{}, {}, {}, {}\n".format(time.time(), data["count_file"], data["size_file"], open("/proc/loadavg").read()))


def test_step2(clear_folders, make_files):
    # test2
    res = []
    res.append(checkout_positive(
        "cd {}; 7z -t{} a {}/arx1.7z".format(data["folder_in"], data["archive_type"], data["folder_out"]),
        "Everything is Ok"))
    res.append(checkout_positive(
        "cd {}; 7z -t{} e arx1.7z -o{} -y".format(data["folder_out"], data["archive_type"], data["folder_ext"]),
        "Everything is Ok"))
    for item in make_files:
        res.append(checkout_positive("ls {}".format(data["folder_ext"]), item))
    assert all(res)
    # Writing stats to stat.txt
    with open("stat.txt", "a") as stat_file:
        stat_file.write(
            "{}, {}, {}, {}\n".format(time.time(), data["count_file"], data["size_file"], open("/proc/loadavg").read()))


def test_step3():
    # test3
    assert checkout_positive(
        "cd {}; 7z -t{} t {}/arx1.7z".format(data["folder_in"], data["archive_type"], data["folder_out"]),
        "Everything is Ok"), "Test3 Fail"

def test_step4():
    # test4
    assert checkout_positive(
        "cd {}; 7z -t{} u {}/arx1.7z".format(data["folder_in"], data["archive_type"], data["folder_out"]),
        "Everything is Ok"), "Test4 Fail"
    # Writing stats to stat.txt
    with open("stat.txt", "a") as stat_file:
        stat_file.write(
            "{}, {}, {}, {}\n".format(time.time(), data["count_file"], data["size_file"], open("/proc/loadavg").read()))


def test_step5(clear_folders, make_files):
    # test5
    res = []
    res.append(checkout_positive(
        "cd {}; 7z -t{} a {}/arx1.7z".format(data["folder_in"], data["archive_type"], data["folder_out"]),
        "Everything is Ok"))
    for item in make_files:
        res.append(
            checkout_positive("cd {}; 7z -t{} l arx1.7z".format(data["folder_out"], data["archive_type"]), item))
    assert all(res)
    # Writing stats to stat.txt
    with open("stat.txt", "a") as stat_file:
        stat_file.write(
            "{}, {}, {}, {}\n".format(time.time(), data["count_file"], data["size_file"], open("/proc/loadavg").read()))


def test_step7():
    assert checkout_positive("7z -t{} d {}/arx1.7z".format(data["archive_type"], data["folder_out"]), "Everything is Ok"), "Test7 Fail"
    # Writing stats to stat.txt
    with open("stat.txt", "a") as stat_file:
        stat_file.write(
            "{}, {}, {}, {}\n".format(time.time(), data["count_file"], data["size_file"], open("/proc/loadavg").read()))
