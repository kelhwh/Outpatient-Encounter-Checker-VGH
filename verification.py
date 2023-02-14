import time

def verify_length_strict(input, expected_len):
    if len(input) == expected_len:
        return True
    else:
        print("Input length is expected to be {} but get {}!".format(expected_len, len(input)))
        return False

def verify_date(input):
    try:
        time.strptime(input, "%Y%m%d")
        return True
    except:
        print("Input format not recognizable!")
        return False
