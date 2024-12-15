"""
Personal Expense Tracker 
Course-End Project

Author: Reuel Gatus
        rgatus@gmail.com
"""

import os    # https://docs.python.org/3/library/filesys.html
import csv   # https://docs.python.org/3/library/csv.html
import sys   # https://docs.python.org/3/library/sys.html
import traceback    # https://docs.python.org/3/library/traceback.html
from datetime import datetime    # https://docs.python.org/3/library/datetime.html


# constants
MONTH_FORMAT = "%Y-%m"
DATE_FORMAT = "%Y-%m-%d"
DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# get the user's home directory
home_dir = os.path.expanduser("~")

# default filename
expense_filename = "AI_ML_CalTech/CB_AI_Projects/Personal_Expense_Tracker/expenses.csv"
budget_filename = "AI_ML_CalTech/CB_AI_Projects/Personal_Expense_Tracker/budget.csv"

# default data storage  
EXPENSE_FILE = os.path.join(home_dir, expense_filename)
BUDGET_FILE = os.path.join(home_dir, budget_filename)

# get current year and month
c_month = datetime.now() 
f_date = c_month.strftime(MONTH_FORMAT)
CURRENT_MONTH_DATE = f_date
CURRENT_MONTH_NAME= c_month.strftime("%B")

# global list 
expense_entries = []
budget_entries = []


# user interface for adding expense(s) 
def add_expenses():

    if not budget_entries:
        
        print(f"Info: No budget allocated for the month of {CURRENT_MONTH_NAME}. Please add month budget.")
        
        # set month budget
        if not set_month_budget():
            return False

        # load save budget information 
        if not load_budget():
            return False

    while True:

        cntr = 0 
        while True:

            t_date = input("Enter the expense date (YYYY-MM-DD): ")
          
            if validate_date(t_date):
                break
                
            print("Please try again.")

            cntr += 1
            if cntr > 3:
                print(f"Max try exceeded, exiting 'Add expenses'")
                return False
               
        cntr = 0 
        while True:

            t_category = input("Enter the category (e.g., FOOD, TRANSPORTATION, UTILITIES, ENTERTAINMENT, MISC): ")
        
            if validate_category(t_category):
                break
                
            print("Please try again.")

            cntr += 1
            if cntr > 3:
                print(f"Max try exceeded, exiting 'Add expenses'")
                return False

        cntr = 0 
        while True:

            t_amount = input("Enter the amount: ")
            
            if validate_amount(t_amount):
                t_amount = round(float(t_amount), 2)
                break
                
            print("Please try again.")

            cntr += 1
            if cntr > 3:
                print(f"Max try exceeded, exiting 'Add expenses'")
                return False


        t_description = input("Enter a description (optional): ")

        if t_description == "":
            t_description = "Stuffs"

        
        # add expense to the list
        if not add_expense_entry(t_date, t_category, t_amount, t_description):
            return False

        # if the user wants to add another expense
        more_expenses = input("Do you want to add another expense? (y/n): ").strip().lower()

        if more_expenses != 'y':
            break
    
    return True


# add an expense entry to global list 'expense_entries'
def add_expense_entry(t_date, t_category, t_amount, t_description=""):

    # validate entry arguments
    if not validate_date(t_date):
        print("Invalid date format. Please enter a valid date (YYYY-MM-DD).")
        return False
    
    if not validate_category(t_category):
        print("Invalid category. Please enter a valid category.")
        return False
    
    if not validate_amount(t_amount):
        print("Invalid amount. Please enter a valid amount (greater than 0).")
        return False
    
    # entry timestamp
    entry_date = datetime.now().strftime(DATE_TIME_FORMAT)
    
    # format input values
    u_category = t_category.strip().lower()  # clean up the category input
    f_amount = float(t_amount)  # convert the amount to float

    # format input date 
    c_date = t_date.strip()  # clean up date input
    o_date = datetime.strptime(c_date, "%Y-%m-%d") # convert to datetime object
    f_date = o_date.strftime(DATE_FORMAT)  # formatted date

    # create the expense dictionary
    expense_dict = {
        "Timestamp": entry_date,
        "Transaction Date": f_date,
        "Amount": f_amount,
        "Category": u_category,
        "Description": t_description
    }
    
    # very fist expense entry, add header first
    if len(expense_entries) < 2:

        # no expenses loaded (exists); initialize expense_entries
        # create expense header dictionary and insert in the new 'expense_enries'
        expense_header_dict = {
            "Timestamp": "Timestamp",
            "Transaction Date": "Transaction Date",
            "Amount": "Amount",
            "Category": "Category",
            "Description": "Description"
        }
        
        expense_entries.append(expense_header_dict)
        #expense_entries.insert (0, expense_header_dict)

    # add the expense to the global list
    expense_entries.append(expense_dict)

    #print("Expense added:", expense_dict)
    return True


