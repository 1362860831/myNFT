const AOSRing = artifacts.require("AOSRing");
const Curve = artifacts.require("Curve");
const Schnorr = artifacts.require("Schnorr");

module.exports = function(deployer) {
  deployer.deploy(Curve);
  deployer.link(Curve, [Schnorr, AOSRing]);
  deployer.deploy(Schnorr);
  deployer.link(Schnorr, AOSRing);
  deployer.deploy(AOSRing);
};