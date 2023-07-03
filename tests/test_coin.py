import pytest
from brownie import Coin, accounts

@pytest.fixture(scope="module")
def coin_contract(accounts):
    initial_supply = 1000000
    contract = Coin.deploy(initial_supply, {'from': accounts[0]})
    yield contract

def test_name(coin_contract):
    assert coin_contract.name() == "BToken"

def test_symbol(coin_contract):
    assert coin_contract.symbol() == "BDT"

def test_decimals(coin_contract):
    assert coin_contract.decimals() == 18

def test_total_supply(coin_contract):
    initial_supply = 1000000
    assert coin_contract.totalSupply() == initial_supply

def test_balance_of(coin_contract, accounts):
    initial_supply = 1000000
    assert coin_contract.balanceOf(accounts[0]) == initial_supply

def test_transfer(coin_contract, accounts):
    transfer_amount = 1000
    initial_balance_owner = coin_contract.balanceOf(accounts[0])
    initial_balance_recipient = coin_contract.balanceOf(accounts[1])

    coin_contract.transfer(accounts[1], transfer_amount, {'from': accounts[0]})

    assert coin_contract.balanceOf(accounts[0]) == initial_balance_owner - transfer_amount
    assert coin_contract.balanceOf(accounts[1]) == initial_balance_recipient + transfer_amount


def test_spendAllowance(coin_contract, accounts):
    owner = accounts[0]
    spender = accounts[1]
    initial_allowance = coin_contract.allowance(owner, spender)
    spend_amount = 200
    print("Initial Allowance:", initial_allowance)

    # Approvo un'allowance sufficiente prima di eseguire il trasferimento
    allowance_amount = 1000
    coin_contract.approve(spender, allowance_amount, {'from': owner})

    # Eseguo il trasferimento utilizzando transferFrom
    coin_contract.transferFrom(owner, spender, spend_amount, {'from': spender})

    # Verifico che l'allowance sia stata diminuita correttamente
    assert coin_contract.allowance(owner, spender) == allowance_amount - spend_amount


def test_approve(coin_contract, accounts):
    approval_amount = 1000
    coin_contract.approve(accounts[1], approval_amount, {'from': accounts[0]})
    assert coin_contract.allowance(accounts[0], accounts[1]) == approval_amount

def test_transfer_from(coin_contract, accounts):
    transfer_amount = 500
    initial_balance = coin_contract.balanceOf(accounts[0])
    coin_contract.approve(accounts[1], transfer_amount, {'from': accounts[0]})
    coin_contract.transferFrom(accounts[0], accounts[2], transfer_amount, {'from': accounts[1]})
    assert coin_contract.balanceOf(accounts[0]) == initial_balance - transfer_amount
    assert coin_contract.balanceOf(accounts[2]) == transfer_amount
def test_allowance(coin_contract, accounts):
    owner = accounts[0]
    spender = accounts[1]
    initial_allowance = coin_contract.allowance(owner, spender)

    # Eseguo un'operazione che modifica l'allowance
    approve_amount = 500
    coin_contract.approve(spender, approve_amount, {'from': owner})

    # Verifico che l'allowance sia stata aggiornata correttamente
    assert coin_contract.allowance(owner, spender) == approve_amount

def test_increase_allowance(coin_contract, accounts):
    initial_allowance = coin_contract.allowance(accounts[0], accounts[1])
    increase_amount = 500
    coin_contract.increaseAllowance(accounts[1], increase_amount, {'from': accounts[0]})
    assert coin_contract.allowance(accounts[0], accounts[1]) == initial_allowance + increase_amount

def test_decrease_allowance(coin_contract, accounts):
    initial_allowance = coin_contract.allowance(accounts[0], accounts[1])
    decrease_amount = 500
    coin_contract.decreaseAllowance(accounts[1], decrease_amount, {'from': accounts[0]})
    assert coin_contract.allowance(accounts[0], accounts[1]) == initial_allowance - decrease_amount



def test_mint(coin_contract, accounts):
    mint_amount = 1000
    initial_balance = coin_contract.balanceOf(accounts[0])
    coin_contract.mint(accounts[0], mint_amount, {'from': accounts[0]})
    assert coin_contract.balanceOf(accounts[0]) == initial_balance + mint_amount


def test_burn(coin_contract, accounts):
    burn_amount = 500
    initial_balance = coin_contract.balanceOf(accounts[0])
    coin_contract.burn(burn_amount, {'from': accounts[0]})
    assert coin_contract.balanceOf(accounts[0]) == initial_balance - burn_amount

def test_burn_from(coin_contract, accounts):
    burn_amount = 500
    initial_balance = coin_contract.balanceOf(accounts[0])
    coin_contract.approve(accounts[1], burn_amount, {'from': accounts[0]})
    coin_contract.burnFrom(accounts[0], burn_amount, {'from': accounts[1]})
    assert coin_contract.balanceOf(accounts[0]) == initial_balance - burn_amount