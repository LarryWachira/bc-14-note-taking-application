

def list_to_string(args):
    note_list = args['<note_content>']
    note_content = ' '.join(note_list)
    return note_content

def query_to_string(args):
    query_list = args['<query_string>']
    query_string = ' '.join(query_list)
    return query_string

def num_check(arg):
    num_str = arg['<note_id>']
    try:
        note_id = int(num_str)
        return note_id
    except ValueError:
        print('Please type in an integer value.')
        return

def num_check_limit(arg):
    num_str = arg['<items_per_page>']
    try:
        items_per_page = int(num_str)
        return items_per_page
    except (ValueError, TypeError):
        print('Please type in an integer value.')
        return
