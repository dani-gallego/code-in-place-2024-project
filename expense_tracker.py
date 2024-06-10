import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import csv



RECORD_SUMMARY_DATA = []
BUDGET = 0.0


def main():
    global BUDGET

    print("Welcome to Expense Tracker!")
    BUDGET = user_budget()
    
    # Main menu for expense tracker
    menu_option()


def menu_option():
    # User will have few options to select in main menu
    print("\nWhat would you like to do? ")
    menu = ["💸 Track your Expenses", "📃 Record Summary", "🔚 Exit"]
    
    # Pick options in the main menu
    while True:
        for num_option, option_name in enumerate(menu):
            print(f"{num_option + 1}) {option_name}")
        
        # Index option ranges from 1 to length of the menu
        index_option = f"[1 - {len(menu)}]"

        # User can select what index will be selected from the menu
        selected_index = input(f'Select the expense category {index_option}: ')

        if selected_index.isdigit():
            selected_index = int(selected_index) - 1
            if selected_index in range(len(menu)):
                selected_options = menu[selected_index]
                print(f"You've chosen option {selected_options}")

                if selected_index == 0:
                    track_expenses_details()
                elif selected_index == 1:
                    record_summary()
                elif selected_index == 2:
                    print("Exiting the program.")
                    exit()
            else:
                print(f"Invalid input. Please enter a correct index.\n")
        else:
            print(f"Invalid input. Please enter a correct index.\n")



def record_summary():
    print("🎯 Record Summary!\n")

    total_spent = 0

    print("Here's the daily record summary")
    if RECORD_SUMMARY_DATA:
        for record in RECORD_SUMMARY_DATA:
            print(f"<Date: {record['date']}, Category: {record['category']}, "
                  f"Expense Name: {record['expense_name']}, Amount: {record['amount']} pesos>")
            total_spent += record["amount"] 

        remaining_budget = BUDGET - total_spent
        print(f"\nRemaining Budget: {remaining_budget} pesos\n")

    else:
        print("No records found!\n")
        return
    
   # Ask if the user wants to save the records to a CSV file
    while True:
        save_expenses_csv = input('Do you want to save your expenses? (yes/no): ')
        if save_expenses_csv.lower() in ('yes', 'y'):
            save_expenses(RECORD_SUMMARY_DATA, "expense.csv")
            print("Saved.")
            display_graph()
            break
        elif save_expenses_csv.lower() in ('no', 'n'):
            print("Not saved.")
            break
        else:
            print('Invalid input. Please enter a correct input: (yes/no)')

def save_expenses(records, filename):
    keys = records[0].keys()
    with open(filename, "a", newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(records)

def track_expenses_details():
    global RECORD_SUMMARY_DATA
    expenses = {}
    while True:
        chosen_category = expense_category()
        if chosen_category == 4:
            print("Going back to main menu")
            menu_option()
        expense_name, expense_amount = expense_tracker(chosen_category)
        if chosen_category not in expenses:
            expenses[chosen_category] = {}
        expenses[chosen_category][expense_name] = expense_amount
        current_date = datetime.now().strftime("%Y-%m-%d")  # Get current date
        RECORD_SUMMARY_DATA.append(
        {"date": current_date,
         "category": chosen_category,
         "expense_name": expense_name,
         "amount": expense_amount}
        )
        total_expense = sum_total(expenses)
        check_budget(BUDGET, total_expense)
        
        # Ask user if they want to continue
        cont = input("\nDo you want to continue? (yes/no): ")
        if cont.lower() in ("no" , "n"):
            display_graph()
            break
        elif cont.lower() in ("yes", "y"):
            print("Let's continue your expenses!")
            continue
        else:
            print("Invalid input. Please enter a correct option.\n")


    
# Enter amount of budget
def user_budget():
    print("\nPlease input your budget for today!")
    user_budget = float(input("Enter the amount of budget: "))
    return user_budget


# Lists of expense category
# Grocery, Transportation, Utility Bills, Parcel/Packages
def expense_category():
    print("\nPlease choose expense category below!")
    expense_category = ["🛒 Grocery", "🚌 Transporation", "⚡ Utility Bills", "📦 Parcel / Packages", "Back to Main Menu"]

    # Pick the expense category
    while True:
        for i, category_name in enumerate(expense_category):
            print(f"{i + 1}) {category_name}")
        
        # Index category ranges from 1 to length of the expense_category
        index_category = f"[1 - {len(expense_category)}]"

        # User can select what index will be selected from the category
        chosen_index = input(f'Select the expense category {index_category}: ')

        if chosen_index.isdigit():
            chosen_index = int(chosen_index) - 1
            if chosen_index in range(len(expense_category)):
                chosen_category = expense_category[chosen_index]
                print(f"You've chosen category {chosen_category}")
                if chosen_index == 4:
                    menu_option()
                return chosen_category
            else:
                print(f"Invalid input. Please enter a correct index.\n")
        
        

# Track your expense
def expense_tracker(chosen_category):
    print("\nLet's see your expenses so far")
    expense_name = input("Enter the expense name: ")
    # Enter the amount spent
    expense_amount = float(input('Enter the amount spent: '))
    print(f"Expense name: {expense_name}, Amount: {expense_amount} pesos")
    return expense_name, expense_amount


# Calculation of the total sum of amount spent
def sum_total(expenses):
    total = 0
    for category in expenses.values():
        total += sum(category.values())
    print(f"\nTotal amount spent so far: {total} pesos")
    return total


# Display the budget and see it's overbudget or underbudget
def check_budget(BUDGET, total_expense):
    if total_expense > BUDGET:
        print(f"You have -{total_expense - BUDGET} pesos in your account!")
    else:
        print(f"Here's your remaining balance in your budget {BUDGET - total_expense} pesos")


# Display the graph of expense category with it's total amount by category
def display_graph(expenses):
    categories = list(expenses.keys())
    amounts = [sum(category.values()) for category in expenses.values()]
    # Create a random color for the bar graph
    colors = (np.random.random(), np.random.random(), np.random.random())
    plt.bar(categories, amounts, color = colors)
    plt.xlabel('Expense Category')
    plt.ylabel('Amount in Pesos')
    plt.title('Expenses by Category')
    plt.show()

if __name__ == "__main__":
    main()