# validate the date format (example: YYYY-MM-DD)
def validate_date(t_date):

    try:
        datetime.strptime(t_date, DATE_FORMAT)
        return True
  
    except ValueError:
        # invalid date format
        print(f"Error: '{t_date}' is an invalid date. Please use the YYYY-MM-DD format.")
        # traceback.print_exc()
        return False

    except TypeError:
        # input is not a string
        print("Error: Invalid type for date. The date should be a string in YYYY-MM-DD format.")
        # traceback.print_exc()
        return False


# validate the category
def validate_category(t_category):

    valid_categories = ["FOOD", "TRANSPORTATION", "UTILITIES", "ENTERTAINMENT", "MISC"]
           
    t_category_upper = t_category.strip().upper()

    if t_category_upper in valid_categories:
        return True 
    
    else:
        print(f"Error: {t_category} is an invalid category value. Please use one of the following valid categories:")
        print("""
              - FOOD: meals, groceries
              - TRANSPORTATION: gas, bus fare, rideshare
              - UTILITIES: electric, gas
              - ENTERTAINMENT: restaurant, movies, entertainment expenses
              - MISC: anything other than the above categories
            """)
        return False


# validate the amount (must be a positive number)
def validate_amount(t_amount):
    
    try:
        # convert input string to float
        f_amount = float(t_amount)
        
        # ensure the amount is non-negative
        if f_amount < 0:
            print(f"Error: The amount '{t_amount}' cannot be negative.")
            return False
        
        # valid amount value
        return True
        
    except ValueError:
        print(f"Error: The amount '{t_amount}' is an invalid format, expecting a numeric non-negative value .")
        # traceback.print_exc()
        return False


# read expense.csv and populate global list 'expense_entries' 
def load_expenses(file_path=None):

    # default to the global constant EXPENSE_FILE if no path is provided
    file_path = file_path or EXPENSE_FILE

    try:

        if not os.path.exists(file_path):
            print(f"Error: The file '{file_path}' does not exist.")        
            return None
    
        with open(file_path, 'r', newline='') as file:
            expense_reader = csv.reader(file)

            # iterate over the rows
            for row in expense_reader:
                
                # expense entry has atleast 4 columns, 5th column (Description is optional)
                if len(row) >= 4:
                    
                    entry_date = row[0]
                    f_date = row[1]
                    f_amount = row[2]
                    u_category = row[3]

                    try:
                        t_description = row[4]
                    
                    except ValueError:
                        print(f"Invalid row 'row[4]' or empty, skipping this entry.")
                        continue

                # create the expense dictionary
                expense_dict = {
                    "Timestamp": entry_date,
                    "Transaction Date": f_date,
                     "Amount": f_amount,
                     "Category": u_category,
                    "Description": t_description
                }
    
                # add the expense to the global list
                expense_entries.append(expense_dict)
        
        return True
    
    except FileNotFoundError:
        print(f"Error: The file path '{file_path}' could not be found.")
        return None
    
    except PermissionError:
        print(f"Error: You do not have permission to write to '{file_path}'.")
        return None

    except IsADirectoryError:
        print(f"Error: The path '{file_path}' is a directory, not a file.")
        return None

    except Exception as err:
        print(f"Error while reading the '{file_path}' file: {err}")
        # traceback.print_exc()
        return None


# display expenses from global 'expense_entries' list ( of dictionaries )
def view_expenses():

    # check if the 'expense_entries' list is empty
    if not expense_entries:
        print("No expenses to display. The global list 'expense_entries' is empty.")
        return None
    
    headers = expense_entries[0]

    # get column widths 
    column_widths = get_dict_column_widths(expense_entries[1:], headers)

    # print separator line
    def print_separator():
        separator_length = sum(column_widths) + len(column_widths) * 3 - 3  # width + spaces, less 3 char (5th | column separator)
        print("-" * separator_length)

    print("\n")
    print_separator()

    # print the header
    print_aligned_row(headers, column_widths, headers)

    print_separator()

    # get dictionary size using the expense entry header
    expense_dict_size = len(expense_entries[0])
    
    for row in expense_entries[1:]:

        if len(row) == expense_dict_size:
            # print each expense entry, aligned based on the column widths
            print_aligned_row(row, column_widths, headers)

        else:
            print(f"Incomplete expense entry; '{row}' , skipping this entry")

    print_separator()

    return True


