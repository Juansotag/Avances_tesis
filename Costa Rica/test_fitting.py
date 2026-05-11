import pandas as pd
import numpy as np
import hashlib
from scipy.optimize import curve_fit
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# 1. Carga y preparación de datos
print("Cargando datos...")
file_path = 'Scrapping data v2.xlsx'
xl = pd.ExcelFile(file_path)

df_fb = pd.read_excel(xl, sheet_name='Facebook')
df_ig = pd.read_excel(xl, sheet_name='Instagram')
df_tk = pd.read_excel(xl, sheet_name='TikTok')
df_tw = pd.read_excel(xl, sheet_name='Twitter')

def generate_id(text):
    if pd.isna(text): return "missing_text"
    return hashlib.md5(str(text).encode('utf-8')).hexdigest()

if df_tw['postId'].isnull().all() or df_tw['postId'].astype(str).str.strip().eq('').all():
    df_tw['postId'] = df_tw['text'].apply(generate_id)

def prepare_evolution_df(df, platform, mapping, user_col, id_col, date_pub_col):
    df = df.copy()
    df.columns = df.columns.astype(str).str.strip()
    actual_user_col = next((col for col in [user_col, 'Username', 'name', 'Candidato'] if col in df.columns), None)
    if actual_user_col:
        df['candidate'] = df[actual_user_col].astype(str)
    else:
        df['candidate'] = "Desconocido"
    
    df = df[~df['candidate'].str.contains('Desconocido|nan|None', case=False, na=True)]
    df['platform'] = platform
    df['internal_post_id'] = platform + "_" + df[id_col].astype(str)
    df = df.rename(columns=mapping)
    
    df['fecha_ext'] = pd.to_datetime(df['fecha_ext'], errors='coerce', dayfirst=True).dt.tz_localize(None)
    df['fecha_pub'] = pd.to_datetime(df[date_pub_col], errors='coerce', dayfirst=True).dt.tz_localize(None)
    df['dia_relativo'] = (df['fecha_ext'] - df['fecha_pub']).dt.days + 1
    
    for col in ['likes', 'comments', 'shares']:
        if col in df.columns: df[col] = pd.to_numeric(df[col], errors='coerce')
        else: df[col] = 0.0
            
    return df[['internal_post_id', 'platform', 'candidate', 'dia_relativo', 'likes', 'comments', 'shares']]

ev_fb = prepare_evolution_df(df_fb, 'Facebook', {'megusta': 'likes', 'comentarios': 'comments', 'compartidas': 'shares'}, 'Username', 'postId', 'fecha_pub')
ev_ig = prepare_evolution_df(df_ig, 'Instagram', {'megusta': 'likes', 'comentarios': 'comments'}, 'Username', 'postId', 'fecha_pub')
ev_tk = prepare_evolution_df(df_tk, 'TikTok', {'megusta': 'likes', 'comentarios': 'comments', 'compartidos': 'shares'}, 'Username', 'postId', 'fecha_pub')
ev_tw = prepare_evolution_df(df_tw, 'Twitter', {'likecount': 'likes', 'replycount': 'comments', 'retweet_count': 'shares'}, 'Username', 'postId', 'createdat')

df_combined = pd.concat([ev_fb, ev_ig, ev_tk, ev_tw], ignore_index=True)
df_combined['total_int'] = df_combined['likes'] + df_combined['comments'] + df_combined['shares']

def interpolate_and_calc_pct(group):
    group = group.sort_values('dia_relativo').drop_duplicates('dia_relativo')
    if len(group) < 1: return None
    
    group['total_int'] = group['total_int'].cummax()
    min_day, max_day = int(group['dia_relativo'].min()), int(group['dia_relativo'].max())
    
    if max_day > min_day:
        full_range = pd.DataFrame({'dia_relativo': range(min_day, max_day + 1)})
        meta_cols = [c for c in ['internal_post_id', 'platform', 'candidate'] if c in group.columns]
        if meta_cols:
            meta = group.iloc[0][meta_cols]
            group = pd.merge(full_range, group, on='dia_relativo', how='left')
            for col in meta_cols: group[col] = meta[col]
        else:
            group = pd.merge(full_range, group, on='dia_relativo', how='left')
        group['total_int'] = group['total_int'].interpolate(method='linear')
    
    total = group['total_int'].max()
    group['total_int_pct'] = (group['total_int'] / total) if total > 0 else 0
        
    return group

print("Procesando curvas...")
df_pct = df_combined.groupby('internal_post_id', group_keys=False).apply(interpolate_and_calc_pct)
df_pct = df_pct.dropna(subset=['internal_post_id'])

# Agrupar por dia_relativo para encontrar la curva promedio global
avg_curve = df_pct.groupby('dia_relativo')['total_int_pct'].mean().reset_index()
# Fill forward to keep it monotonic if it drops due to composition bias
avg_curve['total_int_pct'] = avg_curve['total_int_pct'].cummax()

x_data = avg_curve['dia_relativo'].values
y_data = avg_curve['total_int_pct'].values

# Funciones de distribución (CDF)
def logistic_curve(x, L, k, x0):
    return L / (1 + np.exp(-k * (x - x0)))

def gompertz_curve(x, a, b, c):
    return a * np.exp(-b * np.exp(-c * x))

def lognormal_cdf(x, s, scale):
    from scipy.stats import lognorm
    return lognorm.cdf(x, s, scale=scale)

def exponential_cdf(x, lam):
    from scipy.stats import expon
    return expon.cdf(x, scale=1/lam)

print("Ajustando modelos...")
results = []
try:
    popt_log, _ = curve_fit(logistic_curve, x_data, y_data, p0=[1, 1, 1], maxfev=10000)
    y_pred = logistic_curve(x_data, *popt_log)
    results.append(('Logistic', r2_score(y_data, y_pred), popt_log))
except:
    pass

try:
    popt_gomp, _ = curve_fit(gompertz_curve, x_data, y_data, p0=[1, 1, 1], maxfev=10000)
    y_pred = gompertz_curve(x_data, *popt_gomp)
    results.append(('Gompertz', r2_score(y_data, y_pred), popt_gomp))
except:
    pass

try:
    popt_exp, _ = curve_fit(exponential_cdf, x_data, y_data, p0=[1], maxfev=10000)
    y_pred = exponential_cdf(x_data, *popt_exp)
    results.append(('Exponential', r2_score(y_data, y_pred), popt_exp))
except:
    pass

for name, r2, popt in results:
    print(f"Modelo: {name}, R2: {r2:.4f}, Params: {popt}")

