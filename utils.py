def error(error_type):
	list_error = {
		'bad_file': 'Bad file'
	}
	print('Error: %s' % list_error[error_type])
	exit(1)
