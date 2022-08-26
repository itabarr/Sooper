import sqlite3


def scrub(table_name):
    return ''.join( chr for chr in table_name if chr.isalnum() )

def create_create_statement(table_name, columns):
    return f"CREATE TABLE IF NOT EXISTS {scrub(table_name)} ({columns[0]}" + (
            ",{} "*(len(columns)-1)).format(*map(scrub,columns[1:])) + ")"

def create_table_from_list(db_path, table_name, col_list, col_type=None):
    db = sqlite3.connect(db_path)
    cur = db.cursor()
    sql = create_create_statement(table_name, col_list)
    cur.execute(sql)

def fill_dict_keys(keys_list, dict):
    dict = {k: dict.get(k, '') for k in keys_list}
    return dict

def get_ordered_columns_names_from_table(db_path, table_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.execute(f'select * from {table_name}')
    col_data = cursor.description
    ordered_col_names = []

    for col in col_data:
        ordered_col_names.append(col[0])

    return ordered_col_names



if __name__ == '__main__':
    DB_PATH = r'C:\Users\as\Sooper\DB\db\try.db'
    TABLE_NAME = "Promo"
    COL_NAMES = ['ItemCode', 'ItemType', 'IsGiftItem', 'PromotionId', 'AllowMultipleDiscounts', 'PromotionDescription', 'PromotionUpdateDate', 'PromotionStartDate', 'PromotionStartHour', 'PromotionEndDate', 'PromotionEndHour', 'IsWeightedPromo', 'MinQty', 'DiscountType', 'RewardType', 'DiscountRate', 'MinNoOfItemOfered', 'Clubs', 'AdditionalIsCoupon', 'AdditionalGiftCount', 'AdditionalIsTotal', 'AdditionalIsActive']

    ordered_col_names = get_ordered_columns_names_from_table(DB_PATH,
                                                             TABLE_NAME)
    print(ordered_col_names)
    print("done.")

