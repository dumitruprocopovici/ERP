""" Accounting module

Data table structure:
    * id (string): Unique and random generated identifier
        at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letters)
    * month (number): Month of the transaction
    * day (number): Day of the transaction
    * year (number): Year of the transaction
    * type (string): in = income, out = outflow
    * amount (int): amount of transaction in USD
"""

# everything you'll need is imported:
# User interface module
import ui
# data manager module
import data_manager
# common module
import common


def start_module():
    """
    Starts this module and displays its menu.
     * User can access default special features from here.
     * User can go back to main menu from here.

    Returns:
        None
    """

    table = data_manager.get_table_from_file("accounting/items.csv")
    list_options = ["Show table", "Add new record", "Remove record",
                    "Update record", "Highest profit year", "Average profit in year"]
    while True:
        ui.print_menu("Accounting manager", list_options, "Back to main menu")
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
            ui.print_result(which_year_max(table), "Highest profit year is")
        elif option == "6":
            year = ui.get_inputs(["Please enter year: "], "")
            ui.print_result(avg_amount(table, year[0]), "Averege amount is")
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

    title_list = ["ID", "Month", "Day", "Year", "Type", "Amount"]
    ui.print_table(table, title_list)


def add(table):
    """
    Asks user for input and adds it into the table.

    Args:
        table (list): table to add new record to3

    Returns:
        list: Table with a new record
    """

    list_labels = ["Month: ", "Day: ", "Year: ", "Type: ", "Amount: "]
    new_record = ui.get_inputs(list_labels, 'Add new record')
    new_record.insert(0, common.generate_random(table))
    table.append(new_record)
    data_manager.write_table_to_file("accounting/items_test.csv", table)

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
    data_manager.write_table_to_file("accounting/items.csv", table)

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
                table[id_index] = ui.get_inputs(
                    ["Month: ", "Day: ", "Year: ", "Type: ", "Amount: "], "Please provide the necessary information")
                table[id_index].insert(0, id_[0])
                wrong_id = False
            else:
                id_index += 1
    data_manager.write_table_to_file("accounting/items_test.csv", table)

    return table


# special functions:
# ------------------

def which_year_max(table):
    """
    Question: Which year has the highest profit? (profit = in - out)

    Args:
        table (list): data table to work on

    Returns:
        number
    """

    highest_profit = 0
    yearly_profit = {}
    for line in table:
        if line[3] not in yearly_profit:
            if line[4] == "in":
                yearly_profit[line[3]] = int(line[5])
            else:
                yearly_profit[line[3]] = 0-int(line[5])
        else:
            if line[4] == "in":
                yearly_profit[line[3]] += int(line[5])
            else:
                yearly_profit[line[3]] -= int(line[5])
    for line[3] in yearly_profit:
        if yearly_profit[line[3]] > highest_profit:
            highest_profit = yearly_profit[line[3]]

    return int(line[3])


def avg_amount(table, year):
    """
    Question: What is the average (per item) profit in a given year? [(profit)/(items count)]

    Args:
        table (list): data table to work on
        year (number)

    Returns:
        number
    """

    profit = 0
    items_count = 0
    for line in table:
        if int(line[3]) == int(year):
            items_count += 1
            if line[4] == "in":
                profit += int(line[5])
            else:
                profit -= int(line[5])
    if items_count == 0:
        return "There are no records for this year!"

    return profit / items_count
