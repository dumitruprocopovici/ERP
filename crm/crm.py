""" Customer Relationship Management (CRM) module

Data table structure:
    * id (string): Unique and random generated identifier
        at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letters)
    * name (string)
    * email (string)
    * subscribed (int): Is she/he subscribed to the newsletter? 1/0 = yes/no
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

    list_options = ["Show table", "Add Customer", "Remove Customer", "Update Customer", "Get Longest name id",
                    "Get subscribed e-mails", "Name by ID"]
    exit_message = "Return to Main Menu"
    table = data_manager.get_table_from_file("crm/customers.csv")

    while True:
        ui.print_menu("Customer Relationship Management (CRM)",
                      list_options, "Back to main menu")
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
            ui.print_result(get_longest_name_id(table), "Longest name Id")
        elif option == "6":
            ui.print_result(get_subscribed_emails(table), "Subscribed e-mails")
        elif option == "7":
            id = ui.get_inputs(["ID: "], "Please type ID")
            ui.print_result(get_name_by_id_from_table(table, id[0]), "Name by ID")
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

    title_list = ["ID", "Name", "Mail Address", "Subscribed Member"]
    ui.print_table(table, title_list)


def add(table):
    """
    Asks user for input and adds it into the table.

    Args:
        table (list): table to add new record to

    Returns:
        list: Table with a new record
    """

    table_list = ["Name", "Mail Address", "Subscribed Member"]
    new_record = ui.get_inputs(table_list, 'Add new record')
    new_record.insert(0, common.generate_random(table))
    table.append(new_record)
    data_manager.write_table_to_file("crm/customers.csv", table)
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
    data_manager.write_table_to_file("crm/customers.csv", table)
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
                table[id_index] = ui.get_inputs(["Name", "Mail Address", "Subscribed Member"],
                                                "Please provide the necessary information")
                table[id_index].insert(0, id_[0])
                wrong_id = False
            else:
                id_index += 1
    data_manager.write_table_to_file("crm/customers.csv", table)
    return table


# special functions:
# ------------------

def get_longest_name_id(table):
    """
        Question: What is the id of the customer with the longest name?

        Args:
            table (list): data table to work on

        Returns:
            string: id of the longest name (if there are more than one, return
                the last by alphabetical order of the names)
        """

    longest_name = table[0]
    for i in table:
        if len(i[1]) > len(longest_name[1]):
            longest_name = i
        elif len(i[1]) == len(longest_name[1]) and i[1] > longest_name[1]:
            longest_name = i

    ui.print_result(longest_name[1], 'The Longest Name ID is')
    return longest_name[0]


# the question: Which customers has subscribed to the newsletter?
# return type: list of strings (where string is like email+separator+name, separator=";")
def get_subscribed_emails(table):
    """
        Question: Which customers has subscribed to the newsletter?

        Args:
            table (list): data table to work on

        Returns:
            list: list of strings (where a string is like "email;name")
        """

    temp = ['', '']
    list_of_subscribers = []
    for i in table:
        if int(i[3]) == 1:
            temp[0] = i[2]
            temp[1] = i[1]
            list_of_subscribers.append(temp)
            temp = ['', '']
    return list_of_subscribers


# functions supports data analyser
# --------------------------------


def get_name_by_id(id):
    """
    Reads the table with the help of the data_manager module.
    Returns the name (str) of the customer with the given id (str) on None om case of non-existing id.

    Args:
        id (str): the id of the customer

    Returns:
        str: the name of the customer
    """
    
    return get_name_by_id_from_table(data_manager.get_table_from_file("crm/customers.csv"), id)
    


def get_name_by_id_from_table(table, id):
    """
    Returns the name (str) of the customer with the given id (str) on None om case of non-existing id.

    Args:
        table (list of lists): the customer table
        id (str): the id of the customer

    Returns:
        str: the name of the customer
    """
    
    for line in table:
        if id in line:
            return line[1]
