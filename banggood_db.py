import csv
import json
import mysql.connector


class DATABASE:

    connection = None
    cursor = None

    def __init__(self):
        if Database.connection is None:
                try:
                        Database.connection = mysql.connector.connect(host="127.0.0.1",
                                user="root",
                                password="",
                                database="xtestx")
                        Database.cursor = Database.connection.cursor()
                except Exception as error:
                        print("Error: Connection not established {}".format(error))
        else:
                print("Connection established")

        self.connection = Database.connection
        self.cursor = Database.cursor

    def insert_countries(data: dict):

        connection = mysql.connector.connect(user="root",
                password="",
                host="localhost",
                database="bg")
        cursor = connection.cursor()

        query = ("insert into countries (country_id, country_name) values (%(country_id)s, %(country_name)s)")
        cursor.execute(query, data)
        connection.commit()

        cursor.close()
        connection.close()

    def insert_categories(data: dict):

        connection = mysql.connector.connect(user="root",
                password="",
                host="localhost",
                database="bg")
        cursor = connection.cursor()

        query = ("insert into categories (cat_id, cat_name, parent_id) values (%(cat_id)s, %(cat_name)s, %(parent_id)s)")
        cursor.execute(query, data)
        connection.commit()

        cursor.close()
        connection.close()


    def insert_odoo_attributes(data):
 
        connection = mysql.connector.connect(user="root",
                password="",
                host="localhost",
                database="bg")
        cursor = connection.cursor()        
        # query = ("insert into attributes (value_name, option_list, default_name) values (%(value_name)s, %(option_list)s, %(default_name)s)")
        query = ("insert into attributes (External_ID, Attribute_name, Category, Display_Type, Variants_Creation_Mode, Visibility, Values_External_ID, Values_ID, Values_Value) values (%(External_ID)s, %(Attribute_name)s, %(Category)s, %(Display_Type)s, %(Variants_Creation_Mode)s, %(Visibility)s, %(Values_External_ID)s, %(Values_ID)s, %(Values_Value)s)")
        cursor.execute(query, data)
        connection.commit()

        cursor.close()
        connection.close()


    def delete_odoo_attributes():
 
        connection = mysql.connector.connect(user="root",
                password="",
                host="localhost",
                database="bg")
        cursor = connection.cursor()        
        # query = ("insert into attributes (value_name, option_list, default_name) values (%(value_name)s, %(option_list)s, %(default_name)s)")
        query = ("delete from attributes where id > 0")
        cursor.execute(query)
        connection.commit()

        cursor.close()
        connection.close()


    def insert_odoo_category_id(odoo_cat_id: str, cat_name: str):
 
        connection = mysql.connector.connect(user="root",
                password="",
                host="localhost",
                database="bg")
        cursor = connection.cursor()

        query = ("UPDATE categories SET odoo_category_id = '" + odoo_cat_id + "' WHERE cat_name = '" + cat_name + "'")
        cursor.execute(query)
        connection.commit()

        cursor.close()
        connection.close()           

    def insert_odoo_product_id(odoo_product_id: str, product_id: str):
 
        connection = mysql.connector.connect(user="root",
                password="",
                host="localhost",
                database="bg")
        cursor = connection.cursor()

        query = ("UPDATE products SET odoo_product_id = '" + odoo_product_id + "' WHERE product_id = '" + product_id + "'")
        cursor.execute(query)
        connection.commit()

        cursor.close()
        connection.close()

    def insert_products(data: dict):

        connection = mysql.connector.connect(user="root",
                password="",
                host="localhost",
                database="bg")
        cursor = connection.cursor()

        query = (
                "insert into products (product_id, cat_id, product_name, img, meta_desc, add_date, modify_date, weight, currency, warehouse_list, poa_list, image_list, description, lang, stocks, in_stock) values (%(product_id)s, %(cat_id)s, %(product_name)s, %(img)s, %(meta_desc)s, %(add_date)s, %(modify_date)s, %(weight)s, %(currency)s, %(warehouse_list)s, %(poa_list)s, %(image_list)s, %(description)s, %(lang)s, %(stocks)s, %(in_stock)s)"
                )
        cursor.execute(query, data)
        connection.commit()

        cursor.close()
        connection.close()


    def select_all_attributes():

        connection = mysql.connector.connect(user="root",
                password="",
                host="localhost",
                database="bg")
        cursor = connection.cursor()

        query = (
                # "SELECT Attribute_name FROM attributes WHERE Attribute_name like '%Mode%'"

                "SELECT * FROM attributes"
                )
        cursor.execute(query)
        # connection.commit()

        return cursor.fetchall()

 

    def select_all_attribute_values():

        connection = mysql.connector.connect(user="root",
                password="",
                host="localhost",
                database="bg")
        cursor = connection.cursor()

        query = (
                # "SELECT Attribute_name FROM attributes WHERE Attribute_name like '%Mode%'"

                "SELECT * FROM attributeValues"
                )
        cursor.execute(query)
        # connection.commit()

        return cursor.fetchall()

        

    def select_attributes(Attribute_name, Values_Value):

        connection = mysql.connector.connect(user="root",
                password="",
                host="localhost",
                database="bg")
        cursor = connection.cursor()

        query = (
                # "SELECT Attribute_name FROM attributes WHERE Attribute_name like '%Mode%'"

                "SELECT * FROM attributes WHERE Attribute_name = '" + Attribute_name + "' and Values_Value = '" + Values_Value + "'"
                )
        cursor.execute(query)
        # connection.commit()

        return cursor.fetchall()

        
    def select_categories_where(cat_id):

        connection = mysql.connector.connect(user="root",
                password="",
                host="localhost",
                database="bg")
        cursor = connection.cursor()

        query = (
                "SELECT * FROM categories WHERE cat_id = " + cat_id# '%tools%'"
                )
        cursor.execute(query)
        # connection.commit()

        return cursor.fetchall()
    
    def select_exists(product_id):

        connection = mysql.connector.connect(user="root",
                password="",
                host="localhost",
                database="bg")
        cursor = connection.cursor()
        query = (
                "SELECT EXISTS(SELECT * FROM products WHERE product_id=' " + product_id + "')"
        )
        cursor.execute(query)

        # print(cursor.fetchone())
        exists = cursor.fetchone()
        # print(exists)
        return exists

    def select_odoo_category_id():

        connection = mysql.connector.connect(user="root",
                password="",
                host="localhost",
                database="bg")
        cursor = connection.cursor()
        query = (
                "SELECT * FROM products WHERE odoo_category_id != '' OR odoo_category_id IS NOT NULL"
                )
        cursor.execute(query)
        # connection.commit()
        # print(cursor.fetchone())
        return cursor.fetchall() 


    def select_products_all():

        connection = mysql.connector.connect(user="root",
                password="",
                host="localhost",
                database="bg")
        cursor = connection.cursor()

        query = (
                "SELECT * FROM products"
                )
        cursor.execute(query)
        # connection.commit()

        return cursor.fetchall()

    def select_product_by_id(product_id):

        connection = mysql.connector.connect(user="root",
                password="",
                host="localhost",
                database="bg")
        cursor = connection.cursor()
        query = (
                "SELECT * FROM products WHERE product_id = " + product_id
                )
        cursor.execute(query)
        # connection.commit()
        # print(cursor.fetchone())
        return cursor.fetchall()

    def select_product_category():

        connection = mysql.connector.connect(user="root",
                password="",
                host="localhost",
                database="bg")
        cursor = connection.cursor()
        query = (
                "SELECT cat_id FROM products"
                )
        cursor.execute(query)
        # connection.commit()
        # print(cursor.fetchone())
        cats = cursor.fetchall()
        cats = set(cats)
        catDict = {}
        for cat in cats:
                cursor = connection.cursor()
                query = (
                        "SELECT cat_name FROM categories WHERE cat_id = " + str(cat[0])
                        )
                cursor.execute(query)                # print(cat[0])
                if not cat in catDict.keys():


                        # print(cursor.fetchone()[0])
                        catDict[cat[0]] = [cursor.fetchone()[0]]
                # else:
                #         catDict[cat].append(cursor.fetchone()[0])

        print(catDict)

        csvheader = [
                "Name",
                "Website",
                "Internal Reference",
        ]
        csvdata = []

        # db_select = Database.select_categories_where()
        for k, v in catDict.items():
                print(k)
                l = [v[0]]
                l.append("My Website")
                l.append(k)
                csvdata.append(l)
        
        with open('category_import.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(csvheader)

            # write multiple rows
            writer.writerows(csvdata) 

    def update_product_stock(product_id: str):
        """
        """
        connection = mysql.connector.connect(user="root",
                password="",
                host="localhost",
                database="bg")
        cursor = connection.cursor()               
        query = "UPDATE products SET in_stock = 0 WHERE product_id = " + product_id       
        cursor.execute(query)
        connection.commit()

        return 1
 
    def update_product_by_id(product_id: str, data: dict):
        """
        """
        connection = mysql.connector.connect(user="root",
                password="",
                host="localhost",
                database="bg")
        cursor = connection.cursor()               
        # query = "UPDATE products SET in_stock = 0 WHERE product_id = " + product_id       
        # cursor.execute(query)
        # connection.commit()


        query = (
                "UPDATE products SET warehouse_list = %(warehouse_list)s, poa_list = %(poa_list)s, description = %(description)s, stocks = %(stocks)s, in_stock = %(in_stock)s  WHERE product_id = " + product_id 
                )
        cursor.execute(query, data)
        connection.commit()

        cursor.close()
        connection.close()

        return 1

# Database.select_product_category()  

        # return cursor.fetchall()
  


#   data = {"p1": "1", "p2": "test"}
#   insert(self, data)

# Database.select_exists("1350512")

# with open("rc_stuff_products.csv", "r") as file:
#         csvreader = csv.reader(file)
#         header = next(csvreader)
#         # rows = []
#         for row in csvreader:
#                 Database.insert_odoo_product_id(row[0], row[2])
#                 # rows.append(row)
# print("done")
