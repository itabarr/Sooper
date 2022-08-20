import pandas as pd
import sqlite3
import os
from DB.XsdValidator import CharIntSplit
import xml.etree.ElementTree as ET
import time
from DB.DbUtils import fillDictKeys, createTableFromList

def PriceXmlToPandas(xmlfile):

    inner_data = pd.read_xml(xmlfile , xpath="/root/Items/Item")
    num_of_items = len(inner_data.index)

    outer_data = pd.read_xml(xmlfile , xpath="/root")
    outer_data = outer_data.drop('Items', axis=1)
    outer_data = pd.concat([outer_data]*num_of_items, ignore_index=True)

    full_data = pd.concat([inner_data, outer_data], axis=1)

    return full_data
def PromoXmlToPandas(xmlfile):
    inner_data = pd.read_xml(xmlfile, xpath="/root/Promotions/Promotion")
    num_of_items = len(inner_data.index)

    outer_data = pd.read_xml(xmlfile, xpath="/root")
    outer_data = outer_data.drop('Promotions', axis=1)
    outer_data = pd.concat([outer_data] * num_of_items, ignore_index=True)

    full_data = pd.concat([inner_data, outer_data], axis=1)

    return full_data
def InsertDataframeToDb(dataframe, db, table):
    conn = sqlite3.connect(db)
    dataframe.to_sql(table, conn, if_exists='append' )
def PriceInsertDirToDb(dir_path, db , table, general_type):
    for file in os.listdir(dir_path):
        full_file_path = os.path.join(dir_path , file)
        file_name, file_extension = os.path.splitext(file)
        file_type = CharIntSplit(file)[0]

        if file_extension == '.xml' and file_type == general_type:
            InsertDataframeToDb(PriceXmlToPandas(full_file_path), db, table)

            print(f"Inserted {file} to {db}.")
def PromoInsertDirToDb(dir_path, db , table, general_type):
    for file in os.listdir(dir_path):
        full_file_path = os.path.join(dir_path , file)
        file_name, file_extension = os.path.splitext(file)
        file_type = CharIntSplit(file)[0]

        if file_extension == '.xml' and file_type == general_type:
            InsertDataframeToDb(PromoXmlToPandas(full_file_path), db, table)

            print(f"Inserted {file} to {db}.")
def ParsePromoXml(promoxmlfile , colNames):
    db = sqlite3.connect(r'C:\Users\as\Sooper\DB\db\PromoFull.db')
    cur = db.cursor()


    output = pd.DataFrame()

    tree = ET.parse(promoxmlfile)

    outer_data = tree.findall('./')
    promos = tree.findall(".//Promotion")
    promos_elem = tree.find(".//Promotions")
    outer_data.remove(promos_elem)


    create = True

    for promo in promos:
        promo_items = promo.findall('.//Item')
        promo_items_elem = promo.find('.//PromotionItems')
        promo.remove(promo_items_elem)

        add_info = promo.findall('.//AdditionalRestrictions/')
        add_info_elem = promo.find('.//AdditionalRestrictions')
        promo.extend(add_info)
        promo.remove(add_info_elem)

        for item in promo_items:
            item.extend(promo)
            #PrintXmlNodeChilds(item)

            item_dict = TreeItemToDict(item)
            item_dict = fillDictKeys(colNames, item_dict)
            sql = 'INSERT INTO Promotions ({}) VALUES ({})'.format(
                ','.join(item_dict.keys()),
                ','.join(['?'] * len(item)))
            cur.execute(sql, tuple(item_dict.values()))

            #item_df = pd.DataFrame([item_dict], columns=item_dict.keys())
            #output = pd.concat([output,item_df])


    return output
def TreeItemToDict(item):
    dict = {}
    for child in item:
        dict[child.tag] =  child.text
    return dict
def PrintXmlNodeChilds(root):
    for child in root:
        print(ET.tostring(child))

    print( )
    print( )


if __name__ == '__main__':
    start_time = time.time()
    colNames = ['ItemCode', 'ItemType', 'IsGiftItem', 'PromotionId', 'AllowMultipleDiscounts', 'PromotionDescription', 'PromotionUpdateDate', 'PromotionStartDate', 'PromotionStartHour', 'PromotionEndDate', 'PromotionEndHour', 'IsWeightedPromo', 'MinQty', 'DiscountType', 'RewardType', 'DiscountRate', 'MinNoOfItemOfered', 'Clubs', 'AdditionalIsCoupon', 'AdditionalGiftCount', 'AdditionalIsTotal', 'AdditionalIsActive']

    createTableFromList('./db/try.db', 'try1', colNames)
    df = ParsePromoXml(r'C:\Users\as\Sooper\SeleniumDownload\PromoFull7290027600007-271-202208190300.xml', colNames)
    print("--- %s seconds ---" % (time.time() - start_time))
