async function getCoinInfo() {
    let urlCoins = '/side/bitget_spot_asset.php';
    let urlRates = '/side/spot-ticker.php';

    let coins = await fetch(urlCoins).then(response => response.json());
    let rates = await fetch(urlRates).then(response => response.json());

    let coinRates = {};
    for (let rate of rates.data) {
        let coinName = rate.symbol.replace('USDT', '');
        coinRates[coinName] = parseFloat(rate.close);
    }

    let coinInfo = '';
    let totalValue = 0;
    for (let coin of coins) {
        if (parseFloat(coin.available) > 0.00001) {
            let iconPath = `imc/coin_icon/${coin.coinName.toLowerCase()}.png`;
            let available = parseFloat(coin.available).toFixed(8);

            let coinValue;
            if (coin.coinName === "USDT") {
                coinValue = parseFloat(available).toFixed(2);
            } else if (coinRates[coin.coinName]) { 
                coinValue = (parseFloat(coin.available) * coinRates[coin.coinName]).toFixed(2);
            } else {
                coinValue = "N/A";
            }

            if (coinValue !== "N/A") {
                totalValue += parseFloat(coinValue);
            }

            coinInfo += `<div class="coin-box">
            <img class="coin-icon" src="${iconPath}" onerror="this.onerror=null; this.src='imc/coin_icon/no_pic.png';" alt="${coin.coinName} Icon">
            <p>${available}</p>
            <p class="coin-name">${coin.coinName}</p>
            <p class="coin-value">${coinValue} USDT</p>
         </div>`;
        }
    }

    let statusMainCoinElement = document.querySelector(".status-main-coin");
    let cashCsElement = document.querySelector(".cash-cs");

    console.log(statusMainCoinElement); // Sollte das Element mit der Klasse .status-main-coin ausgeben
    console.log(cashCsElement); // Sollte das Element mit der Klasse .cash-cs ausgeben

    if (statusMainCoinElement) {
        statusMainCoinElement.innerHTML = coinInfo;
    }

    if (cashCsElement) {
        cashCsElement.innerText = `${totalValue.toFixed(2)} USDT`;
    }
}

getCoinInfo(); 

setInterval(getCoinInfo, 5000); // Rufen Sie die getCoinInfo Funktion alle 5000 Millisekunden (5 sec) auf


