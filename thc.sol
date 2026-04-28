// SPDX-License-Identifier: MIT
// 👉 License declare करतो (open-source, safe for use)

pragma solidity ^0.8.20;
// 👉 Solidity compiler version (0.8.20 किंवा compatible version वापरेल)

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
// 👉 Ready-made ERC20 token logic import (transfer, balance, supply etc.)

contract HuntCoin is ERC20 {
    // 👉 आपला contract ERC20 inherit करतो (म्हणजे सगळे standard functions मिळतात)

    address public owner;
    // 👉 Owner (admin) address store करतो

    // 👉 Constructor: contract deploy होताना एकदाच run होतो
    constructor(address _owner) ERC20("Hunt Coin", "thc") {
        // 👉 ERC20 constructor call करतो (name = Hunt Coin, symbol = thc)

        owner = _owner;
        // 👉 जो address deploy करताना दिला तो owner बनतो

        _mint(owner, 1000000 * 10 ** decimals());
        // 👉 10 लाख coins तयार करून owner ला देतो
        // 👉 decimals() = usually 18 (ERC20 standard)
    }

    // 👉 Custom modifier (security layer)
    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        // 👉 जर function call करणारा owner नसेल तर error दे

        _;
        // 👉 पुढचा function run होऊ दे (if condition true)
    }

    // 👉 Mint function (new coins create करण्यासाठी)
    function mint(address to, uint256 amount) public onlyOwner {
        // 👉 फक्त owner हा function call करू शकतो

        _mint(to, amount);
        // 👉 दिलेल्या address ला new coins देतो
    }

    // 👉 Burn function (coins destroy करण्यासाठी)
    function burn(uint256 amount) public onlyOwner {
        // 👉 फक्त owner वापरू शकतो

        _burn(owner, amount);
        // 👉 owner च्या balance मधून coins delete करतो
    }

    // 👉 Ownership transfer function
    function transferOwnership(address newOwner) public onlyOwner {
        // 👉 फक्त current owner ownership बदलू शकतो

        owner = newOwner;
        // 👉 newOwner ला admin control देतो
    }
}