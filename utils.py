def error(error_type):
    list_error = {
        'bad_file': 'Bad file',
        'bad_number_children': '"Number of children should be at least 1"'
    }
    print('Error: %s' % list_error[error_type])
    exit(1)
