import csv
from genericpath import exists
import json
from tkinter import W
import mysql.connector
import os
import requests
import sys
import time

from datetime import datetime
from requests.structures import CaseInsensitiveDict

from banggood_gat import *
from banggood_db import *


with open("access_token") as f:
    access_token = f.read()

base_url = "https://api.banggood.com"
params = {"lang": "en"}
params["access_token"] =  access_token

cnx = mysql.connector.connect(
        user="root",
        password="",
        host="localhost",
        database="bg"
)

class BANGGOOD:

    """
    """


    def make_request(self, url: str, params: dict):

        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Connection"] = "close"
        response = requests.get(url, params, headers=headers)
        response = json.loads(response.text)
        # print(response)
        if response["code"] == 21020 or response["code"] == 21030 or response["code"] == 11020:

            print(response)
            GAT.get_access_token()

            with open("access_token") as f:
                access_token = f.read()

            params["access_token"] = access_token
            response = requests.get(url, params, headers=headers)
            response = json.loads(response.text)

            return response

        elif response["code"] == 31020:

            print(response)
            return 0

        return response


    def pagination(self, url: str, page_total: int):

        pages = []
        for page in range(1, page_total + 1):

            params["page"] = page
            response = self.make_request(url, params)
            pages.append(response)

        return pages


    def get_countries(self):

        url = base_url + "/common/getCountries"
        response = self.make_request(url, params)
        print(response)

        for i in response["countries"]:
            print(i)
            data = {
                    "country_id": int(i["country_id"]),
                    "country_name": i["country_name"]
                    }
            Database.insert_countries(data)
        print("get_countrues is done")


    def get_attribute_list(self):
        with open('Product Attribute (product.attribute).csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)

            External_ID = ""
            Attribute_name = ""
            Category = ""
            Display_Type = ""
            Variants_Creation_Mode = ""
            Visibility = ""

            for row in csv_reader:
                # print(csv_reader[0])
                if row[0] == "":
                    # print(row)
                    attribute_data = {
                        "External_ID": External_ID,
                        "Attribute_name": Attribute_name,
                        "Category": Category,
                        "Display_Type": Display_Type,
                        "Variants_Creation_Mode": Variants_Creation_Mode,                        
                        "Visibility": Visibility,
                        "Values_External_ID": row[7],
                        "Values_ID": "1",                        
                        "Values_Value": row[8],
                    }
                    Database.insert_odoo_attributes(attribute_data)

                else:
                    External_ID = row[0]
                    Attribute_name = row[2]
                    Category = row[3]
                    Display_Type = row[4]
                    Variants_Creation_Mode = row[5]
                    Visibility = row[6]
                    attribute_data = {
                        "External_ID": row[0],
                        "Attribute_name": row[2],
                        "Category": row[3],
                        "Display_Type": row[4],
                        "Variants_Creation_Mode": row[5],                        
                        "Visibility": row[6],
                        "Values_External_ID": row[7],
                        "Values_ID": "1",                        
                        "Values_Value": row[8],
                    }
                    Database.insert_odoo_attributes(attribute_data)
        print("get_attribute_list done")

    def get_category_list(self):

        url = base_url + "/category/getCategoryList"
        response = self.make_request(url, params)

        if response["code"] != 0:

            print("get_category_list - Response not 0")
            print(response)

            return 0
        
        page_total = response['page_total']
        categoryList = self.pagination(url, page_total)

        categories = {}
        for i in categoryList:
            print(i)
            for j in i["cat_list"]:

                data = {
                        "cat_id": int(j["cat_id"]),
                        "cat_name": j["cat_name"],
                        "parent_id": int(j["parent_id"])
                        }
                # Database.insert_categories(data)

                categories[j["cat_id"]] = j

        with open("category_list.json", 'w', encoding='utf-8') as f:
            json.dump(categories, f, ensure_ascii=False, indent=4)


    def get_product_list(self):

        url = base_url + "/product/getProductList"
        
        db_select = [["8769"], ["8770"], ["8772"], ["8773"], ["8774"], ["8775"], ["8776"], ["8778"]]

        for i in db_select:

            ts = 172
            params["cat_id"] = i[0]
            response = self.make_request(url, params)

            if response["code"] != 0:

                print("get_product_list - Response not 0")
                print(response)

                return 0
            
            page_total = response["page_total"]
            ts = int(page_total) * ts
            productList = self.pagination(url, page_total)

            with open("products_list_rc_" + str(i[0]) + ".json", "w", encoding="utf-8") as f:
                json.dump(productList, f, ensure_ascii=False, indent=4)

            time.sleep(int(ts) + 172)
       

    def insert_in_db(self):

        rc_cat = ['264', '1751', '1752', '1753', '1813', '1848', '1855', '2007', '2085', '2719', '3993', '8767', '8768', '8769', '8770', '8772', '8773', '8774', '8775', '8776', '8778']

        for root, dirs, files in os.walk("."):
            # print(files)
            break
        print(files)
        for fil in files:
            # print(fil)
            if fil.startswith("products_list_rc_"):

                with open(fil) as json_file:
                    productList = json.load(json_file)
            
                for i in productList:
                    # print(i)
                    if not i["product_list"]:
                        print("not i")
                        break

                    for v in i["product_list"]:

                        exists = Database.select_exists(v["product_id"])

                        if exists[0] == 1:
                            print("exists")
                            pass

                        elif [x for x in rc_cat if x.startswith(str(v["cat_id"]))]:
                            # print(v["product_id"])
                            s = self.get_stocks(v["product_id"])
                            if s == 0:
                                pass

                            else:
                                r = self.get_product_info(v["product_id"])

                                data = {
                                        "product_id": int(v["product_id"]),
                                        "cat_id": int(v["cat_id"]),
                                        "product_name": v["product_name"],
                                        "img": v["img"],
                                        "meta_desc": v["meta_desc"],
                                        "add_date": datetime.strptime(v["add_date"], "%Y-%m-%d %H:%M:%S"),
                                        "modify_date": datetime.strptime(v["modify_date"], "%Y-%m-%d %H:%M:%S"),
                                        "weight": r["weight"],
                                        "currency": r["currency"],
                                        "warehouse_list": json.dumps(r["warehouse_list"]),
                                        "poa_list": json.dumps(r["poa_list"]),
                                        "image_list": json.dumps(r["image_list"]),
                                        "description": replace_all(r["description"]),
                                        "lang": r["lang"],
                                        "stocks": json.dumps(s["stocks"]),
                                        "in_stock": int(s["in_stock"])
                                        }
                                Database.insert_products(data)

                                time.sleep(48)

                        else:
                            print("nsert_in_db - Out of bound cat_id")
                            print(v["cat_id"])

                        # print(v)

        print("insert_in_db - Job done")


    def get_product_info(self, product_id: str):

        url = base_url + "/product/getProductInfo"
        params["product_id"] = product_id

        response = self.make_request(url, params)

        if response["code"] == 41010:

            print("get_product_info - 41010")
            print(response)

        else:

            return response


    def get_stocks(self, product_id: str):

        url = base_url + "/product/getStocks"

        params["product_id"] = product_id
        response = self.make_request(url, params)

        # print(response)
        z = 0
        if response["code"] == 41010:

            print("get_stocks - 41010")

            return 0

        elif response["code"] == 12087:

            print("get_stocks - The product is not on sale")

            return 0

        elif "stocks" not in response.keys():
            response["stocks"] = []
            response["in_stock"] = 0

        else:

            for i in response["stocks"]:

                if "stock_list" in i:

                    for j in i["stock_list"]:

                        if j["stock"] > 0:

                            z+=j["stock"]

        if z == 0:


            response["in_stock"] = 0
            return response

        else:

            response["in_stock"] = z
            return response


    def get_product_update_list(self):

        url = base_url + "/product/getProductUpdateList"
        
        response = self.make_request(url, params)

        if response["code"] == 41010:

            print("get_product_update_list - 41010")

        else:

            page_total = response["page_total"]
            productList = self.pagination(url, params, page_total)

            with open("product_update_list.json", "w", encoding="utf-8") as f:
                json.dump(productList, f, ensure_ascii=False, indent=4)


def get_files():
    """
        Get files in a list current folder
    """

    for root, dirs, files in os.walk("."):
        break

    return files


def replace_all(text, dic={"\"": "'", "\n": "", "\t": " "}):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


# if len(sys.argv) == 1:

#     print("Usage one of the following arguments:\n")
#     print("get_category_list")
#     print("get_product_list")
#     print("insert_in_db")
#     print("get_product_info")
#     print("get_stocks")
#     print("get_product_update_list")
#     print("get_attribute_list")
    
# elif sys.argv[1] == "get_category_list":

#     BANGGOOD().get_category_list()

# elif sys.argv[1] == "get_product_list":

#     BANGGOOD().get_product_list()

# elif sys.argv[1] == "insert_in_db":

#     BANGGOOD().insert_in_db()

# elif sys.argv[1] == "get_stocks":

#     BANGGOOD().get_stocks()

# elif sys.argv[1] == "get_product_update_list":

#     BANGGOOD().get_product_update_list()

# elif sys.argv[1] == "get_attribute_list":

#     BANGGOOD().get_attribute_list()

# elif sys.argv[1] == "get_countries":

#     BANGGOOD().get_countries()

# else:

#     print("Usage one of the following arguments:\n")
#     print("get_category_list")
#     print("get_product_list")
#     print("insert_in_db")
#     print("get_product_info")
#     print("get_stocks")
#     print("get_product_update_list")
#     print("get_attribute_list")

#BANGGOOD().get_category_list()
#BANGGOOD().get_product_list()
#BANGGOOD().insert_in_db()
#BANGGOOD().get_product_info()
#BANGGOOD().get_stocks()
#BANGGOOD().get_product_update_list()
BANGGOOD().get_countries()
