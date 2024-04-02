import tkinter as tk
from tkinter import *
from tkinter import ttk
import threading
import time

from selenium.webdriver.common.by import By
from seleniumbase import Driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import re

driver = None
running = False

event_name_to_data = {}

# Function to update the dropdown with event names
def update_dropdown(event_names):
    dropdown['values'] = event_names

# Function to update the table with line data
def update_table(data):
    table.delete(*table.get_children())
    for row_data in data:
        table.insert('', tk.END, values=row_data)

# Function to handle dropdown selection change
def on_dropdown_change(event):
    selected_event = dropdown.get()
    if selected_event in event_name_to_data:
        update_table(event_name_to_data[selected_event])

def run_script():
    global running, event_name_to_data, driver, isBrowser
    print("Progressing on Login ...")
    # driver = Driver(uc=False)

    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument("--window-size=1920,1080")
    if not isBrowser.get():
        options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    # UserId = "sadikhakan10@gmail.com"
    # UserPass = "123456aA"
    UserId = username_entry.get()
    UserPass = password_entry.get()

    try:
        
        driver.get('https://www.biletalsat.com')
        time.sleep(3)
        try:
            loginButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="header"]/div[3]/div/div[2]/ul/li[1]/a[1]')))
            loginButton.click()
        except:
            driver.find_element(By.XPATH, '//*[@id="header"]/div[3]/div/div[2]/span').click()
            driver.find_element(By.XPATH, '//*[@id="mobile-menu"]/ul/li[5]').click()
        
        time.sleep(2)
        wait = WebDriverWait(driver, 10)
        
        gmail_element = driver.find_element(By.ID, 'email-modal')
        gmail_element.send_keys(UserId)
        password_element = driver.find_element(By.ID, 'pass-modal')
        password_element.send_keys(UserPass)
        driver.find_element(By.XPATH, '//*[@id="loginForm"]/div[2]/button').click()
        time.sleep(2)

        print("Going to ticket page ...")
        try:
            element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="header"]/div[3]/div/div[2]/ul/li[1]/a')))
            element.click()
            element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="header"]/div[3]/div/div[2]/ul/li[1]/ul/li[1]/a')))
            element.click()
        except:
            driver.find_element(By.XPATH, '//*[@id="header"]/div[3]/div/div[2]/span').click()
            element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mobile-menu"]/ul/li[5]')))
            element.click()
            element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mobile-menu"]/ul/li[5]/ul/li[1]/a')))
            element.click()

        print("Extracting data from the page ...")
        print('==================================')
        print('----------------------------------')

        my_lists = driver.find_elements(By.XPATH, '//*[@id="account"]/div[1]/div[3]/div[3]/div')
        for index, my_list in enumerate(my_lists):
            my_list.click()
            time.sleep(2)

        while running:

            event_names = []
            for my_list in my_lists:
                event_name = my_list.find_element(By.TAG_NAME, 'h5').text
                print(event_name)
                print('----------------------------------')
                line_data = []
                lines_elt = my_list.find_elements(By.XPATH, './/div[2]/div/main/div')
                for index, line_elt in enumerate(lines_elt):

                    if not running:
                        driver.quit()
                        return

                    category = ""
                    options_elt = line_elt.find_elements(By.XPATH, './/div[2]/select/option')
                    for option_elt in options_elt:
                        if option_elt.get_attribute("selected"):
                            category = option_elt.text

                    format = ""
                    options_elt = line_elt.find_elements(By.XPATH, './/div[3]/select/option')
                    for option_elt in options_elt:
                        if option_elt.get_attribute("selected"):
                            format = option_elt.text

                    qty = line_elt.find_element(By.XPATH, './/div[4]/input').get_attribute("value")
                    sell = line_elt.find_element(By.XPATH, './/div[5]/input').get_attribute("value")
                    adno = line_elt.find_element(By.XPATH, './/div[7]/input').get_attribute("value")
                    earning = line_elt.find_element(By.XPATH, './/div[9]/input').get_attribute("value")
                    price = line_elt.find_element(By.XPATH, './/div[10]/input').get_attribute("value")

                    if event_name in event_name_to_data and event_name_to_data[event_name] and event_name_to_data[event_name][index][8] != '':
                        sell_prc = WebDriverWait(line_elt, 10).until(EC.element_to_be_clickable((By.XPATH, './/div[10]/input')))
                        sell_prc.click()
                        time.sleep(4)
                        min_price = float(driver.find_element(By.CLASS_NAME, 'min--price').text[:-4])
                        limit_price = round(float(event_name_to_data[event_name][index][8]), 2)
                        my_price_string = driver.find_element(By.CSS_SELECTOR, 'li[class="red"]').text

                        my_price = re.search(r'\d+\.\d+', my_price_string).group()
                        print(my_price)

                        if float(my_price) == min_price:
                            prices_elt = driver.find_elements(By.XPATH, '//*[@id="price-panel"]/div[2]/div[1]/div[1]/div[1]/ul/li/span')
                            prices = [float(re.search(r'\d+\.\d+', price_elt.text).group()) for price_elt in prices_elt]
                            second_price = sorted(prices)[1]
                            if second_price > float(my_price) + 0.02:
                                price = second_price - 0.01
                            else:
                                price = float(my_price)
                        else:
                            price = float(min_price) - 0.01
                        
                        if limit_price > price:
                            price = limit_price

                        price = round(price, 2)
                        real_price = price
                        rate = 0
                        while rate<0.8 and real_price == price  :
                            sell_prc.clear()
                            sell_prc.send_keys(price)
                            time.sleep(0.5)
                            earning = line_elt.find_element(By.XPATH, './/div[9]/input').get_attribute("value")
                            real_price = float(line_elt.find_element(By.XPATH, './/div[10]/input').get_attribute("value"))
                            rate = float(earning)/price
                        price = str(price)
                        
                        driver.find_element(By.XPATH, '//*[@id="price-panel"]/div[1]/div[1]/i').click()
                        time.sleep(1)

                    line = {
                        "category": category,
                        "format": format,
                        "qty": qty,
                        "sell": sell,
                        "adno": adno,
                        "earning": earning,
                        "price": price,
                    }
                    line_data.append(line)
                if event_name not in event_name_to_data or not event_name_to_data[event_name]:
                    line_data_for_event = [('☐', line['category'], line['format'], line['qty'], line['sell'], line['adno'], line['earning'], line['price'], '') for line in line_data]
                else:
                    line_data_for_event = [(event_name_to_data[event_name][k][0], line['category'], line['format'], line['qty'], line['sell'], line['adno'], line['earning'], line['price'], event_name_to_data[event_name][k][8]) for k, line in enumerate(line_data)]
                event_name_to_data[event_name] = line_data_for_event

                print(line_data_for_event)
                print('----------------------------------')

                selected_event = dropdown.get()
                if selected_event in event_name_to_data:
                    update_table(event_name_to_data[selected_event])
                event_names = list(event_name_to_data.keys())
                dropdown['values'] = event_names
                if not selected_event:
                    dropdown.current(0)
                    update_table(event_name_to_data[event_names[0]])
            
    except Exception as error:
        print("An exception occurred:", error)
        pass
    finally:
        driver.quit()

