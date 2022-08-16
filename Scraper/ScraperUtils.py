import os
import shutil
import gzip

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

def ExtractAndSaveGzip(gzFilePath):
    file_name, file_extension = os.path.splitext(gzFilePath)

    if file_extension != '.gz':
        raise Exception("File extension is not gz. Can't extract file.")
        return

    with gzip.open(gzFilePath, 'rb') as f_in:
        with open(file_name, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


