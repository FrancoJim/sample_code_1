from sample_1.change_machine import ChangeMachine


def test_minimum_coins():
    # Test case 1: Total amount is $1.23
    with ChangeMachine(1.23) as cm:
        assert (
            cm.minimum_coins()
            == "$1.23 => {'Silver Dollar': '1', 'Half Dollar': '0', 'Quarter': '0', 'Dime': '2', 'Nickel': '0', 'Penny': '3'}"
        )

    # Test case 2: Total amount is $5.75
    with ChangeMachine(5.75) as cm:
        assert (
            cm.minimum_coins()
            == "$5.75 => {'Silver Dollar': '5', 'Half Dollar': '1', 'Quarter': '0', 'Dime': '0', 'Nickel': '0', 'Penny': '0'}"
        )

    # Test case 3: Total amount is $0.99
    with ChangeMachine(0.99) as cm:
        assert (
            cm.minimum_coins()
            == "$0.99 => {'Silver Dollar': '0', 'Half Dollar': '1', 'Quarter': '2', 'Dime': '4', 'Nickel': '0', 'Penny': '4'}"
        )
