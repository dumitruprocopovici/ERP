""" Human resources module

Data table structure:
    * id (string): Unique and random generated identifier
        at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letters)
    * name (string)
    * birth_year (number)
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

    # your code

    table = data_manager.get_table_from_file("hr/persons.csv")
    options = ['Show Table', 'Add New Item', 'Remove an Item',
               'Update Data', 'get Oldest Person', 'get Persons Closest to Average']
    title = 'Human Resources:'
    exit_message = 'go to Main Menu'
    while True:
        ui.print_menu(title, options, exit_message)
        inputs = ui.get_inputs(["Please enter a number: "], "")
        option = inputs[0]
        if option == "1":
            show_table(table)
        elif option == "2":
            table = add(table)
        elif option == "3":
            id_ = ui.get_inputs(["Please Enter ID:"], "")
            table = remove(table, id_[0])
        elif option == "4":
            id_ = ''
            update(table, id_)
        elif option == "5":
            get_oldest_person(table)
        elif option == "6":
            get_persons_closest_to_average(table)
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

    headers = ['ID', 'Name', 'Year of Birth']
    ui.print_table(table, headers)


def add(table):
    """
    Asks user for input and adds it into the table.

    Args:
        table (list): table to add new record to

    Returns:
        list: Table with a new record
    """

    # your code

    list_of_inputs = ['Enter a Name:', 'Enter a Year of Birth:']
    title_for_call = 'Introduce Information about User:'
    new_item_info = ui.get_inputs(list_of_inputs, title_for_call)
    new_item = [None, None, None]
    new_item[0] = common.generate_random(table)
    new_item[1] = new_item_info[0]
    new_item[2] = new_item_info[1]
    table.append(new_item)
    data_manager.write_table_to_file("hr/persons.csv", table)
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

    # your code

    for i in table:
        if i[0] == id_:
            table.remove(i)
            break
    data_manager.write_table_to_file("hr/persons.csv", table)
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

    # your code

    wrong_id = True
    while wrong_id:
        id_ = ui.get_inputs(["Please Enter ID:"], "")
        for line in table:
            if line[0] == id_[0]:
                table_update = ui.get_inputs(
                    ['Enter a Name:', 'Enter a Year of Birth:'], "Please provide the necessary information")
                line[1] = table_update[0]
                line[2] = table_update[1]
                wrong_id = False
    data_manager.write_table_to_file("hr/persons.csv", table)

    return table


# special functions:
# ------------------

def get_oldest_person(table):
    """
    Question: Who is the oldest person?

    Args:
        table (list): data table to work on

    Returns:
        list: A list of strings (name or names if there are two more with the same value)
    """

    # your code

    oldest_person = 3000
    for i in table:
        if oldest_person > int(i[2]):
            oldest_person = int(i[2])
    list_of_oldest_persons = []
    for i in table:
        if oldest_person == int(i[2]):
            list_of_oldest_persons.append(i[1])
    if len(list_of_oldest_persons) == 1:
        ui.print_result(list_of_oldest_persons, 'Oldest Person is')
    else:
        ui.print_result(list_of_oldest_persons, 'Oldest Person are')
    return list_of_oldest_persons


def get_persons_closest_to_average(table):
    """
    Question: Who is the closest to the average age?

    Args:
        table (list): data table to work on

    Returns:
        list: list of strings (name or names if there are two more with the same value)
    """

    # your code

    average_year = 0
    count = 0
    for i in table:
        average_year += int(i[2])
        count += 1
    average_year = average_year / count

    closest_to_average = 10000
    for i in table:
        if abs(int(i[2]) - average_year) < abs(closest_to_average - average_year):
            closest_to_average = int(i[2])

    list_of_closest_to_average = []
    for i in table:
        if closest_to_average == int(i[2]):
            list_of_closest_to_average.append(i[1])
    ui.print_result(list_of_closest_to_average, 'Closest to average age')
    return list_of_closest_to_average
