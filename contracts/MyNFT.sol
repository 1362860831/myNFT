pragma solidity ^0.8.13;

import "./ERC721.sol";

contract MyNFT is ERC721 {
    uint constant public price = 1 ether;

    function mint(address payable to, uint id) external payable {
        require(msg.value >= price, "not enough money");
        uint rest = msg.value - price;
        to.transfer(rest);
        _mint(to, id);
    }

    function burn(uint id) external {
        require(msg.sender == _ownerOf[id], "not owner");
        _burn(id);
    }

    receive() external payable {}
}
