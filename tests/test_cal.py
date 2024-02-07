from app.calculations import BankAccount


def test_set_ba():
    ba = BankAccount(50)
    assert ba.balance == 50