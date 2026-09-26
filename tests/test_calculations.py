from app.calculations import add, divide, multiply, subtract,BankAccount
import pytest

# @pytest.mark.parametrize("num1, num2, expected", [
#     (2, 3, 5),
#     (5, 3, 2),
#     (2, 3, 6)
# ])
# def test_add(num1, num2, expected):
#     print("Testing add function")
#     assert add(num1, num2) == expected                  


# def test_subtract():
#     print("Testing subtract function")
#     assert subtract(5, 3) == 2

# def test_multiply():
#     print("Testing multiply function")
#     assert multiply(2, 3) == 6

# def test_divide():
#     print("Testing divide function")
#     assert divide(6, 3) == 2

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

def test_bank_default_amt(zero_bank_account):
    assert zero_bank_account.balance==0

def test_bank_set_initial_amt(bank_account):
    assert bank_account.balance==50

def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance==30

def test_deposit(bank_account):
    bank_account.deposit(30)
    assert bank_account.balance==80

@pytest.mark.parametrize("deposited,withdrew,expected",[(200,100,100),(150,10,140),(1200,200,1000)])
def test_bank_transaction(zero_bank_account,deposited,withdrew,expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance==expected