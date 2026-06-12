import numpy as np
import pandas as pd

def performance(data):

    result = pd.DataFrame(index=['Stategy Results'])

    #calculating sharpe
    returns = data['returns']
    
    if returns.std() != 0:
        result['sharpe'] = (np.sqrt(252) * (returns.mean() / returns.std()))
    else:
        result['sharpe'] = np.nan
    
    # calculating winning rate
    win_rate = (returns>0).mean()
    result['win rate(in %)'] = win_rate*100

    #calculating cumulative return for each day and using last as final    
    cumulative_path = (1 + returns).cumprod()
    cum_ret_final = cumulative_path.iloc[-1] - 1
    result['cumulative_return'] = cum_ret_final

    #calculating annualized return with the help of final cumulative return
    ann_ret = (1 + cum_ret_final) ** (252 / len(returns)) - 1
    result['annualized_return'] = ann_ret

    #calculating result['sortino ratio'] ratio 
    risk_free_rate = 0.04/252
    downside_std = np.sqrt(np.mean(np.minimum(returns, 0)**2))
    if downside_std != 0:
        result['sortino ratio'] = np.sqrt(252)*(returns.mean()-risk_free_rate)/downside_std
    else:
        result['sortino ratio'] = np.nan

    #calculating maximum drawdown by its definition
    rolling_max = cumulative_path.cummax()
    drawdown = (cumulative_path / rolling_max) - 1
    result['Maximum Drawdown'] = drawdown.min()

    #adding drawdown into data for graph representation
    data.loc[returns.index,'drawdown'] = drawdown 

    #calculating profit and losses
    p_and_l = data['delta']

    profits = p_and_l[p_and_l>0]
    losses = p_and_l[p_and_l<0]
    result['avg_profit(in ₹)'] = (profits.mean() if(len(profits)>0) else np.nan)  
    result['avg_loss(in ₹)'] = (abs(losses.mean()) if(len(losses)>0) else np.nan)
    result['max_profit(in ₹)'] = (profits.max() if(len(profits)>0) else np.nan) 
    result['max_loss(in ₹)'] = (abs(losses.min()) if(len(losses)>0) else np.nan) 
    
    return result