# get expense_entries column widths
def get_dict_column_widths(rows, headers):
    column_widths = []
    
    for header in headers:
        
        # find the max width for this column (header + any row values)
        max_width = max(len(str(header)), max(len(str(row.get(header, ''))) for row in rows))
        column_widths.append(max_width)
    
    return column_widths


# print rows with alignment based on column widths
def print_aligned_row(row, column_widths, headers):

    # ensure the row has the correct number of values
    # 'zip()'  https://docs.python.org/3.3/library/functions.html
    # 'str()', 'ljust()'  https://docs.python.org/3/library/stdtypes.html#textseq

    aligned_row = " | ".join(f"{str(row.get(header, '')).ljust(width)}" 
                             for header, width in zip(headers, column_widths))  
    print(aligned_row)


# set month's budget allocation 
def set_month_budget():

    global budget_entries

    cntr = 0
    while True:

        month_budget_date = input("\nEnter month YYYY-MM : ")

        if validate_month_format(month_budget_date):
            break
        else:
            print(f"Invalid month date format {month_budget_date}. Please use YYYY-MM format\n")
            cntr += 1
            if cntr >= 3:
                print(f"Max '{cntr}' date entry try exceeded, exiting 'Add month budget'.")
                return False

    cntr = 0
    while True:

        month_budget_amount = input("\nEnter budget allocation amount : ")

        if validate_amount(month_budget_amount):
            break

        else:    
            print(f"Invalid amount format {month_budget_amount}.\n")
            cntr += 1
            if cntr >= 3:
                print(f"Max '{cntr}' amount entry try exceeded, exiting 'Add month budget'.")
                return False

    # get current year and month
    c_date = datetime.now() 
    o_date = c_date.strftime(MONTH_FORMAT)
    month_name = c_date.strftime("%B")

    month_budget_Description = input("\nEnter budget description (optional) : ")

    if month_budget_Description == "":
        
        month_budget_Description = f"{month_name} budget allocation"


    budget_dict = {
        "Timestamp": c_date,
        "Month": month_name,
        "Date": month_budget_date,
        "Amount": month_budget_amount,
        "Description": month_budget_Description
    }

    # use of 'copy' to avoid potentially/accidentally modifying 'budget_entries' dictionary entry 
    if len(budget_entries) > 1: 

        # set (override) the current budget dictionary entry in the global list
        # skip budget[0] it's the header
        budget_entries[1] = budget_dict.copy()
    
    else:
        
        # initialize 'budget_entries' global list
        if not budget_entries:

            # add new budget entry
            budget_entries.append(budget_dict.copy())
        
    # save budget information to csv file
    save_budget_to_file(BUDGET_FILE)
    print(f"\n*** Budget information is saved in {BUDGET_FILE} file by default ***\n")
    return True


# validate month format YYYY-MM 
def validate_month_format(b_month):
    
    # ensure the input is a string (convert to string if it's not)
    if not isinstance(b_month, str):
        b_month = str(b_month)

    # clean input and check for empty string or None
    c_month = b_month.strip() if b_month else ""

    # check if the cleaned input is empty (after stripping spaces)
    if not c_month:
        print("Error: The month input is empty. Please provide a valid month in YYYY-MM format.")
        return False

    try:
        # parse the date using the expected format
        datetime.strptime(c_month, MONTH_FORMAT)

        # month is valid
        return True

    except ValueError:
        print(f"Error: The month '{b_month}' is invalid. Please use the YYYY-MM format.")
        traceback.print_exc()
        return False
        

# save global list 'budget_entries' to budget.csv file
def save_budget_to_file(file_path=None):

    if not budget_entries:
        print("No budget to save.")
        return None
    
    # default to global BUDGET_FILE if no path is provided
    file_path = file_path or BUDGET_FILE

    try:
        
        # check if the file already exists
        file_exists = os.path.exists(file_path)

        with open(file_path, 'w', newline='') as file:

            # fieldnames from the keys of the first dictionary in expense_entries
            fieldnames = list(budget_entries[0].keys())

            budget_writer = csv.DictWriter(file, fieldnames=fieldnames)

            # add header only if file doesn't 
            if not file_exists:
                budget_writer.writeheader()
            
            # write the expense entries; skip header budget_entries[0]
            budget_writer.writerows(budget_entries)
            print(f"Budget saved to {file_path}")
            
    except FileNotFoundError:
        print(f"Error: The file path '{file_path}' could not be found.")
        return None
    
    except PermissionError:
        print(f"Error: You do not have permission to write to '{file_path}'.")
        return None

    except IsADirectoryError:
        print(f"Error: The path '{file_path}' is a directory, not a file.")
        return None

    except Exception as err:
        print(f"Error while creating/appending the file: {err}")
        traceback.print_exc()
        return None


