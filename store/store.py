""" Store module

Data table structure:
    * id (string): Unique and random generated identifier
        at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letters)
    * title (string): Title of the game
    * manufacturer (string)
    * price (number): Price in dollars
    * in_stock (number)
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

    table = data_manager.get_table_from_file("store/games.csv")
    list_options = ["Show table", "Add new record", "Remove record",
                    "Update record", "Games of each manufacturer", "Average amount of games"]
    while True:
        ui.print_menu("Store manager", list_options, "Back to main menu")
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
            ui.print_result(get_counts_by_manufacturers(table),
                            "Games available of each manufacturer: ")
        elif option == "6":
            manufacturer = ui.get_inputs(["Please enter manufacturer: "], "")
            ui.print_result(get_average_by_manufacturer(
                table, manufacturer), "Averege amount of games")
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

    title_list = ["ID", "Title", "Manufacturer", "Price", "In_stock"]
    ui.print_table(table, title_list)


def add(table):
    """
    Asks user for input and adds it into the table.

    Args:
        table (list): table to add new record to

    Returns:
        list: Table with a new record
    """

    list_labels = ["Title: ", "Manufacturer: ", "Price: ", "In_stock: "]
    new_record = ui.get_inputs(list_labels, 'Add new record')
    new_record.insert(0, common.generate_random(table))
    table.append(new_record)
    data_manager.write_table_to_file("store/games.csv", table)

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
    data_manager.write_table_to_file("store/games.csv", table)

    return table


def update(table, id_):
    """
    Updates specified record in the table. Ask users for new data.

    Args:
        table: list in which record should be updated
        id_ (str): id of a record to update

    Returns:
        list: table with updated record
    """

    id_index = 0
    wrong_id = True
    while wrong_id:
        for line in table:
            if line[0] == id_[0]:
                table[id_index] = ui.get_inputs(["Title: ", "Manufacturer: ", "Price: ", "In_stock: "
                                                 ], "Please provide the necessary information")
                table[id_index].insert(0, id_[0])
                wrong_id = False
            else:
                id_index += 1
    data_manager.write_table_to_file("store/games.csv", table)

    return table


# special functions:
# ------------------

def get_counts_by_manufacturers(table):
    """
    Question: How many different kinds of game are available of each manufacturer?

    Args:
        table (list): data table to work on

    Returns:
         dict: A dictionary with this structure: { [manufacturer] : [count] }
    """
    manufacturer = []
    count_list = []
    for line in table:
        if line[2] not in manufacturer:
            manufacturer.append(line[2])
    for i in manufacturer:
        count = 0
        for line in table:
            if line[2] == i:
                count += 1
        count_list.append(count)
    return {k: v for k, v in zip(manufacturer, count_list)}


def get_average_by_manufacturer(table, manufacturer):
    """
    Question: What is the average amount of games in stock of a given manufacturer?

    Args:
        table (list): data table to work on
        manufacturer (str): Name of manufacturer

    Returns:
         number
    """

    amount_of_games = 0
    nr_of_manufacturer = 0
    for line in table:
        if line[2] == manufacturer[0]:
            nr_of_manufacturer += 1
            amount_of_games += int(line[4])
    if nr_of_manufacturer == 0:
        return "There is no such manufacturer!"
    else:
        return amount_of_games / nr_of_manufacturer
