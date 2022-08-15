import os


def EmptyDir(path):
    for f in os.listdir(path):
        os.remove(os.path.join(path, f))
    number_files = CountNumOfFiles(path)

    if number_files == 0:
        return 'SUCCESS'

    else:
        raise Exception("Could not empty folder.")


def CountNumOfFiles(path):
    lst = os.listdir(path)  # your directory path
    number_files = len(lst)
    return number_files