# user interface to track month's expenses
# month argument expects YYYY-MM format
def track_budget(b_month = None):

    if b_month is not None:

        if not validate_month_format(b_month):

            cntr = 0
            while True:

                #get user input
                b_month = input("\nPlease enter transaction month YYYY-MM : ")
                b_month = b_month.strip()  # clean up date input
                #b_month.strftime(MONTH_FORMAT)
            
                if validate_month_format(b_month):
                    break

                else:
                    print(f"\nInvalid month format {b_month}, please use YYYY-MM.")
                    cntr += 1
                    if cntr >= 3:
                        print(f"Warning: Max retry exceeded, exiting track_budget...")
                        return False 

    else:
    
        b_month = CURRENT_MONTH_DATE
     
    if not budget_entries:
        print(f"Error: No budget allocation for the month of {CURRENT_MONTH_NAME} is defined")
        return False

    try:

        if not view_running_month_expenses(b_month):
            # handle expected valication return 'False' explicitly
            return False

    except ValueError:
        print(f"Error: The month '{b_month}' is invalid. Please use the YYYY-MM format.")
        traceback.print_exc()
        return False
        
    return True


# display month running expenses from global 'expense_entries' list ( of dictionaries )
def view_running_month_expenses(t_month):

    # check if the 'expense_entries' list is empty
    if not expense_entries:
        print("No expenses to display. The global list 'expense_entries' is empty.")
        return False

    if not validate_month_format(t_month):
        return False
    
    # format input date for consistency
    c_month = t_month.strip()  # clean up date input
    o_date = datetime.strptime(c_month, MONTH_FORMAT) # convert to datetime object
    f_date = o_date.strftime(MONTH_FORMAT)  # formatted date
    month_name = o_date.strftime("%B") 

    # get dictionary size using the expense entry header
    expense_dict_size = len(expense_entries[0])
    
    running_month_expenses =  0.0           
    transaction_count = 0

    for row in expense_entries[1:]:
          
        if len(row) == expense_dict_size:

            if f_date in row["Transaction Date"]:
                transaction_count += 1 
                running_month_expenses += round(float(row["Amount"]), 2)
        else:
            print(f"Incomplete expense entry; '{row}' ")

    # note 'budget_entries[0]' is the header, skip
    # and 'budget_entries[1]' is a string, convert it to float 
    if not budget_entries:
        print(f"Budget is not loaded, please load month's budget first")
        return False
    
    month_budget_allocation = float(budget_entries[1]["Amount"])

    print(f"\n{'-' * 40}")
    print(f"\n   Expenses for the month of {month_name}")
    print(f"\n{'-' * 40}")
    print(f"\nRunning total: ${running_month_expenses}")
    print(f"Total number of transactions: {transaction_count}")
    print(f"This month's budget allocation: ${month_budget_allocation} \n")
    if running_month_expenses <= month_budget_allocation:
        print(f"You have ${month_budget_allocation - running_month_expenses} left for this month.\n") 
        print(f" {'-' * 40}\n")

    elif running_month_expenses > month_budget_allocation:
        print(f"You have exceeded your month of {month_name} budget by ${month_budget_allocation - running_month_expenses}.\n") 
        print(f" {'-' * 40}\n")

    return running_month_expenses


# read budget.csv and populate global list 'expense_entries' 
def load_budget(file_path=None):

    global budget_entries

    # clear stale entries

    budget_entries = []

    # default to the global constant EXPENSE_FILE if no path is provided
    file_path = file_path or BUDGET_FILE

    try:

        if not os.path.exists(file_path):
            print(f"Error: The file '{file_path}' does not exist.")        
            return False
    
        with open(file_path, 'r', newline='') as file:
            budget_reader = csv.reader(file)

            # iterate over the rows
            for row in budget_reader:
                
                # budget entry has atleast 4 columns, 5th column (Description is optional)
                if len(row) >= 4:
                    
                    entry_date = row[0]
                    b_month_name = row[1]
                    b_date = row[2]
                    b_amount = row[3]

                    try:
                        b_description = row[4]
                    
                    except ValueError:
                        print(f"Invalid row 'row[4]' or empty, skipping this entry.")
                        continue

                # create the expense dictionary
                budget_dict = {
                    "Timestamp": entry_date,
                    "Month": b_month_name,
                     "Date": b_date,
                     "Amount": b_amount,
                    "Description": b_description
                }
    
                # add the expense to the global list
                budget_entries.append(budget_dict)
        
        return True
    
    except FileNotFoundError:
        print(f"Error: The file path '{file_path}' could not be found.")
        return False
    
    except PermissionError:
        print(f"Error: You do not have permission to write to '{file_path}'.")
        return False

    except IsADirectoryError:
        print(f"Error: The path '{file_path}' is a directory, not a file.")
        return False

    except Exception as err:
        print(f"Error while reading the '{file_path}' file: {err}")
        traceback.print_exc()
        return False


