const Faucet = artifacts.require("Faucet");

module.exports = function(deployer, network, accounts) {
  deployer.deploy(Faucet, { from: accounts[0], value: "80000000000000000000" });
};