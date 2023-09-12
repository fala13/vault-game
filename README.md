# Hats Challenge #2 solution
## Issue
ERC4226ETH.sol implementation suffers from re-entrancy issue in line 162.
In line 158 amount of ETH above token total supply is computed to be sent back to vault owner later in line 164.
If there is such excess ETH and re-entrance occurs in line 162 more ETH will be sent to vault owner than intended.
If other users would keep ETH in the vault, they might loose funds as the amount of ETH in contract would be lower than sum of balances.

## Fix proposals:
- Move content of line 158 and 163-165, that is withdrawing excess ETH, to a separate function (separation of concerns).
- Move content of line 158 after content of line 162 to avoid this interaction.
- Use nonReentrant modifier on withdraw().

## PoC outline:
- Deploy example Vault.
- Deploy bomb contract which will self-destruct to forcibly send 1 ETH to Vault contract. Since the Vault contract does not have receive() or fallback() functions this is the only way to cause difference in contract ETH balance and _totalSupply counter.
- Call withdraw() from a custom contract which triggers re-entrancy one single time. This causes value of 1 excess ETH to be transferred two times to vault owner leaving the vault empty. Interestingly no deposit needs to be made by the attacker and the re-entrancy can be caused by withdrawing 0 wei.

## Example calltrace of attack:
```
Initial call cost  [21432 gas]
Exploit.attack  0:2000  [22618 / 371170079 gas]
├── Vault.withdraw  [CALL]  55:1834  [29491326 / 341702001 gas]
│   └── ERC4626ETH.withdraw  194:1754  [28974572 / 312210675 gas]
│       └── ERC4626ETH._withdraw  226:1675  [2473 / 283236103 gas]
│           ├── ERC20._burn  278:397  [-12400 gas]
│           └── Exploit  [CALL]  433:1647  [143243586 / 283246030 gas]
│               └── Vault.withdraw  [STATICCALL]  860:1634  [28540934 / 140002444 gas]
│                   └── ERC4626ETH.withdraw  999:1554  [28087484 / 111461510 gas]
│                       └── ERC4626ETH._withdraw  1031:1475  [473 / 83374026 gas]
│                           ├── ERC20._burn  1083:1202  [-12400 gas]
│                           └── Exploit  [STATICCALL]  1238:1447  [83385953 gas]
└── Vault.captureTheFlag  [CALL]  1866:1995  [29445460 gas]
```

## Notable PoC files:
- contracts/EthBomb.vy - vyper contract with self-destruct
- contracts/Exploit.vy - vyper contract with withdrawal, re-entrancy and CTF flag capture
- tests/test_vault.py - Brownie test containing the PoC flow

## Commands to execute the PoC:
```
pip install eth-brownie
brownie pm install OpenZeppelin/openzeppelin-contracts@4.7.3
brownie test
```
