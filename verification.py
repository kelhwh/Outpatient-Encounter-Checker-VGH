import time

def verify_length_strict(input, expected_len):
    if len(input) != expected_len:
        return print("Input length is expected to be {} but get {}!".format(expected_len, len(input)))
    else:
        return

def verify_date(input):
    try:
        time.strptime(input, "%Y%m%d")
        return
    except:
        return print("Input format not recognizable!")