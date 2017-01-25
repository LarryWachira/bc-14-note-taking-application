

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
