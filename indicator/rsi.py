
import pandas as pd

def rsi(source: pd.Series, length: int) -> pd.Series:
    delta = source.diff().fillna(0)
    
    avg_gain = delta.where(delta > 0, 0).ewm(alpha=1/length, adjust=False).mean()
    avg_loss = -delta.where(delta < 0, 0).ewm(alpha=1/length, adjust=False).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi