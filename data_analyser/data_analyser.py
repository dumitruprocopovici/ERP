"""
This module creates reports for the marketing department.
This module can run independently from other modules.
Has no own data structure but uses other modules.
Avoid using the database (ie. .csv files) of other modules directly.
Use the functions of the modules instead.
"""

# todo: importing everything you need
import data_manager
# importing everything you need
import ui
import common
from sales import sales
from crm import crm


def start_module():
    """
    Starts this module and displays its menu.
     * User can access default special features from here.
     * User can go back to main menu from here.

    Returns:
        None
    """

    labels_options = ["Show last buyer name", "Show last buyer id", "Show name of who spent the most and how much",
                      "Show id of who spent the most and how much", "Show frequently buyers names", "Show frequently buyers id"]
    while True:
        ui.print_menu("Data analyser", labels_options, "Back to main menu")
        inputs = ui.get_inputs(["Please enter a number: "], "")
        option = inputs[0]
        if option == "1":
            ui.print_result(get_the_last_buyer_name(), "The last buyer is")
        elif option == "2":
            ui.print_result(get_the_last_buyer_id(), "The last buyer id is")
        elif option == "3":
            ui.print_result(get_the_buyer_name_spent_most_and_the_money_spent(
            ), "The one who spent the most is: ")
        elif option == "4":
            ui.print_result(get_the_buyer_id_spent_most_and_the_money_spent(
            ), "The one who spent the most is: ")
        elif option == "5":
            ui.print_result(get_the_most_frequent_buyers_names(
                num=2), "The most frequent buyer name is: ")
        elif option == "6":
            ui.print_result(get_the_most_frequent_buyers_ids(
                num=1), "The most frequent buyer id is: ")
        elif option == "0":
            break
        else:
            ui.print_error_message("Choose something else!")

    pass


def get_the_last_buyer_name():
    """
    Returns the customer _name_ of the customer made sale last.

    Returns:
        str: Customer name of the last buyer
    """
    table = data_manager.get_table_from_file("sales/sales.csv")
    index_of_year = 5
    index_of_day = 4
    index_of_month = 3
    find_the_latest_date = []

    maximum_year = 0
    maximum_month = 0
    table = data_manager.get_table_from_file("sales/sales.csv")

    id_of_customer = ""

    for row in table:
        if int(row[index_of_year]) > maximum_year:
            maximum_year = int(row[index_of_year])
    for row in table:
        if int(row[index_of_year]) == maximum_year:
            if int(row[index_of_month]) > maximum_month:
                maximum_month = int(row[index_of_month])

    for row in table:
        if maximum_year == int(row[index_of_year]) and maximum_month == int(row[index_of_month]):
            find_the_latest_date.append(row[index_of_day])
    maximum_day = int(max(find_the_latest_date))

    for row in table:
        if int(row[index_of_year]) == maximum_year and int(row[index_of_month]) == maximum_month and int(row[index_of_day]) == maximum_day:
            id_of_customer += row[-1]
    crm_table = data_manager.get_table_from_file("crm/customers.csv")

    index_of_id = 0
    index_of_customer_name = 1
    for row in crm_table:
        if row[index_of_id] == id_of_customer:
            return "".join(row[index_of_customer_name])


def get_the_last_buyer_id():
    """
    Returns the customer _id_ of the customer made sale last.

    Returns:
        str: Customer id of the last buyer
    """
    index_of_year = 5
    index_of_day = 4
    index_of_month = 3

    maximum_year = 0
    maximum_month = 0
    maximum_day = 0
    table = data_manager.get_table_from_file("sales/sales.csv")

    id_of_customer = ""

    for row in table:
        if int(row[index_of_year]) >= maximum_year:
            maximum_year = int(row[index_of_year])
            if int(row[index_of_month]) > maximum_month:
                maximum_month = int(row[index_of_month])
                if int(row[index_of_day]) >= maximum_day:
                    maximum_day = int(row[index_of_day])

    for row in table:
        if int(row[index_of_year]) == maximum_year and int(row[index_of_month]) == maximum_month and int(row[index_of_day]) == maximum_day:
            id_of_customer += row[-1]

    return id_of_customer


