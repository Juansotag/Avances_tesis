import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from pyGRNN import GRNN
import matplotlib.pyplot as plt
import seaborn as sns

def rename_account(account, paz_orig, quiroga_orig):
    """Standardizes account names to 'Paz' or 'Quiroga'."""
    if account == paz_orig:
        return 'Paz'
    elif account == quiroga_orig:
        return 'Quiroga'
    return account

def load_and_aggregate_platform(filepath, sheet_name, date_col, numeric_cols, id_col, rename_params, date_range):
    """
    Loads a sheet from Excel, cleans it, renames accounts, 
    and aggregates data daily, including empty days.
    """
    df = pd.read_excel(filepath, sheet_name=sheet_name)
    
    # Basic cleaning
    if 'postId' in df.columns:
        df = df.drop_duplicates(subset=['postId'], keep='first')
    elif 'id' in df.columns:
        df = df.drop_duplicates(subset=['id'], keep='first')
        
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce').dt.date
    df[numeric_cols] = df[numeric_cols].fillna(0)
    
    # Rename
    df[id_col] = df[id_col].apply(lambda x: rename_account(x, *rename_params))
    
    # Aggregation
    agg_dict = {c: 'sum' for c in numeric_cols}
    agg_dict['posts'] = ('account' if id_col=='account' else id_col, 'count') # Proxy for count
    
    # We need to be careful with the .agg syntax for named columns
    raw_agg = df.groupby([id_col, date_col]).agg(
        posts=(id_col, 'count'),
        **{c: (c, 'sum') for c in numeric_cols}
    ).reset_index()
    
    # Reindex to include all dates
    accounts = raw_agg[id_col].unique()
    fechas = [d.date() for d in pd.date_range(start=date_range[0], end=date_range[1])]
    base = pd.DataFrame([(a, f) for a in accounts for f in fechas], columns=[id_col, date_col])
    
    final_agg = base.merge(raw_agg, on=[id_col, date_col], how='left').fillna(0)
    
    # Calculate Averages (AVG)
    final_avg = final_agg.copy()
    for col in numeric_cols:
        final_avg[col] = final_agg[col] / final_agg['posts'].replace(0, np.nan)
    final_avg = final_avg.fillna(0)
    
    # Merge AGG and AVG
    return final_agg.merge(final_avg, on=[id_col, date_col, 'posts'], suffixes=('_agg', '_avg'))

def normalizar_y_suavizar(df, columnas_id, columnas_features, window=1, por_cuenta=True):
    """
    Normalizes features and applies a rolling mean.
    """
    scaler = MinMaxScaler(feature_range=(0, 1))
    df_result = []

    if por_cuenta:
        for account, group in df.groupby('account'):
            g = group.copy().sort_values(by=columnas_id[1])
            g[columnas_features] = scaler.fit_transform(g[columnas_features])
            if window > 1:
                g[columnas_features] = g[columnas_features].rolling(window=window, min_periods=1).mean()
            df_result.append(g)
        df_final = pd.concat(df_result, ignore_index=True)
    else:
        df_final = df.copy()
        df_final[columnas_features] = scaler.fit_transform(df[columnas_features])
        if window > 1:
            df_final = df_final.sort_values(by=columnas_id)
            df_final[columnas_features] = df_final[columnas_features].rolling(window=window, min_periods=1).mean()

    return df_final.infer_objects(copy=False)

def daily_intent_from_polls(polls_df, election_date, election_result):
    """
    Interpolates poll data to create a daily series.
    """
    dfp = polls_df.copy()
    for c in ['Quiroga', 'Paz']:
        if dfp[c].max() > 1.0:
            dfp[c] = dfp[c] / 100.0

    s = dfp[['Quiroga', 'Paz']].sum(axis=1).replace(0, np.nan)
    dfp['Quiroga'] = dfp['Quiroga'] / s
    dfp['Paz'] = dfp['Paz'] / s

    q_fin = election_result['Quiroga'] / 100.0 if election_result['Quiroga'] > 1 else election_result['Quiroga']
    p_fin = election_result['Paz'] / 100.0 if election_result['Paz'] > 1 else election_result['Paz']
    
    dfp = pd.concat([
        dfp,
        pd.DataFrame([{'fecha': pd.to_datetime(election_date), 'Quiroga': q_fin, 'Paz': p_fin}])
    ], ignore_index=True).sort_values('fecha')

    idx = pd.date_range(dfp['fecha'].min(), dfp['fecha'].max(), freq='D')
    return (dfp.set_index('fecha')
            .reindex(idx)
            .interpolate('linear')
            .bfill().ffill()
            .reset_index()
            .rename(columns={'index': 'date'}))

def run_model(model_type, X_train, y_train, X_pred):
    """
    Trains and predicts using the specified model.
    """
    if model_type == 'LR':
        model = LinearRegression()
    elif model_type == 'MLP':
        model = MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=2000, random_state=42)
    elif model_type == 'GRNN':
        model = GRNN()
    else:
        raise ValueError("Unknown model type")
        
    model.fit(X_train, y_train)
    return model.predict(X_pred)
