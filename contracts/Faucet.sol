pragma solidity ^0.8.13;

contract Faucet{
    event Withdraw(address indexed account, uint amount);

    function withdraw(uint amount, address account) public {
        require (amount <= 0.1 ether, "please do not claim over 0.1 ether one time!");
        require (amount <= address(this).balance, "the contract has no money!");
        payable(account).transfer(amount);
        emit Withdraw(account, amount);
    }
    constructor() payable{}
    receive() external payable {}
}