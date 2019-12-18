""" Sales module

Data table structure:
    * id (string): Unique and random generated identifier
        at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letters)
    * title (string): Title of the game sold
    * price (number): The actual sale price in USD
    * month (number): Month of the sale
    * day (number): Day of the sale
    * year (number): Year of the sale
    * customer_id (string): id from the crm
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

    table = data_manager.get_table_from_file("sales/sales.csv")
    list_options = ["Show table", "Add new record", "Remove record",
                    "Update record", "Lowest price item", "Items sold in given time", "Get title by ID",
                    "Get item ID sold last", "Get item title sold last", "Get the sum of prices", "Get customer ID by sale ID",
                    "Get all customers ID", "get all sale ID", "Get number of sales per customer"]
    while True:
        ui.print_menu("Sales manager", list_options, "Back to main menu")
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
            ui.print_result(get_lowest_price_item_id(table),
                            "The id of the item sold for the lowest price is")
        elif option == "6":
            month_from = ui.get_inputs(["Month from: "], "")
            day_from = ui.get_inputs(["Day from: "], "")
            year_from = ui.get_inputs(["Year from: "], "")
            month_to = ui.get_inputs(["Month to: "], "")
            day_to = ui.get_inputs(["Day to: "], "")
            year_to = ui.get_inputs(["Year to: "], "")
            ui.print_result(get_items_sold_between(table, month_from, day_from, year_from, month_to,
                                                   day_to, year_to), "The list with the items sold in the chosen amount of time is")
        elif option == "7":
            id_ = ui.get_inputs(["ID: "], "Please type ID:")
            ui.print_result(get_title_by_id_from_table(
                table, id_), "The title is:")
        elif option == "8":
            ui.print_result(get_item_id_sold_last_from_table(
                table), "The last id item sold is:")

        elif option == "9":
            ui.print_result(get_item_title_sold_last_from_table(
                table), "The last id item sold is:")

        elif option == "10":
            item_idss = [1, 1]
            item_ids = []
            while item_idss[1] == True:
                item_idss = ui.get_inputs(
                    ["ID:", "add another one?:"], "introduce ID")
                item_ids.append(item_idss[0])
            ui.print_result(get_the_sum_of_prices_from_table(
                table, item_ids), "The sum of items is:")
        elif option == "11":
            sale_id = ui.get_inputs(["ID:"], "introduce ID")
            ui.ptint_result(
                get_customer_id_by_sale_id_from_table(table, sale_id), "ID sale is:")
        elif option == "12":
            ui.print_result(get_all_customer_ids_from_table(
                table), "All customer ids is:")
        elif option == "13":
            ui.print_result(
                get_all_sales_ids_for_customer_ids_from_table(table), "All sales IDs is:")
        elif option == "14":
            ui.print_result(
                get_num_of_sales_per_customer_ids_from_table(table), "All sales per customer are:")
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

    title_list = ["ID", "Title", "Price",
                  "Month", "Day", "Year", "Customer ID"]
    ui.print_table(table, title_list)


def add(table):
    """
    Asks user for input and adds it into the table.

    Args:
        table (list): table to add new record to

    Returns:
        list: Table with a new record
    """

    list_labels = ["Title: ", "Price: ", "Month: ",
                   "Day: ", "Year: ", "Customer ID:"]
    new_record = ui.get_inputs(list_labels, 'Add new record')
    new_record.insert(0, common.generate_random(table))
    table.append(new_record)
    data_manager.write_table_to_file("sales/sales.csv", table)

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
    data_manager.write_table_to_file("sales/sales.csv", table)

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
                    ["Title: ", "Price: ", "Month: ", "Day: ", "Year: "], "Please provide the necessary information")
                table[id_index].insert(0, id_[0])
                wrong_id = False
            else:
                id_index += 1
    data_manager.write_table_to_file("sales/sales.csv", table)

    return table


# special functions:
# ------------------

def get_lowest_price_item_id(table):
    """
    Question: What is the id of the item that was sold for the lowest price?
    if there are more than one item at the lowest price, return the last item by alphabetical order of the title

    Args:
        table (list): data table to work on

    Returns:
         string: id
    """

    min_line = table[0]
    for line in table:
        if int(line[2]) < int(min_line[2]):
            min_line = line
        elif int(line[2]) == int(min_line[2]) and line[1] > min_line[1]:
            min_line = line
    return min_line[0]


def get_items_sold_between(table, month_from, day_from, year_from, month_to, day_to, year_to):
    """
    Question: Which items are sold between two given dates? (from_date < sale_date < to_date)

    Args:
        table (list): data table to work on
        month_from (int)
        day_from (int)
        year_from (int)
        month_to (int)
        day_to (int)
        year_to (int)

    Returns:
        list: list of lists (the filtered table)
    """

    for line in table:
        if line[5] < year_from[0] or line[5] > year_to[0]:
            table.remove(line)
        elif line[5] == year_from[0] and line[3] < month_from[0]:
            table.remove(line)
        elif line[5] == year_from[0] and line[3] == month_from[0] and line[4] < day_from[0]:
            table.remove(line)
        elif line[5] == year_to[0] and line[3] > month_to[0]:
            table.remove(line)
        elif line[5] == year_to[0] and line[3] == month_to[0] and line[4] > day_to[0]:
            table.remove(line)

    return table


# functions supports data abalyser
# --------------------------------


def get_title_by_id(id):
    """
    Reads the table with the help of the data_manager module.
    Returns the title (str) of the item with the given id (str) on None om case of non-existing id.

    Args:
        id (str): the id of the item

    Returns:
        str: the title of the item
    """

    return get_title_by_id_from_table(data_manager.get_table_from_file("sales/sales.csv"), id)


def get_title_by_id_from_table(table, id):
    """
    Returns the title (str) of the item with the given id (str) on None om case of non-existing id.

    Args:
        table (list of lists): the sales table
        id (str): the id of the item

    Returns:
        str: the title of the item
    """

    for line in table:
        if id in line:
            return line[1]


def get_item_id_sold_last():
    """
    Reads the table with the help of the data_manager module.
    Returns the _id_ of the item that was sold most recently.

    Returns:
        str: the _id_ of the item that was sold most recently.
    """

    return get_item_id_sold_last_from_table(data_manager.get_table_from_file("sales/sales.csv"))


def get_item_id_sold_last_from_table(table):
    """
    Returns the _id_ of the item that was sold most recently.

    Args:
        table (list of lists): the sales table

    Returns:
        str: the _id_ of the item that was sold most recently.
    """
    answer_ID = None
    answer_date = [0, 0, 0]
    for i in table:
        if int(i[5]) >= answer_date[0]:
            if int(i[3]) >= answer_date[1]:
                if int(i[4]) >= answer_date[2]:
                    answer_date[0] = int(i[5])
                    answer_date[1] = int(i[3])
                    answer_date[2] = int(i[4])
                    answer_ID = i[0]
    return answer_ID


def get_item_title_sold_last_from_table(table):
    """
    Returns the _title_ of the item that was sold most recently.

    Args:
        table (list of lists): the sales table

    Returns:
        str: the _title_ of the item that was sold most recently.
    """

    answer_name = None
    answer_date = [0, 0, 0]
    for i in table:
        if int(i[5]) >= answer_date[0]:
            if int(i[3]) >= answer_date[1]:
                if int(i[4]) >= answer_date[2]:
                    answer_date[0] = int(i[5])
                    answer_date[1] = int(i[3])
                    answer_date[2] = int(i[4])
                    answer_name = i[1]
    return answer_name


def get_the_sum_of_prices(item_ids):
    """
    Reads the table of sales with the help of the data_manager module.
    Returns the sum of the prices of the items in the item_ids.

    Args:
        item_ids (list of str): the ids

    Returns:
        number: the sum of the items' prices
    """

    return get_the_sum_of_prices_from_table(data_manager.get_table_from_file("sales/sales.csv"), item_ids)


def get_the_sum_of_prices_from_table(table, item_ids):
    """
    Returns the sum of the prices of the items in the item_ids.

    Args:
        table (list of lists): the sales table
        item_ids (list of str): the ids

    Returns:
        number: the sum of the items' prices
    """
    summ = 0

    for i in item_ids:
        if item_ids == i[0]:
            summ += i[2]
    return summ


def get_customer_id_by_sale_id(sale_id):
    """
    Reads the sales table with the help of the data_manager module.
    Returns the customer_id that belongs to the given sale_id
    or None if no such sale_id is in the table.

    Args:
         sale_id (str): sale id to search for
    Returns:
         str: customer_id that belongs to the given sale id
    """

    return get_customer_id_by_sale_id_from_table(data_manager.get_table_from_file("sales/sales.csv"), sale_id)


def get_customer_id_by_sale_id_from_table(table, sale_id):
    """
    Returns the customer_id that belongs to the given sale_id
    or None if no such sale_id is in the table.

    Args:
        table: table to remove a record from
        sale_id (str): sale id to search for
    Returns:
        str: customer_id that belongs to the given sale id
    """

    for i in table:
        if sale_id == table[0]:
            return table[6]


def get_all_customer_ids():
    """
    Reads the sales table with the help of the data_manager module.

    Returns:
         set of str: set of customer_ids that are present in the table
    """

    return get_all_customer_ids_from_table(data_manager.get_table_from_file("sales/sales.csv"))


def get_all_customer_ids_from_table(table):
    """
    Returns a set of customer_ids that are present in the table.

    Args:
        table (list of list): the sales table
    Returns:
         set of str: set of customer_ids that are present in the table
    """

    customer_IDs = []
    for i in table:
        customer_IDs.append(i[0])
    return customer_IDs


def get_all_sales_ids_for_customer_ids():
    """
    Reads the customer-sales association table with the help of the data_manager module.
    Returns a dictionary of (customer_id, sale_ids) where:
        customer_id:
        sale_ids (list): all the sales belong to the given customer
    (one customer id belongs to only one tuple)

    Returns:
         (dict of (key, value): (customer_id, (list) sale_ids)) where the sale_ids list contains
            all the sales id belong to the given customer_id
    """

    return get_all_sales_ids_for_customer_ids_from_table(data_manager.get_table_from_file("sales/sales.csv"))


def get_all_sales_ids_for_customer_ids_from_table(table):
    """
    Returns a dictionary of (customer_id, sale_ids) where:
        customer_id:
        sale_ids (list): all the sales belong to the given customer
    (one customer id belongs to only one tuple)
    Args:
        table (list of list): the sales table
    Returns:
         (dict of (key, value): (customer_id, (list) sale_ids)) where the sale_ids list contains
         all the sales id belong to the given customer_id
    """

    customer_IDs_dict = {}
    for i in table:
        if i[0] not in customer_IDs_dict:
            customer_IDs_dict[i[0]] = [i[6]]
        if i[0] in customer_IDs_dict:
            customer_IDs_dict[i[0]].append(i[6])
    return customer_IDs_dict


def get_num_of_sales_per_customer_ids():
    """
     Reads the customer-sales association table with the help of the data_manager module.
     Returns a dictionary of (customer_id, num_of_sales) where:
        customer_id:
        num_of_sales (number): number of sales the customer made
     Returns:
         dict of (key, value): (customer_id (str), num_of_sales (number))
    """

    return get_num_of_sales_per_customer_ids_from_table(data_manager.get_table_from_file("sales/sales.csv"))


def get_num_of_sales_per_customer_ids_from_table(table):
    """
     Returns a dictionary of (customer_id, num_of_sales) where:
        customer_id:
        num_of_sales (number): number of sales the customer made
     Args:
        table (list of list): the sales table
     Returns:
         dict of (key, value): (customer_id (str), num_of_sales (number))
    """

    customer_IDs_dict = {}
    for i in table:
        if i[0] not in customer_IDs_dict:
            customer_IDs_dict[i[0]] = 1
        if i[0] in customer_IDs_dict:
            customer_IDs_dict[i[0]] += 1
    return customer_IDs_dict
