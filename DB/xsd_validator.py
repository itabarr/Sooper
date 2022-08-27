import xmlschema
import os
import re

def validate_xml_file(xml_path, xsd_path):
    schema = xmlschema.XMLSchema(xsd_path)
    try:
        result = schema.validate(xml_path)
        return "Valid"

    except Exception as e:
        return e
def char_int_split(s):
    return re.split(r"\d+", s)
def validate_dir(dir_path, xsd_path, to_print=None):
    xsd_type = os.path.basename(xsd_path).split('.')[0]

    for file in os.listdir(dir_path):
        full_file_path = os.path.join(dir_path , file)
        file_name, file_extension = os.path.splitext(file)
        file_type = char_int_split(file)[0]

        if file_extension == '.xml' and file_type == xsd_type:
            val_result = validate_xml_file(full_file_path, xsd_path)

            if to_print == True:
                print(f"File name {file} validation status is: {val_result}")


            if val_result != 'Valid':
                raise Exception(f"File name {file} validation failed with status: {val_result}")


    return f"Folder: {dir_path} relevant files are valid with Schema: {xsd_path}."

if __name__ == '__main__':

    xml_path = r'C:\Users\as\Sooper\SeleniumDownload\Price7290027600007-001-202208181900.xml'
    xsd_path = r'C:\Users\as\Sooper\DB\xsd\PriceFull.xsd'
    dir_path = r'C:\Users\as\Sooper\SeleniumDownload'

    print(validate_dir(dir_path, xsd_path, to_print=True))