# Function to handle Start button click
def start_script():
    global running
    if not running:
        running = True
        threading.Thread(target=run_script).start()

# Function to handle Stop button click
def stop_script():
    global running
    running = False

root = tk.Tk()
root.title("Ticket Price View")
root.resizable(False, False)

# Arrange login and password fields to top left
username_label = tk.Label(root, text="Username")
username_label.grid(row=0, column=0, sticky='w', padx=20, ipady=10)
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1, sticky='w', padx=5, pady=10)
password_label = tk.Label(root, text="Password")
password_label.grid(row=1, column=0, sticky='w', padx=20, pady=10)
password_entry = tk.Entry(root)
password_entry.grid(row=1, column=1, sticky='w', padx=5, pady=10)

isBrowser = IntVar()
Checkbutton(root, text="Show Browser", variable=isBrowser).grid(row=1, column=17, sticky='w')

# Arrange start/stop button and dropdown to top right
start_button = tk.Button(root, text="Start", command=start_script, width=15, bg="green")
start_button.grid(row=0, column=18, sticky='e', padx=20, pady=10)
stop_button = tk.Button(root, text="Stop", command=stop_script, width=15, bg="red")
stop_button.grid(row=0, column=19, sticky='e', padx=20, pady=10)
dropdown_label = tk.Label(root, text="Select Event")
dropdown_label.grid(row=1, column=18, padx=20, pady=10)
dropdown = ttk.Combobox(root)
dropdown.grid(row=1, column=19, sticky='e', padx=20, pady=10)
dropdown.config(width=30)
dropdown.bind("<<ComboboxSelected>>", on_dropdown_change)

