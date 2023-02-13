
def verified_input(prompt, verification, **kwargs):
    verified = False
    while not verified:
        var = input(prompt)
        verified = verification(var, **kwargs)

    return var
def exit_prompt(message=None):
    print(message)
    input("Press ENTER to leave.")
    exit()

def restart_prompt(run_fun, message=None):
    print(message)
    input("Press ENTER to restart.")
    run_fun()


if __name__ == '__main__':
    from verification import verify_date
    OPD_DATE = verified_input("date:", verify_date)
    print(OPD_DATE)