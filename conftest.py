import datetime
import random
import string
import subprocess
import pytest
# from checkout import ssh_checkout
from sshcheckers import ssh_checkout, ssh_getout
import yaml

with open("config.yaml") as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folders():
    return ssh_checkout(data["host"], data["user"], "11",
                        "mkdir {} {} {} {}".format(data["folder_in"], data["folder_out"], data["folder_ext"],
                                                   data["folder_badarx"]), "")


@pytest.fixture()
def clear_folders():
    return ssh_checkout(data["host"], data["user"], "11",
                        "rm -rf {}/* {}/* {}/* {}/*".format(data["folder_in"], data["folder_out"], data["folder_ext"],
                                                            data["folder_badarx"]), "")


@pytest.fixture()
def make_files():
    list_off_files = []
    for i in range(data["count_file"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout(data["host"], data["user"], "11",
                        "cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["folder_in"],
                                                                                               filename,
                                                                                               data["size_file"]),
                        ""):
            list_off_files.append(filename)
    return list_off_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not ssh_checkout(data["host"], data["user"], "11", "cd {}; mkdir {}".format(data["folder_in"], subfoldername),
                        ""):
        return None, None
    if not ssh_checkout(data["host"], data["user"], "11",
                        "cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data["folder_in"],
                                                                                                  subfoldername,
                                                                                                  testfilename), ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture()
def make_badarx():
    ssh_checkout(data["host"], data["user"], "11",
                 "cd {}; 7z a {}/badarx.7z".format(data["folder_in"], data["folder_badarx"]),
                 "Everything is Ok"), "Test Fail"
    ssh_checkout(data["host"], data["user"], "11", "truncate -s 1 {}/badarx.7z".format(data["folder_badarx"]),
                 "Everything is Ok"), "Test Fail"
    yield "badarx"
    ssh_checkout(data["host"], data["user"], "11", "rm -f {}/badarx.7z".format(data["folder_badarx"]), "")
