#!/usr/bin/env python
# coding: utf-8

#  #                  Inventory Management System

# ## Features
# 
# * Loads data from a json file
# * Shows the list of products available in inventory to user
# * Can take multiple product inputs at once
# * Displays the bill and Update the inventory
# * Saves the Sales record into a Text file
# * Admin panel with login Feature to Manage inventory
# 

# ###  Run Each cell till the end to Execute Main Program

# In[13]:


#import required libraries

import json
from random import random


# #### Function to verify credentials for admin login

# In[14]:


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


# #### Admin login Function 

# In[15]:


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


# #### Function to View inventory items

# In[29]:


def view_product():
    with open('inventory.json','r') as inv:
        data=json.load(inv)
        inv.close()
        print('Product ID Product Name \t  Category \t\tBrand')
        print("-" *75)
        for product_id, product in data['products'].items():
            print(f"{product_id : <10} ",f"{product['name']: <22}",f"{product['category']: <20}",f"{product['brand']: <15}")


# In[30]:


# Run this to View Products
view_product()


# #### Function to Add a product into inventory

# In[17]:


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


# In[ ]:


# Execute this to test Add product function
add_product()


# #### Function to search a product from inventory

# In[18]:


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


# In[34]:


# Run this to test Search product function
search_product()


# #### Updating an Existing product from inventory

# In[39]:


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
        print('Hit "Enter" to skip updating that value')
        u_name = input('Enter updated product name: ').strip()
        u_price =input('Enter updated price: ').strip()
        u_quantity = input('Enter number added: ').strip()
        u_category = input('Enter updated category: ').strip()
        u_brand = input('Enter updated brand: ').strip()
        

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
            "quantity" : data['products'][product_id]['quantity'] + int(u_quantity),
            "category" : u_category,
            "brand" : u_brand
        }

        data['products'][product_id] = updated_product

        with open('inventory.json', 'w') as inv:
            json.dump(data, inv,indent=2, sort_keys=True)
            
        return admin_panel()


# In[40]:


# Run this to test Update product function
update_product()


# #### Function to Delete a Product from inventory

# In[20]:


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


# #### Admin Panel Function

# In[21]:


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
        return adminpanel()

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


# #### Function to generate bill and update inventory

# In[22]:


def transaction(pdt_ids) :
        import time
        time.ctime()
        
        sales = {}
        report=[]
    
        total=0

        with open('inventory.json','r') as j_f:
            data=json.load(j_f)
            
        
        order={}
        report.append(str(time.ctime())+'\nTransaction ID: '+str(data['transid']))

            
        for pdt_id in pdt_ids:
            print(f"Selected Product Name: {data['products'][pdt_id]['name']} -",f"Price : {data['products'][pdt_id]['price']}",f"\nQuantity Available : {data['products'][pdt_id]['quantity']}")
            order[pdt_id]=input("Enter the Quantity")
        
        print("\n************Bill***************\n")
        print("Receipt No : ",data['transid'])
        print(time.ctime(),'\n')
        for x, y in order.items():
            print(f"{data['products'][x]['name']}  : {data['products'][x]['price']} *",y,"=",int(data['products'][x]['price'])*int(y))
            total += (int(data['products'][x]['price'])*int(y))
            
        print("************************************")
        print("Total =",total,"Rs")
        print("************************************")
        
        
        for k, v in order.items():
    
            #updating product data in json file
            data ['products'][k]['quantity'] = int(int(data ['products'][k]['quantity']) - int(v))
            j_f = open("inventory.json", "w+")
            json.dump(data, j_f, indent=2, sort_keys=True)
            data['transid'] += 1
   

            #generating data for sales file    
            report.append('\nProduct name: '+data['products'][k]['name']+"\tQty sold: "+str(v))
            fdr=open('report.txt','a') 
            
        report.append('\nTotal Amount: ' + str(total) + 'Rs \n\n ')
        for i in report:
            fdr.write(i)
        fdr.close()
            
#     return main()     


# ### Dashboard of program
# 
# User can view list available products.
# 
# Input the product id's of required products
# 
# To enter Admin Panel enter '0'
# 
# Default Credentials: user_id = 'admin'            pass: '12345'

# In[24]:


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


    

main()


# In[ ]:




