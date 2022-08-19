import pandas as pd
import sqlite3
import os
from DB.XsdValidator import CharIntSplit


def PriceXml2Pandas(xmlfile):

    inner_data = pd.read_xml(xmlfile , xpath="/root/Items/Item")
    num_of_items = len(inner_data.index)

    outer_data = pd.read_xml(xmlfile , xpath="/root")
    outer_data = outer_data.drop('Items', axis=1)
    outer_data = pd.concat([outer_data]*num_of_items, ignore_index=True)

    full_data = pd.concat([inner_data, outer_data], axis=1)

    return full_data

def Insert_dataframe_2_DB(dataframe, db, table):
    conn = sqlite3.connect(db)
    dataframe.to_sql(table, conn, if_exists='append')


def Price_Insert_dir_2_DB(dir_path, db , table, general_type):
    for file in os.listdir(dir_path):
        full_file_path = os.path.join(dir_path , file)
        file_name, file_extension = os.path.splitext(file)
        file_type = CharIntSplit(file)[0]

        if file_extension == '.xml' and file_type == general_type:
            Insert_dataframe_2_DB(PriceXml2Pandas(full_file_path),db , table)

            print(f"Inserted {file} to {db}.")


if __name__ == '__main__':
    dir_path = r'C:\Users\as\Sooper\SeleniumDownload'
    db = r'C:\Users\as\Sooper\DB\db\PriceFull.db'
    table = 'Items'
    general_type = 'PriceFull'

    Price_Insert_dir_2_DB(dir_path , db , table , general_type)

    dir_path = r'C:\Users\as\Sooper\SeleniumDownload'
    db = r'C:\Users\as\Sooper\DB\db\Price.db'
    table = 'Items'
    general_type = 'Price'

    Price_Insert_dir_2_DB(dir_path, db, table, general_type)

