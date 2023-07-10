<!DOCTYPE html>
<html>
<head>
    <title>Candlestick Chart mit Bitget-Daten</title>
    <script src="https://cdn.jsdelivr.net/npm/apexcharts"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
</head>
<body>
    <div id="chart"></div>

    <script>
        var options = {
            series: [
                {
                    data: []
                }
            ],
            chart: {
                type: 'candlestick',
                height: 350
            },
            xaxis: {
                type: 'datetime'
            },
            yaxis: {
                tooltip: {
                    enabled: true
                }
            }
        };

        var chart = new ApexCharts(document.querySelector("#chart"), options);
        chart.render();

        // AJAX-Anfrage an get_candle_data.php senden
        $.ajax({
            url: 'https://eule-trading.site:8000/candleData',
            type: 'GET',
            dataType: 'json',
            success: function(response) {
                var candlestickData = response;

                var formattedData = candlestickData.map(function(data) {
                    return {
                        x: new Date(parseInt(data[0])),
                        y: [parseFloat(data[1]), parseFloat(data[2]), parseFloat(data[3]), parseFloat(data[4])]
                    };
                });

                chart.updateSeries([{ data: formattedData }]);
            },
            error: function(xhr, status, error) {
                console.error(error);
            }
        });
    </script>
</body>
</html>
