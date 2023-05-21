# Correlations

This can be used to pull historical correlations from the binance api.

## Results

Results can be found in `data/processed`

|                 |   BTCUSDT price |   ETHUSDT price |   XRPUSDT price |   LTCUSDT price |   RNDRUSDT price |   MATICUSDT price |   CFXUSDT price |   DOGEUSDT price |   SOLUSDT price |   INJUSDT price |   LDOUSDT price |   FTMUSDT price |   OPUSDT price |   ADAUSDT price |
|:----------------|----------------:|----------------:|----------------:|----------------:|-----------------:|------------------:|----------------:|-----------------:|----------------:|----------------:|----------------:|----------------:|---------------:|----------------:|
| BTCUSDT price   |        1        |        0.877847 |        0.630769 |        0.707404 |         0.426411 |          0.735013 |        0.354564 |         0.627108 |        0.696656 |        0.453006 |        0.407218 |        0.674931 |       0.60292  |        0.735525 |
| ETHUSDT price   |        0.877847 |        1        |        0.642245 |        0.722287 |         0.424738 |          0.765156 |        0.335766 |         0.648623 |        0.709863 |        0.443831 |        0.428977 |        0.68688  |       0.622837 |        0.755312 |
| XRPUSDT price   |        0.630769 |        0.642245 |        1        |        0.585801 |         0.32899  |          0.603582 |        0.271414 |         0.547047 |        0.567462 |        0.370586 |        0.323031 |        0.565905 |       0.486955 |        0.635315 |
| LTCUSDT price   |        0.707404 |        0.722287 |        0.585801 |        1        |         0.372689 |          0.666319 |        0.313085 |         0.596782 |        0.623081 |        0.412492 |        0.365409 |        0.634486 |       0.549322 |        0.685826 |
| RNDRUSDT price  |        0.426411 |        0.424738 |        0.32899  |        0.372689 |         1        |          0.395092 |        0.216747 |         0.336711 |        0.371474 |        0.273503 |        0.230419 |        0.389566 |       0.336735 |        0.396688 |
| MATICUSDT price |        0.735013 |        0.765156 |        0.603582 |        0.666319 |         0.395092 |          1        |        0.326215 |         0.620967 |        0.687304 |        0.438454 |        0.387761 |        0.682203 |       0.59203  |        0.713369 |
| CFXUSDT price   |        0.354564 |        0.335766 |        0.271414 |        0.313085 |         0.216747 |          0.326215 |        1        |         0.274929 |        0.301574 |        0.240719 |        0.204843 |        0.332223 |       0.280756 |        0.321599 |
| DOGEUSDT price  |        0.627108 |        0.648623 |        0.547047 |        0.596782 |         0.336711 |          0.620967 |        0.274929 |         1        |        0.595829 |        0.390855 |        0.32966  |        0.590127 |       0.50868  |        0.635869 |
| SOLUSDT price   |        0.696656 |        0.709863 |        0.567462 |        0.623081 |         0.371474 |          0.687304 |        0.301574 |         0.595829 |        1        |        0.410771 |        0.359415 |        0.631334 |       0.547736 |        0.681515 |
| INJUSDT price   |        0.453006 |        0.443831 |        0.370586 |        0.412492 |         0.273503 |          0.438454 |        0.240719 |         0.390855 |        0.410771 |        1        |        0.261259 |        0.440299 |       0.366472 |        0.436003 |
| LDOUSDT price   |        0.407218 |        0.428977 |        0.323031 |        0.365409 |         0.230419 |          0.387761 |        0.204843 |         0.32966  |        0.359415 |        0.261259 |        1        |        0.381152 |       0.350372 |        0.382241 |
| FTMUSDT price   |        0.674931 |        0.68688  |        0.565905 |        0.634486 |         0.389566 |          0.682203 |        0.332223 |         0.590127 |        0.631334 |        0.440299 |        0.381152 |        1        |       0.573298 |        0.680204 |
| OPUSDT price    |        0.60292  |        0.622837 |        0.486955 |        0.549322 |         0.336735 |          0.59203  |        0.280756 |         0.50868  |        0.547736 |        0.366472 |        0.350372 |        0.573298 |       1        |        0.593607 |
| ADAUSDT price   |        0.735525 |        0.755312 |        0.635315 |        0.685826 |         0.396688 |          0.713369 |        0.321599 |         0.635869 |        0.681515 |        0.436003 |        0.382241 |        0.680204 |       0.593607 |        1        |

## Usage

This retreives the start datetime for each symbol and prints it. I used this info to decide which tickers to withold in the correlation matrix (i.e. dont include sui bc its been trading only for a week).

```python
python3 check_start.py
```

This pulls the data from binance, formats it, and creates the pct_return / correlation dataframes.

Scroll down to the end of the file to make modifications (add/remove tickers, etc)
```python
python2 correlations.py
```

Note: you need to be on a vpn when running this. Also seem to not be able to run on Colab.