# Arrange table to body
table = ttk.Treeview(root, columns=('', 'category', 'format', 'quantity', 'sell', 'ad_no', 'earning', 'price', 'min_price'), show="headings", height="15")
table.grid(row=2, column=0, columnspan=20, padx=20)
columns = [('', 30), ('category', 100), ('format', 100), ('quantity', 100), ('sell', 100), ('ad_no', 100), ('earning', 100), ('price', 100), ('min_price', 100)]

# vertical_scrollbar = ttk.Scrollbar(root, orient="vertical", command=table.yview)
# vertical_scrollbar.grid(row=2, column=19, sticky='e')
# table.configure(yscrollcommand=vertical_scrollbar.set)

editable_column = len(columns) - 1  # Index of the last column
entry = tk.Entry(root, width=10)
entry.grid(row=3, column=19, sticky='e',padx=20, pady=20)

for col_name, width in columns:
    try:
        table.column(col_name, width=width, anchor=tk.CENTER)
        table.heading(col_name, text=col_name.capitalize())
    except:
        pass

table.bind('<ButtonRelease-1>', lambda event: toggle_checkbox(event, table.identify_row(event.y)))
table.bind("<Double-1>", lambda event: table_edit(event, editable_column))

def table_edit(event, col):
    try:
        item = table.selection()[0]
        current_value = table.set(item, col)
        entry.delete(0, tk.END)
        entry.insert(0, current_value)

        entry.focus()
        entry.bind("<Return>", lambda event: update_cell_value(item, col))
        entry.bind("<FocusOut>", lambda event: update_cell_value(item, col))
    except:
        pass

def update_cell_value(item, col):

    try:
        new_value = entry.get()
        entry.delete(0, tk.END)
        index = table.index(item)
        selected_event = dropdown.get()
        line = list(event_name_to_data[selected_event][index])
        line[8] = new_value
        event_name_to_data[selected_event][index] = tuple(line)
        update_table(event_name_to_data[selected_event])
        entry.unbind("<Return>")
        entry.unbind("<FocusOut>")
    except:
        pass

def toggle_checkbox(event, item):
    index = table.index(item)
    y = table.identify_column(event.x)
    col_name = table.heading(y, "text")
    if col_name.lower() == columns[0][0]:
        if table.set(item, column='') == '☐':
            table.set(item, column='', value='☑')
            selected_event = dropdown.get()
            if selected_event in event_name_to_data:
                event_data = list(event_name_to_data[selected_event][index])
                event_data[0] = '☑'
                event_name_to_data[selected_event][index] = tuple(event_data)
        else:
            table.set(item, column='', value='☐')
            selected_event = dropdown.get()
            if selected_event in event_name_to_data:
                event_data = list(event_name_to_data[selected_event][index])
                event_data[0] = '☐'
                event_name_to_data[selected_event][index] = tuple(event_data)

def insert_data():
    for i in range(1): 
        table.insert('', 'end', values=(' ', f' ', f' ', f' ', f' ', f' ', f' ', f' ', f' '))

insert_data()
# Start the GUI event loop
root.mainloop()