"""
unificar_presidencia2026.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Unifica los resultados de scraping (Twitter, TikTok, Facebook) para los
candidatos a la Presidencia 2026 al esquema de redes_unificadas.csv.

Uso:
    python unificar_presidencia2026.py

Salida:
    Elecciones presidencia 2026/resultados/presidencia2026_unificada.csv
"""

import os
import pandas as pd
from pathlib import Path

# ── Rutas ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR    = Path(os.path.abspath(__file__)).parent
RESULTADOS    = SCRIPT_DIR / 'resultados'
OUTPUT_FILE   = RESULTADOS / 'presidencia2026_unificada.csv'

FB_FILE  = RESULTADOS / 'presidencia2026_facebook.csv'
TT_FILE  = RESULTADOS / 'presidencia2026_tiktok.csv'
TW_FILE  = RESULTADOS / 'presidencia2026_tweets.csv'

# Columnas del esquema destino (mismo que redes_unificadas.csv)
SCHEMA_COLS = [
    'id_candidato', 'red_social', 'fecha', 'hora', 'usuario',
    'texto', 'url', 'likes', 'comentarios', 'compartidos', 'vistas',
    'fb_love', 'fb_haha', 'fb_care', 'fb_wow', 'fb_sad', 'fb_angry',
    'favoritos',
]

INTERACT_COLS = [
    'likes', 'comentarios', 'compartidos', 'vistas', 'favoritos',
    'fb_love', 'fb_haha', 'fb_care', 'fb_wow', 'fb_sad', 'fb_angry',
]


def _cast_ints(df: pd.DataFrame) -> pd.DataFrame:
    """Convierte columnas de interacción a int64, rellenando NaN con 0."""
    for col in INTERACT_COLS:
        if col not in df.columns:
            df[col] = 0
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype('int64')
    return df


# ── 1. Facebook ────────────────────────────────────────────────────────────────
def process_facebook(path: Path) -> pd.DataFrame:
    if not path.exists():
        print(f'  ⚠️  No existe: {path}')
        return pd.DataFrame()

    print(f'  📘 Facebook ({path.name})')
    df = pd.read_csv(path, sep=';', encoding='utf-8-sig', low_memory=False)

    time_col = 'time_col' if 'time_col' in df.columns else 'time'
    dt = pd.to_datetime(df[time_col], errors='coerce')

    out = pd.DataFrame({
        'id_candidato': df['id_candidato'],
        'red_social':   'Facebook',
        'fecha':        dt.dt.strftime('%Y-%m-%d'),
        'hora':         dt.dt.strftime('%H:%M:%S'),
        'usuario':      df.get('pageName', ''),
        'texto':        df.get('text', ''),
        'url':          df.get('url', ''),
        'likes':        df.get('likes', 0),
        'comentarios':  df.get('comments', 0),
        'compartidos':  df.get('shares', 0),
        'vistas':       df.get('viewsCount', 0),
        'fb_love':      df.get('reactionLoveCount', 0),
        'fb_haha':      df.get('reactionHahaCount', 0),
        'fb_care':      df.get('reactionCareCount', 0),
        'fb_wow':       df.get('reactionWowCount', 0),
        'fb_sad':       df.get('reactionSadCount', 0),
        'fb_angry':     df.get('reactionAngryCount', 0),
        'favoritos':    0,
    })
    print(f'     → {len(out)} posts')
    return out


# ── 2. TikTok ──────────────────────────────────────────────────────────────────
def process_tiktok(path: Path) -> pd.DataFrame:
    if not path.exists():
        print(f'  ⚠️  No existe: {path}')
        return pd.DataFrame()

    print(f'  🎵 TikTok ({path.name})')
    df = pd.read_csv(path, sep=';', encoding='utf-8-sig', low_memory=False)

    # uploadedAt puede ser Unix timestamp (int) o ISO string
    raw = df['uploadedAt']
    try:
        dt = pd.to_datetime(raw.astype(float), unit='s', errors='coerce')
    except (ValueError, TypeError):
        dt = pd.to_datetime(raw, errors='coerce')

    # Extraer username del campo channel (puede ser JSON string o plain text)
    def _extract_username(val):
        if pd.isna(val):
            return ''
        s = str(val)
        # Si es JSON, intentar extraer "username"
        import json
        try:
            obj = json.loads(s)
            return obj.get('username', s)
        except Exception:
            return s

    username = df['channel'].apply(_extract_username)

    out = pd.DataFrame({
        'id_candidato': df['id_candidato'],
        'red_social':   'TikTok',
        'fecha':        dt.dt.strftime('%Y-%m-%d'),
        'hora':         dt.dt.strftime('%H:%M:%S'),
        'usuario':      username,
        'texto':        df.get('title', ''),
        'url':          df.get('postPage', ''),
        'likes':        df.get('likes', 0),
        'comentarios':  df.get('comments', 0),
        'compartidos':  df.get('shares', 0),
        'vistas':       df.get('views', 0),
        'favoritos':    df.get('bookmarks', 0),
    })
    print(f'     → {len(out)} videos')
    return out


# ── 3. Twitter ─────────────────────────────────────────────────────────────────
def process_twitter(path: Path) -> pd.DataFrame:
    if not path.exists():
        print(f'  ⚠️  No existe: {path}')
        return pd.DataFrame()

    print(f'  🐦 Twitter ({path.name})')
    df = pd.read_csv(path, sep=';', encoding='utf-8-sig', low_memory=False)

    dt = pd.to_datetime(df['date'], errors='coerce')

    out = pd.DataFrame({
        'id_candidato': df['id_candidato'],
        'red_social':   'Twitter',
        'fecha':        dt.dt.strftime('%Y-%m-%d'),
        'hora':         dt.dt.strftime('%H:%M:%S'),
        'usuario':      df.get('account', ''),
        'texto':        df.get('text', ''),
        'url':          df.get('url', ''),
        'likes':        df.get('like_count', 0),
        'comentarios':  df.get('reply_count', 0),
        'compartidos':  df.get('retweet_count', 0),
        'vistas':       df.get('view_count', 0),
        'favoritos':    0,
    })
    print(f'     → {len(out)} tweets')
    return out


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    print('\n🔄 Unificando datos de redes sociales (Presidencia 2026)\n')

    dfs = []
    for fn in [process_facebook, process_tiktok, process_twitter]:
        source_map = {
            process_facebook: FB_FILE,
            process_tiktok:   TT_FILE,
            process_twitter:  TW_FILE,
        }
        df = fn(source_map[fn])
        if not df.empty:
            dfs.append(df)

    if not dfs:
        print('\n❌ No se encontraron datos para unificar.')
        return

    df_final = pd.concat(dfs, ignore_index=True)

    # Asegurar que todas las columnas del esquema existan
    for col in SCHEMA_COLS:
        if col not in df_final.columns:
            df_final[col] = 0 if col in INTERACT_COLS else ''

    df_final = _cast_ints(df_final)
    df_final = df_final[SCHEMA_COLS]          # reordenar al esquema exacto

    RESULTADOS.mkdir(parents=True, exist_ok=True)
    df_final.to_csv(OUTPUT_FILE, index=False, sep=';', encoding='utf-8-sig')

    print(f'\n✅ Archivo unificado guardado en:')
    print(f'   {OUTPUT_FILE}')
    print(f'\n📊 Total publicaciones: {len(df_final)}')
    print('\nResumen por red social:')
    print(df_final['red_social'].value_counts().to_string())
    print('\nResumen por candidato:')
    print(df_final['id_candidato'].value_counts().to_string())


if __name__ == '__main__':
    main()
