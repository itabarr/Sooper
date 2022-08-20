import pandas as pd
import sqlite3
import os
from DB.XsdValidator import CharIntSplit
import xml.etree.ElementTree as ET
import time


def PriceXml2Pandas(xmlfile):

    inner_data = pd.read_xml(xmlfile , xpath="/root/Items/Item")
    num_of_items = len(inner_data.index)

    outer_data = pd.read_xml(xmlfile , xpath="/root")
    outer_data = outer_data.drop('Items', axis=1)
    outer_data = pd.concat([outer_data]*num_of_items, ignore_index=True)

    full_data = pd.concat([inner_data, outer_data], axis=1)

    return full_data
def PromoXml2Pandas(xmlfile):
    inner_data = pd.read_xml(xmlfile, xpath="/root/Promotions/Promotion")
    num_of_items = len(inner_data.index)

    outer_data = pd.read_xml(xmlfile, xpath="/root")
    outer_data = outer_data.drop('Promotions', axis=1)
    outer_data = pd.concat([outer_data] * num_of_items, ignore_index=True)

    full_data = pd.concat([inner_data, outer_data], axis=1)

    return full_data
def Insert_dataframe_2_DB(dataframe, db, table):
    conn = sqlite3.connect(db)
    dataframe.to_sql(table, conn, if_exists='append' )
def Price_Insert_dir_2_DB(dir_path, db , table, general_type):
    for file in os.listdir(dir_path):
        full_file_path = os.path.join(dir_path , file)
        file_name, file_extension = os.path.splitext(file)
        file_type = CharIntSplit(file)[0]

        if file_extension == '.xml' and file_type == general_type:
            Insert_dataframe_2_DB(PriceXml2Pandas(full_file_path),db , table)

            print(f"Inserted {file} to {db}.")
def Promo_Insert_dir_2_DB(dir_path, db , table, general_type):
    for file in os.listdir(dir_path):
        full_file_path = os.path.join(dir_path , file)
        file_name, file_extension = os.path.splitext(file)
        file_type = CharIntSplit(file)[0]

        if file_extension == '.xml' and file_type == general_type:
            Insert_dataframe_2_DB(PromoXml2Pandas(full_file_path),db , table)

            print(f"Inserted {file} to {db}.")
def ParsePromoXml(promoxmlfile):
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
            #print_xml_node_childs(item)

            item_dict = TreeItem2Dict(item)



            if create ==True:
                df = pd.DataFrame.from_dict(item_dict, orient = 'index')
                df = df.transpose()

                Insert_dataframe_2_DB(df, r'C:\Users\as\Sooper\DB\db\PromoFull.db','Promotions')
                create = False

            else:
                sql = 'INSERT INTO Promotions ({}) VALUES ({})'.format(
                    ','.join(item_dict.keys()),
                    ','.join(['?'] * len(item)))
                cur.execute(sql, tuple(item_dict.values()))

            #item_df = pd.DataFrame([item_dict], columns=item_dict.keys())
            #output = pd.concat([output,item_df])


    return output


def TreeItem2Dict(item):
    dict = {}
    for child in item:

        dict[child.tag] =  child.text

    return dict

def print_xml_node_childs(root):
    for child in root:
        print(ET.tostring(child))

    print( )
    print( )


if __name__ == '__main__':
    start_time = time.time()
    df = ParsePromoXml(r'C:\Users\as\Sooper\SeleniumDownload\PromoFull7290027600007-271-202208190300.xml')
    print("--- %s seconds ---" % (time.time() - start_time))
