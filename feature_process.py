def add_features(feats):
    feats = feats.sort_values(by='Date').reset_index(drop=True)
    feats["return_1month"] = feats["Close"].pct_change(20)
    feats["return_2month"] = feats["Close"].pct_change(40)
    feats["return_3month"] = feats["Close"].pct_change(60)

    feats["volatility_1month"] = (
        np.log(feats["Close"]).diff().rolling(20).std()
    )
    feats["volatility_2month"] = (
        np.log(feats["Close"]).diff().rolling(40).std()
    )
    feats["volatility_3month"] = (
        np.log(feats["Close"]).diff().rolling(60).std()
    )

    feats["MA_gap_1month"] = feats["Close"] / (
        feats["Close"].rolling(20).mean()
    )
    feats["MA_gap_2month"] = feats["Close"] / (
        feats["Close"].rolling(40).mean()
    )
    feats["MA_gap_3month"] = feats["Close"] / (
        feats["Close"].rolling(60).mean()
    )

    feats["Volume_gap_1month"] = feats["Volume"] / (
        feats["Volume"].rolling(20).mean()
    )
    feats["Volume_gap_2month"] = feats["Volume"] / (
        feats["Volume"].rolling(40).mean()
    )
    feats["Volume_gap_3month"] = feats["Volume"] / (
        feats["Volume"].rolling(60).mean()
    )
    today_features = [ 'Open', 'High', 'Low', 'Close', 'Volume', 'return_1month',
                       'return_2month', 'return_3month', 'volatility_1month',
                       'volatility_2month', 'volatility_3month', 'MA_gap_1month',
                       'MA_gap_2month', 'MA_gap_3month', 'Volume_gap_1month',
                       'Volume_gap_2month', 'Volume_gap_3month']
    for feature in today_features:
        for n in [1, 3, 5]:
            feats['last_'+ str(n) + '_' + feature] = [-1] * n + list(feats[feature])[:-n]

        if feature in ['Open', 'High', 'Low', 'Close', 'Volume']:
            feats['last_sum_' + feature] = 0
        for n in [1,  3,  5]:
            if feature in [ 'Open', 'High', 'Low', 'Close', 'Volume']:
                feats['last_sum_' + feature] =\
                    feats['last_sum_' + feature] + feats['last_' + str(n) + '_' + feature]
        for n in [1,  3, 5]:
            if feature in [ 'Open', 'High', 'Low', 'Close', 'Volume']:
                feats['last_mean_' + str(n) + '_' + feature] = \
                    feats['last_' + str(n) + '_' + feature] / feats['last_sum_' + feature]
    return feats

def feature_process():
    dfs = pd.read_csv('stock_prices.csv')
    codes = sorted(list(dfs['SecuritiesCode'].unique()))
    new_df = pd.concat([add_features(dfs[(dfs['SecuritiesCode'] == code)]) for code in codes
                        if len(dfs[(dfs['SecuritiesCode'] == code)]) > 100
                        ]).reset_index(drop=True)
    new_df.to_csv('new_data/feature_processed_data.csv', index = False)

feature_process()
    
