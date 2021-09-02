import json
from random import random

def login(i_username, i_password):
    with open('inventory.json', 'r') as inv:
        data = json.load(inv)
        credentials = data['credentials']
        username = credentials['username']
        password = credentials['password']

        if i_username != username or i_password != password:
            return False
        else:
            return True

def admin():
    print("\t"*3 + "-"*5 + "LOGIN" + "-"*5)
    username = input('Enter username: ').strip()
    password = input('Enter password: ').strip()

    if login(username, password):
        print('Logged in sucessfully!')
        admin_panel()
    else:
        print('Please enter correct username & password')
        return admin()

def add_product():
    product_name = input('Enter product name: ').strip()
    quantity = int(input('Enter Quantity available: ').strip())
    category = input('Enter Category: ').strip()
    brand = input('Enter Brand: ').strip()
    price = float(input('Enter price: ').strip())

    if not product_name:
        print('Please fill all the fields correctly ...')
        return add_product()

    product_id = str(int(random() * 10000))
    with open('inventory.json', 'r') as inv:
        data = json.load(inv)
        data['products'][product_id] = {
            "name": product_name,
            "price": price,
            "quantity" : quantity,
            "category" : category,
            "brand" : brand
        }
        with open('inventory.json', 'w') as inv:
            json.dump(data, inv, indent=2, sort_keys=True)
           
    return admin_panel()

def view_product():
    with open('inventory.json','r') as inv:
        data=json.load(inv)
        inv.close()
        for product_id, product in data['products'].items():
            print(f"Product ID: {product_id} ",f": {product['name']}")

def search_product():
    product_name = input('Search product: ').strip()
    with open('inventory.json', 'r') as inv:
        data = json.load(inv)
        for product_id, product in data['products'].items():
            if product['name'].find(product_name) > -1:
                print(f"Product ID: {product_id}")
                print(f"Product Name: {product['name']}")
                print(f"Price: {product['price']}")
                print(f"Available quantity: {product['quantity']}")
                print(f"Category: {product['category']}")
                print(f"Brand: {product['brand']}")
                
                
                print("-"*10)

def update_product():
    product_id = input('Enter product id: ').strip()
    if not product_id:
        print("Please enter a valid id ...")
        return update_product()

    with open('inventory.json', 'r') as inv:
        data = json.load(inv)
        ids = data['products'].keys()
        if product_id not in ids:
            print("Please enter a valid id ...")
            return update_product()

        u_name = input('Enter updated product name: ').strip()
        u_price =input('Enter updated price: ').strip()
        u_quantity = input('Enter updated Quantity: ').strip()
        u_category = input('Enter updated category: ').strip()
        u_brand = input('Enter updated brand: ').strip()
        
#         updated_list=[u_name,u_price, u_quantity, u_category, u_brand]
#         keys=['name','price','quantity','category','brand']
        
        
#         for i,j in zip(updated_list, keys):
#             if not i:
#                 i = data['products'][product_id][j]
        if not u_name:
            u_name = data['products'][product_id]['name']
            
        if not u_price:
            u_price = data['products'][product_id]['price']
        
        if not u_category:
            u_category = data['products'][product_id]['category']

        if not u_brand:
            u_brand = data['products'][product_id]['brand']
            
        if not u_quantity:
            u_quantity = data['products'][product_id]['quantity']

        updated_product = {
            "name": u_name,
            "price": int(u_price),
            "quantity" : int(u_quantity),
            "category" : u_category,
            "brand" : u_brand
        }

        data['products'][product_id] = updated_product

        with open('inventory.json', 'w') as inv:
            json.dump(data, inv,indent=2, sort_keys=True)
            
        return admin_panel()


def delete_product():
    product_id = input('Enter product id: ').strip()
    if not product_id:
        print("Please enter a valid id ...")
        return update_product()

    with open('inventory.json', 'r') as inv:
        data = json.load(inv)
        ids = data['products'].keys()
        if product_id not in ids:
            print("Please enter a valid id ...")
            return update_product()

        data['products'].pop(product_id)

        with open('inventory.json', 'w') as inv:
            json.dump(data, inv,indent=2, sort_keys=True)
            
            
    return admin_panel()

def admin_panel():
    
    print('\t\t----------WELCOME TO INVENTORY----------')
    print('1- Add product')
    print('2- Search product')
    print('3- View Products')
    print('4- Update product')
    print('5- Delete product')
    print('6- Logout')

    option = int(input('Enter option: ').strip())

    if option == 6:
        main()

    if option < 1 or option > 5:
        print('Invalid option')
        input('Press <enter> key to continue ...')
        return menu()

    if option == 1:
        add_product()
    elif option == 2:
        search_product()
    elif option==3:
        view_product()
    elif option == 4:
        update_product()
    else:
        delete_product()

    return admin_panel()


def transaction(pdt_ids) :
        import time
        time.ctime()
        import json
        sales = {}
        report=[]
    
        total=0

        with open('data.json','r') as j_f:
            data=json.load(j_f)
            
            
#         import json
#         a_file = open("records.json", "r")
#         json_object = json.load(a_file)
#         a_file.close()
            
        order={}

            
        for pdt_id in pdt_ids:
            print(f"Selected Product Name: {data['products'][pdt_id]['name']} -",f"Price : {data['products'][pdt_id]['price']}")
            order[pdt_id]=input("Enter the Quantity")
        
        print("\n************Bill***************\n")
        print("Receipt No :")
        print(time.ctime(),'\n')
        for x, y in order.items():
            print(f"{data['products'][x]['name']}  : {data['products'][x]['price']} *",y,"=",int(data['products'][x]['price'])*int(y))
            total+= (int(data['products'][x]['price'])*int(y))
        print("************************************")
        
        for k, v in order.items():
    
            #updating product data in json file
            data ['products'][k]['quantity'] = int(int(data ['products'][k]['quantity']) - int(v))
            j_f = open("data1.json", "w+")
            json.dump(data, j_f)
    #       j_f.close()

            #generating data for sales file    
            report.append( '\n\n'+str(time.ctime())+'\n'+'Product name: '+data['products'][k]['name']+" Qty "+str(data['products'][k]['quantity'])+"\nTotal Amt: "+ str(data['products'][k]['price'])+' '+str(total))
            fdr=open('report.txt','a') 
            for i in report:
                fdr.write(i)
            fdr.close()

            


        print("------------------------------------")
        print("Total =",total,"Rs")
        print("************************************")

        
        with open("sales.json", "w") as outfile:
            json.dump(sales, outfile, indent=1)


def main():
    ui_pid=[]
    print('\n \t\t----------WELCOME TO SHOP-------------\n')
    print('\t What do you Want to buy ')
    view_product()
    print('\n\t\t\t\t\t\t\t\t\t\t\t Enter 0 for admin login ')
    ui_pid = [item for item in input("Enter the Product IDs : ").split()]
    
    with open('inventory.json', 'r') as inv:
        data = json.load(inv)
        ids = data['products'].keys()
        
        if (ui_pid[0]=='0'):
            admin()
        else:
            for i in ui_pid:
                if (i not in ids):
                    print("Invalid Input")
                    main()
                
            
        transaction(ui_pid)


    
if __name__ == "__main__":
    main()