import xmlschema
import os
import re

def validateXmlFile(xml_path, xsd_path):
    schema = xmlschema.XMLSchema(xsd_path)
    try:
        result = schema.validate(xml_path)
        return "Valid"

    except Exception as e:
        return e

def CharIntSplit(s):
    return re.split(r"\d+", s)


def validateDir(dir_path, xsd_path, toprint = None):
    xsd_type = os.path.basename(xsd_path).split('.')[0]

    for file in os.listdir(dir_path):
        full_file_path = os.path.join(dir_path , file)
        file_name, file_extension = os.path.splitext(file)
        file_type = CharIntSplit(file)[0]

        if file_extension == '.xml' and file_type == xsd_type:
            val_result = validateXmlFile(full_file_path, xsd_path)

            if toprint == True:
                print(f"File name {file} validation status is: {val_result}")


            if val_result != 'Valid':
                raise Exception(f"File name {file} validation failed with status: {val_result}")


    return f"Folder: {dir_path} relevant files are valid with Schema: {xsd_path}."

xml_path = r'C:\Users\as\Sooper\SeleniumDownload\Price7290027600007-001-202208181900.xml'
xsd_path = r'C:\Users\as\Sooper\DB\PriceFull.xsd'
dir_path = r'C:\Users\as\Sooper\SeleniumDownload'

print(validateDir(dir_path ,xsd_path, toprint= True))