
import pandas as pd

def prevMonth(ticker: pd.DataFrame):
    result = ticker.copy()
    result['Date'] = pd.to_datetime(result['Date'])
    result['group'] = result['Date'].dt.strftime("%Y-%m")

    m = result.groupby('group').agg({'Open':'first', 'High':'max', 'Low':'min', 'Close':'last', 'Adj Close':'last', 'Volume':'sum'})

    result['Date'] = result['Date'] - pd.DateOffset(months=1)
    result['group'] = result['Date'].dt.strftime("%Y-%m")

    result = result.merge(m, how='left', left_on='group', right_index=True, suffixes=('_', ''))

    return result.drop(['Open_', 'High_', 'Low_', 'Close_', 'Adj Close_', 'Volume_', 'group'], axis=1)