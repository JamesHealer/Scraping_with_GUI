import tkinter as tk
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
    global running, event_name_to_data, driver

    print("Progressing on Login ...")

    driver = Driver(uc=False)
    driver.maximize_window()

    UserId = "sadikhakan10@gmail.com"
    UserPass = "123456aA"
    # UserId = username_entry.get()
    # UserPass = password_entry.get()

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
            time.sleep(4)

        while running:

            event_list = []
            for index, my_list in enumerate(my_lists):
                event_name = my_list.find_element(By.TAG_NAME, 'h5').text
                print(event_name)
                print('----------------------------------')
                line_data = []
                lines_elt = my_list.find_elements(By.XPATH, './/div[2]/div/main/div')
                for line_elt in lines_elt:
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

                    sell_prc = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, './/div[10]/input')))
                    sell_prc.click()
                    time.sleep(3)
                    prices = []
                    prices_elt = driver.find_elements(By.XPATH, '//*[@id="price-panel"]/div[2]/div[1]/div[1]/div[1]/ul/li/span')
                    for prc in prices_elt:
                        prices.append(float(re.search(r'\d+\.\d+', prc.text).group()))
                    driver.find_element(By.XPATH, '//*[@id="price-panel"]/div[1]/div[1]/i').click()
                    time.sleep(0.3)
                    if len(prices) > 0:
                        min_price = min(prices)
                    else:
                        min_price = price
                    line = {
                        "category": category,
                        "format": format,
                        "qty": qty,
                        "sell": sell,
                        "adno": adno,
                        "earning": earning,
                        "price": price,
                        "min_price": min_price
                    }
                    line_data.append(line)
                event = {
                    "name": event_name,
                    "lines": line_data
                }
                print(event)
                print('----------------------------------')
                event_list.append(event)

            event_names = [event["name"] for event in event_list]
            for event in event_list:
                if event["name"] not in event_name_to_data or not event_name_to_data[event["name"]]:
                    line_data_for_event = [('☐', line['category'], line['format'], line['qty'], line['sell'], line['adno'], line['earning'], line['price'], line['min_price']) for line in event["lines"]]
                    event_name_to_data[event["name"]] = line_data_for_event
                else:
                    line_data_for_event = [(event_name_to_data[event["name"]][k][0], line['category'], line['format'], line['qty'], line['sell'], line['adno'], line['earning'], line['price'], line['min_price']) for k, line in enumerate(event["lines"])]
                    event_name_to_data[event["name"]] = line_data_for_event

            selected_event = dropdown.get()
            if selected_event in event_name_to_data:
                update_table(event_name_to_data[selected_event])
            dropdown['values'] = event_names
            if not selected_event:
                dropdown.current(0)
            
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

# Rest of the Tkinter UI setup code
# ...

# Create the main window
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
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1, sticky='w', padx=5, pady=10)

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
table = ttk.Treeview(root, columns=('', 'category', 'format', 'quantity', 'sell', 'ad_no', 'earning', 'price', 'min_price'), show="headings", height="5")
table.grid(row=2, column=0, columnspan=20, padx=20, pady=20)
columns = [('', 30), ('category', 100), ('format', 100), ('quantity', 100), ('sell', 100), ('ad_no', 100), ('earning', 100), ('price', 100), ('min_price', 100)]

for col_name, width in columns:
    table.column(col_name, width=width, anchor=tk.CENTER)
    table.heading(col_name, text=col_name.capitalize())

table.bind('<ButtonRelease-1>', lambda event: toggle_checkbox(table.identify_row(event.y)))

def toggle_checkbox(item):
    index = table.index(item)
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
        table.insert('', 'end', values=('', f'', f'', f'', f'', f'', f'', f'', f''))

insert_data()
# Start the GUI event loop
root.mainloop()