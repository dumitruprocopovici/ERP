""" User Interface (UI) module """


def print_table(table, title_list):
    """
    Prints table with data.

    Example:
        /-----------------------------------\
        |   id   |      title     |  type   |
        |--------|----------------|---------|
        |   0    | Counter strike |    fps  |
        |--------|----------------|---------|
        |   1    |       fo       |    fps  |
        \-----------------------------------/

    Args:
        table (list): list of lists - table to display
        title_list (list): list containing table headers

    Returns:
        None: This function doesn't return anything it only prints to console.
    """

    # your goes code

    for i in range(0, len(table)):
        for j in range(0, len(table[0])):
            table[i][j] = str(table[i][j])

    list_with_length = []
    for i in range(0, len(table[0])):
        list_with_length.append(0)
    for i in range(0, len(table)):
        for j in range(0, len(table[0])):
            if len(table[i][j]) > list_with_length[j]:
                list_with_length[j] = len(table[i][j])
    for i in range(len(title_list)):
        if len(title_list[i]) > list_with_length[i]:
            list_with_length[i] = len(title_list[i])

    for i in range(len(list_with_length)):
        list_with_length[i] += 4

    top_border = '     /'
    number_of_dash = 0
    for i in range(len(list_with_length)):
        number_of_dash += list_with_length[i] + 1
    number_of_dash -= 1
    for i in range(number_of_dash):
        top_border += '-'
    top_border += '\\'
    print(top_border)

    center_border = '     |'
    for i in range(number_of_dash):
        center_border += '-'
    center_border += '|'

    temp_string = '     |'
    for i in range(len(title_list)):
        temp_string += title_list[i].center(list_with_length[i])
        temp_string += '|'
    print(temp_string)
    temp_string = '     |'
    print(center_border)

    for i in range(len(table)):
        for j in range(len(table[0])):
            temp_string += table[i][j].center(list_with_length[j])
            temp_string += '|'
        print(temp_string)
        temp_string = '     |'
        if i != len(table) - 1:
            print(center_border)

    down_border = '     \\'
    for i in range(number_of_dash):
        down_border += '-'
    down_border += '/'
    print(down_border)


def print_result(result, label):
    """
    Displays results of the special functions.

    Args:
        result: result of the special function (string, number, list or dict)
        label (str): label of the result

    Returns:
        None: This function doesn't return anything it only prints to console.
    """

    # your code
    print(f'{label}: {result}\n')


def print_menu(title, list_options, exit_message):
    """
    Displays a menu. Sample output:
        Main menu:
            (1) Store manager
            (2) Human resources manager
            (3) Inventory manager
            (4) Accounting manager
            (5) Sales manager
            (6) Customer relationship management (CRM)
            (0) Exit program

    Args:
        title (str): menu title
        list_options (list): list of strings - options that will be shown in menu
        exit_message (str): the last option with (0) (example: "Back to main menu")

    Returns:
        None: This function doesn't return anything it only prints to console.
    """

    # your code
    print(title)
    for idex in range(0, (len(list_options))):
        print(f'    ({idex+1}) {list_options[idex]}')
    print(f'    (0) {exit_message}')


def get_inputs(list_labels, title):
    """
    Gets list of inputs from the user.
    Sample call:
        get_inputs(["Name","Surname","Age"],"Please provide your personal information")
    Sample display:
        Please provide your personal information
        Name <user_input_1>
        Surname <user_input_2>
        Age <user_input_3>

    Args:
        list_labels (list): labels of inputs
        title (string): title of the "input section"

    Returns:
        list: List of data given by the user. Sample return:
            [<user_input_1>, <user_input_2>, <user_input_3>]
    """
    inputs = []

    # your code
    print(title)
    for i in list_labels:
        temp = input(i)
        inputs.append(temp)

    return inputs


def print_error_message(message):
    """
    Displays an error message (example: ``Error: @message``)

    Args:
        message (str): error message to be displayed

    Returns:
        None: This function doesn't return anything it only prints to console.
    """

    # your code
    print("Error: " + message)
