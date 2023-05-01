const ERC721 = artifacts.require("ERC721");
const MyNFT = artifacts.require("MyNFT");

module.exports = function(deployer) {
  deployer.deploy(ERC721);
  deployer.link(ERC721, MyNFT);
  deployer.deploy(MyNFT);
};