def get_the_buyer_name_spent_most_and_the_money_spent():
    """
    Returns the customer's _name_ who spent the most in sum and the money (s)he spent.

    Returns:
        tuple: Tuple of customer name and the sum the customer spent eg.: ('Daniele Coach', 42)
    """

    sales_table = data_manager.get_table_from_file("sales/sales.csv")
    csv_table = data_manager.get_table_from_file("crm/customers.csv")

    price_index_in_sales_table = 2
    id_index_in_sales_table = len(sales_table[0])-1

    csv_id_index = 0
    csv_name_index = 1

    id_of_customer = None
    name_of_customer = None

    buyers_id_and_sum_paid = {}

    for row in sales_table:
        if row[id_index_in_sales_table] not in buyers_id_and_sum_paid.keys():
            buyers_id_and_sum_paid[row[id_index_in_sales_table]
                                   ] = row[price_index_in_sales_table]
        else:
            if buyers_id_and_sum_paid[row[id_index_in_sales_table]] < row[price_index_in_sales_table]:
                buyers_id_and_sum_paid[row[id_index_in_sales_table]
                                       ] = row[price_index_in_sales_table]

    maximum_sum_spent = max(buyers_id_and_sum_paid.values())

    for key in buyers_id_and_sum_paid.keys():
        if buyers_id_and_sum_paid[key] == maximum_sum_spent:
            id_of_customer = key

    for row in csv_table:
        if row[csv_id_index] == id_of_customer:
            return (row[csv_name_index], maximum_sum_spent)


def get_the_buyer_id_spent_most_and_the_money_spent():
    """
    Returns the customer's _id_ who spent more in sum and the money (s)he spent.

    Returns:
        tuple: Tuple of customer id and the sum the customer spent eg.: (aH34Jq#&, 42)
    """

    sales_table = data_manager.get_table_from_file("sales/sales.csv")

    price_index_in_sales_table = 2
    id_index_in_sales_table = len(sales_table[0])-1

    csv_id_index = 0
    csv_name_index = 1

    id_of_customer = None
    name_of_customer = None

    buyers_id_and_sum_paid = {}

    for row in sales_table:
        if row[id_index_in_sales_table] not in buyers_id_and_sum_paid.keys():
            buyers_id_and_sum_paid[row[id_index_in_sales_table]
                                   ] = row[price_index_in_sales_table]
        else:
            if buyers_id_and_sum_paid[row[id_index_in_sales_table]] < row[price_index_in_sales_table]:
                buyers_id_and_sum_paid[row[id_index_in_sales_table]
                                       ] = row[price_index_in_sales_table]

    maximum_sum_spent = max(buyers_id_and_sum_paid.values())

    for key in buyers_id_and_sum_paid.keys():
        if buyers_id_and_sum_paid[key] == maximum_sum_spent:
            id_of_customer = key
            return (id_of_customer, maximum_sum_spent)


def get_the_most_frequent_buyers_names(num=1):
    """
    Returns 'num' number of buyers (more precisely: the customer's name) who bought most frequently in an
    ordered list of tuples of customer names and the number of their sales.

    Args:
        num: the number of the customers to return.

    Returns:
        list of tuples: Ordered list of tuples of customer names and num of sales
            The first one bought the most frequent. eg.: [('Genoveva Dingess', 8), ('Missy Stoney', 3)]
    """

    sales_table = data_manager.get_table_from_file("sales/sales.csv")
    csv_table = data_manager.get_table_from_file("crm/customers.csv")

    index_of_id_from_sales_table = len(sales_table[0]) - 1
    index_of_id_from_crm_table = 0
    index_of_name_from_crm_table = 1

    dict_with_buyers = {}

    for row in sales_table:
        if row[index_of_id_from_sales_table] not in dict_with_buyers.keys():
            dict_with_buyers.update(
                {str(row[index_of_id_from_sales_table]): 1})
        else:
            dict_with_buyers[row[index_of_id_from_sales_table]] += 1

    for key in dict_with_buyers.keys():
        for row in csv_table:
            if key == row[index_of_id_from_crm_table]:
                dict_with_buyers[row[index_of_name_from_crm_table]] = dict_with_buyers.pop(
                    row[index_of_id_from_crm_table])

    list_with_tuples = [tuple(x) for x in dict_with_buyers.items()]

    return list_with_tuples[0:num]


def get_the_most_frequent_buyers_ids(num=1):
    """
    Returns 'num' number of buyers (more precisely: the customer ids of them) who bought more frequent in an
    ordered list of tuples of customer id and the number their sales.

    Args:
        num: the number of the customers to return.

    Returns:
        list of tuples: Ordered list of tuples of customer ids and num of sales
            The first one bought the most frequent. eg.: [(aH34Jq#&, 8), (bH34Jq#&, 3)]
    """

    sales_table = data_manager.get_table_from_file("sales/sales.csv")
    csv_table = data_manager.get_table_from_file("crm/customers.csv")

    index_of_id_from_sales_table = len(sales_table[0]) - 1
    index_of_id_from_crm_table = 0
    index_of_name_from_crm_table = 1

    dict_with_buyers = {}

    for row in sales_table:
        if row[index_of_id_from_sales_table] not in dict_with_buyers.keys():
            dict_with_buyers.update(
                {str(row[index_of_id_from_sales_table]): 1})
        else:
            dict_with_buyers[row[index_of_id_from_sales_table]] += 1

    list_with_tuples = [tuple(x) for x in sorted(
        dict_with_buyers.items(), key=lambda x:x[0])]

    return list_with_tuples[num-1]
