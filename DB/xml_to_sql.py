#TODO : Find way to resuce promo sql - allocate colums according to types, see if there is non usable data
#TODO: Implement fill dict for prices xml
#TODO: Add stores.xml insertion to db


import pandas as pd
import sqlite3
import os
from DB.xsd_validator import char_int_split
import xml.etree.ElementTree as ET
import time
from DB.db_utils import fill_dict_keys, create_table_from_list , get_ordered_columns_names_from_table,\
    tree_item_to_dict, fix_dict_values

def prices_xml_to_panda_dataframe(xml_file):

    inner_data = pd.read_xml(xml_file, xpath="/root/Items/Item")
    num_of_items = len(inner_data.index)

    outer_data = pd.read_xml(xml_file, xpath="/root")
    outer_data = outer_data.drop('Items', axis=1)
    outer_data = pd.concat([outer_data]*num_of_items, ignore_index=True)

    full_data = pd.concat([inner_data, outer_data], axis=1)

    return full_data
def promo_xml_to_panda_dataframe(xml_file):
    inner_data = pd.read_xml(xml_file, xpath="/root/Promotions/Promotion")
    num_of_items = len(inner_data.index)

    outer_data = pd.read_xml(xml_file, xpath="/root")
    outer_data = outer_data.drop('Promotions', axis=1)
    outer_data = pd.concat([outer_data] * num_of_items, ignore_index=True)

    full_data = pd.concat([inner_data, outer_data], axis=1)

    return full_data
def insert_panda_dataframe_to_db(dataframe, db, table):
    conn = sqlite3.connect(db)
    dataframe.to_sql(table, conn, if_exists='append' )
def insert_prices_xml_from_dir_to_db(dir_path, db, table, prices_type="PriceFull"):
    for file in os.listdir(dir_path):
        full_file_path = os.path.join(dir_path , file)
        file_name, file_extension = os.path.splitext(file)
        file_type = char_int_split(file)[0]

        if file_extension == '.xml' and file_type == prices_type:
            insert_panda_dataframe_to_db(prices_xml_to_panda_dataframe(full_file_path), db, table)

            print(f"Inserted {file} to {db}.")
def insert_promo_xml_from_dir_to_db(dir_path, db, table, promo_type="PromoFull"):
    for file in os.listdir(dir_path):
        full_file_path = os.path.join(dir_path , file)
        file_name, file_extension = os.path.splitext(file)
        file_type = char_int_split(file)[0]

        if file_extension == '.xml' and file_type == promo_type:
            try:
                insert_promo_xml_to_db(full_file_path,db , table)

                print(f"Inserted {file} to {db}.")
            except Exception as err:
                print(f'{file}' , err)
def insert_promo_xml_to_db(promo_xml_file, db_path, table_name):
    # extracting promos xm; data and inserting to sql lite db.

    # connect to sql db.
    conn = sqlite3.connect(db_path)

    # get ordered data columns from table
    ordered_columns_names = get_ordered_columns_names_from_table(db_path, table_name)

    # get outer and inner data of promos xml file
    output = pd.DataFrame()
    tree = ET.parse(promo_xml_file)
    outer_data = tree.findall('./')
    promos = tree.findall(".//Promotion")
    promos_elem = tree.find(".//Promotions")
    outer_data.remove(promos_elem)

    # first loop to on all inner promotions
    for promo in promos:
        promo_items = promo.findall('.//Item')
        promo_items_elem = promo.find('.//PromotionItems')
        promo.remove(promo_items_elem)

        add_info = promo.findall('.//AdditionalRestrictions/')
        add_info_elem = promo.find('.//AdditionalRestrictions')
        promo.extend(add_info)
        promo.remove(add_info_elem)

        # second loop on all the items in promotion
        for item in promo_items:
            item.extend(promo)

            # create a single data atom of 'item/promotion/outer-data" dict
            item_dict = tree_item_to_dict(item)
            item_dict = fill_dict_keys(ordered_columns_names, item_dict)
            item_dict = fix_dict_values(item_dict)

            #insert data to sql
            s_ = "','".join(item_dict.values())
            sql = f"INSERT INTO {table_name} VALUES ('{s_}')"
            conn.execute(sql)

    conn.commit()
    return conn


if __name__ == '__main__':

    DB_PATH = r'C:\Users\as\Sooper\DB\db\PriceFull.db'
    TABLE_NAME = 'tabletry1'
    ORDERED_PRICE_COLUMNS = ['ItemCode', 'ItemType', 'IsGiftItem',
                             'PromotionId', 'AllowMultipleDiscounts',
                             'PromotionDescription', 'PromotionUpdateDate',
                             'PromotionStartDate', 'PromotionStartHour',
                             'PromotionEndDate', 'PromotionEndHour', 'IsWeightedPromo',
                             'MinQty', 'DiscountType', 'RewardType', 'DiscountRate',
                             'MinNoOfItemOfered', 'Clubs', 'AdditionalIsCoupon', 'AdditionalGiftCount',
                             'AdditionalIsTotal', 'AdditionalIsActive']
    PROMOFULL_XML = r'C:\Users\as\Sooper\SeleniumDownload\PromoFull7290027600007-013-202208190300.xml'
    DIR_PATH = r'C:\Users\as\Sooper\SeleniumDownload'

    start_time = time.time()

    create_table_from_list(DB_PATH,TABLE_NAME,ORDERED_PRICE_COLUMNS)


    #insert_promo_xml_to_db(PROMOFULL_XML, DB_PATH , TABLE_NAME)

    insert_promo_xml_from_dir_to_db(DIR_PATH, DB_PATH,TABLE_NAME)
    print("--- %s seconds ---" % (time.time() - start_time))
