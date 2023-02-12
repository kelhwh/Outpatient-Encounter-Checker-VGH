
def verified_input(prompt, verification, **kwargs):
    verified = False
    while not verified:
        var = input(prompt)
        verified = verification(var, **kwargs)

    return var

if __name__ == '__main__':
    from verification import verify_date
    OPD_DATE = verified_input("date:", verify_date)
    print(OPD_DATE)