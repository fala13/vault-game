# @version >=0.3.2

owner: immutable(address) 

@external
@payable
def __default__():
    pass

@external
@payable
def force_eth_to_contract(target: address):
    assert msg.sender == owner
    selfdestruct(target)

@external
@payable
def __init__():
    owner = msg.sender