# user interface to save expenses from global list 'expense_entries' to expenses.csv file
def save_expenses():
    
    # user is done adding expense, save the expenses to a file
    save_request = input("Do you want to save all expenses to a file? (y/n): ").strip().lower()

    if save_request == 'y':
    
        file_path = input("Enter the file path to save the expenses (default is ~/expenses.csv): ")

        # first row is the header
        if len(expense_entries) < 2:

        # no expenses loaded (exists); initialize expense_entries
        # create expense header dictionary and insert in the new 'expense_enries'
            expense_header_dict = {
                "Timestamp": "Timestamp",
                "Transaction Date": "Transaction Date",
                "Amount": "Amount",
                "Category": "Category",
                "Description": "Description"
            }

            expense_entries.insert (0, expense_header_dict)

        # save to CSV file
        save_expenses_to_file(file_path)
    
    else:
        print("Expenses were not saved.")

    return None


# save expenses in global list 'expense_entries' to expenses.csv file
def save_expenses_to_file(file_path=None):

    if not expense_entries:
        print("No expenses to save.")
        return

    # default to global EXPENSE_FILE if no path is provided
    file_path = file_path or EXPENSE_FILE

    try:
        # pen the file in write mode ('w') to overwrite existing content
        with open(file_path, 'w', newline='') as file:
            # derive fieldnames from the first dictionary in expense_entries
            fieldnames = list(expense_entries[0].keys())
            
            # create a CSV DictWriter
            expense_writer = csv.DictWriter(file, fieldnames=fieldnames)

            # check if the first entry in 'expense_entries' already has a header
            # assume that if the first entry is a dictionary with keys matching the fieldnames,
            # it's the header (since fieldnames are extracted from the first dictionary).
            if isinstance(expense_entries[0], dict):

                # only write the header if the first row in expense_entries isn't already the header
                if list(expense_entries[0].keys()) != fieldnames:
                    expense_writer.writeheader()

            # write the expense entries
            expense_writer.writerows(expense_entries)
            print(f"Expenses saved to {file_path} successfully.")

    except FileNotFoundError:
        print(f"Error: The file path '{file_path}' could not be found.")
        return None
    
    except PermissionError:
        print(f"Error: You do not have permission to write to '{file_path}'.")
        return None

    except IsADirectoryError:
        print(f"Error: The path '{file_path}' is a directory, not a file.")
        return None

    except Exception as err:
        print(f"Error while creating/writing the '{file_path}' file: {err}")
        traceback.print_exc()
        return None


# user interface
# make sure to load expenses.csv, run load_expenses to initialize global list of dictionary expense_entries
# make sure to load budget.csv, run load_budget to initialize global list of dictionary budget_entries
def menu():
    while True:
        # print the menu options
        print("\n\n--- Expense Tracker Menu ---\n")
        print("1. Add expense")
        print("2. View expenses")
        print("3. Track budget")
        print("4. Save expenses")
        print("5. Exit (x or X)")

        # get user input
        choice = input("Please select an option (1-5): ")

        # Process user input
        if choice == '1':
            if not add_expenses():  # add an expense
                print("\nWarning: Failed to Add expenses, exiting...")

        elif choice == '2':
    #        view_expenses()  # view expenses
            if not view_expenses():  # view expenses
                print("\nWarning: Failed to View expenses...")

        elif choice == '3':
            # track_budget()  # track budget
            if not track_budget():  # track budget
                print("\nWarning: Failed to Track budget...")

        elif choice == '4':
            if not save_expenses():  # save expenses
                print("\nWarning: Failed to Save expenses...")
                
        elif choice == '5' or choice == 'x' or choice == 'X':
            print("\nExiting the program. Goodbye!\n\n")
            break  # Exit the loop and end the program
        else:
            print("\nInvalid option. Please choose a number between 1 and 5.\n")

        #clear_screen()

# Main
if __name__ == "__main__":

    load_expenses()
    load_budget()

    menu()

