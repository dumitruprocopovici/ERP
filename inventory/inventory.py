""" Inventory module

Data table structure:
    * id (string): Unique and random generated identifier
        at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letters)
    * name (string): Name of item
    * manufacturer (string)
    * purchase_year (number): Year of purchase
    * durability (number): Years it can be used
"""

# everything you'll need is imported:
# User interface module
import ui
# # data manager module
import data_manager
# # common module
import common


def start_module():
    """
    Starts this module and displays its menu.
     * User can access default special features from here.
     * User can go back to main menu from here.

    Returns:
        None
    """

    # your code
    list_options = ["Show table", "Add new record", "Remove record", "Update record", "See available items", "See average availability for each manufacturer"]
    table = data_manager.get_table_from_file("inventory/inventory.csv")
    
    while True:
        ui.print_menu("Inventory manager", list_options, "Back to main menu")
        inputs = ui.get_inputs(["Please enter a number: "], "")
        option = inputs[0]
        if option == "1":
            show_table(table)
        elif option == "2":
            add(table)
        elif option == "3":
            id_ = ui.get_inputs(["ID: "], "Please type ID to remove")
            table = remove(table, id_)
        elif option == "4":
            id_ = ui.get_inputs(["ID: "], "Please type ID to update")
            table = update(table, id_)
        elif option == "5":
            year = ui.get_inputs(["Year: "], "Please enter year: ")
            ui.print_result(get_available_items(table, year, ), "Available items are")
        elif option == "6":
            ui.print_result(get_average_durability_by_manufacturers(table), "Averege amount is: ")
        elif option == "0":
            break
        else:
            ui.print_error_message("Choose something else!")
    


def show_table(table):
    """
    Display a table

    Args:
        table (list): list of lists to be displayed.

    Returns:
        None
    """
    # your code
    table = data_manager.get_table_from_file("inventory/inventory.csv")
    title_list = ["ID", "Name", "Manufacturer", "Year of purchase", "Years it can be used"]
    ui.print_table(table,title_list)


def add(table):
    """
    Asks user for input and adds it into the table.

    Args:
        table (list): table to add new record to

    Returns:
        list: Table with a new record
    """

    list_labels = ["Name: ", "Manufacturer: ", "Year of purchase: ", "Durability: "]
    new_record = ui.get_inputs(list_labels, 'Add new record')
    new_record.insert(0, common.generate_random(table))
    table.append(new_record)
    data_manager.write_table_to_file("inventory/inventory.csv", table)

    return table


def remove(table, id_):
    """
    Remove a record with a given id from the table.

    Args:
        table (list): table to remove a record from
        id_ (str): id of a record to be removed

    Returns:
        list: Table without specified record.
    """

    for line in table:
        if line[0] == id_[0]:
            table.remove(line)
    data_manager.write_table_to_file("inventory/inventory.csv", table)

    return table


def update(table, id_):
    """
    Updates specified record in the table. Ask users for new data.

    Args:
        table (list): list in which record should be updated
        id_ (str): id of a record to update

    Returns:
        list: table with updated record
    """

    id_index = 0
    wrong_id = True
    while wrong_id:
        for line in table:
            if line[0] == id_[0]:
                table[id_index] = ui.get_inputs(["Name: ", "Manufacturer: ", "Year of purchase: ", "Durability: "], "Please provide the necessary information")
                table[id_index].insert(0, id_[0])
                wrong_id = False
            else:
                id_index += 1
    data_manager.write_table_to_file("inventory/inventory.csv", table)

    return table


# special functions:
# ------------------

def get_available_items(table, year):
    """
    Question: Which items have not exceeded their durability yet (in a given year)?

    Args:
        table (list): data table to work on
        year (number)

    Returns:
        list: list of lists (the inner list contains the whole row with their actual data types)
    """
    available_items = []
    table = data_manager.get_table_from_file("inventory/inventory.csv")
    release_i = 3
    durability_i = 4
    for i in table:
        if int(year[0]) - int(i[release_i]) <= int(i[durability_i]):
            available_items.append(i)
        
    return available_items if (int(year[0])  - int(i[release_i])) >= 0 else ui.print_error_message("There are no available items for this year")
        
    


def get_average_durability_by_manufacturers(table):
    """
    Question: What are the average durability times for each manufacturer?

    Args:
        table (list): data table to work on

    Returns:
        dict: a dictionary with this structure: { [manufacturer] : [avg] }
    """

    table = data_manager.get_table_from_file("inventory/inventory.csv")

    manufacturer_i = 2
    durability_i = 4

    sony_average = 0
    nintendo_average = 0
    microsoft_average = 0

    sony_in_table = 0
    nintendo_in_table = 0
    microsoft_in_table = 0
    
    for i in table:
        if i[manufacturer_i] == "Sony":
            sony_in_table += i.count("Sony")
            sony_average += int(i[durability_i])
        if i[manufacturer_i] == "Microsoft":
            microsoft_average += int(i[durability_i])
            microsoft_in_table += i.count("Microsoft")
        if i[manufacturer_i] == "Nintendo":
            nintendo_in_table += i.count("Nintendo")    
            nintendo_average += int(i[durability_i])

    sony_average = sony_average / sony_in_table
    microsoft_average = microsoft_average / microsoft_in_table
    nintendo_average = nintendo_average / nintendo_in_table

    average = {"Sony":sony_average, "Nintendo":nintendo_average, "Microsoft":microsoft_average}

    return average


