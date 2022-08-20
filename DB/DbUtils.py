import sqlite3


def scrub(table_name):
    return ''.join( chr for chr in table_name if chr.isalnum() )

def createCreateStatement(tableName, columns):
    return f"CREATE TABLE IF NOT EXISTS {scrub(tableName)} ({columns[0]}" + (
            ",{} "*(len(columns)-1)).format(*map(scrub,columns[1:])) + ")"


def createTableFromList(db_path, table_name, colList, colType= None):
    db = sqlite3.connect(db_path)
    cur = db.cursor()
    sql = createCreateStatement(table_name, colList)
    cur.execute(sql)

def fillDictKeys(keys_list, dict):
    dict = {k: dict.get(k, '') for k in keys_list}
    return dict


if __name__ == '__main__':
    db = r'C:\Users\as\Sooper\DB\db\try.db'
    tabName = "Promo"
    colNames = ['ItemCode', 'ItemType', 'IsGiftItem', 'PromotionId', 'AllowMultipleDiscounts', 'PromotionDescription', 'PromotionUpdateDate', 'PromotionStartDate', 'PromotionStartHour', 'PromotionEndDate', 'PromotionEndHour', 'IsWeightedPromo', 'MinQty', 'DiscountType', 'RewardType', 'DiscountRate', 'MinNoOfItemOfered', 'Clubs', 'AdditionalIsCoupon', 'AdditionalGiftCount', 'AdditionalIsTotal', 'AdditionalIsActive']

    dict = {'ItemCode' : 1}

    dict2 = fillDictKeys(colNames, dict)

    x=1


# def createPricesDb(db_path, table_name):
#
# def createPromosDb(db_path, table_name ):

