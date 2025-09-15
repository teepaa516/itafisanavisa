import pandas as pd
import json
import os
import random
from typing import Dict, List

# Nämä asetetaan app.py:ssä sen mukaan, mikä CSV on valittu
PACKAGES_FILE = "packages.json"
HIGHSCORES_FILE = "highscores.json"
CSV_FILE = "verbit.csv"
PACKAGE_SIZE = 20

# --------------------
# Sanat
# --------------------
def load_words(csv_file: str | None = None) -> pd.DataFrame:
    """Lataa sanat CSV:stä ja varmistaa sarakkeet.
    Jos csv_file on None, käytetään utils.CSV_FILE -globaalimuuttujaa.
    """
    if csv_file is None:
        csv_file = CSV_FILE

    df = pd.read_csv(csv_file)
    expected = {"suomi", "italia", "epäsäännöllinen"}
    missing = expected - set(df.columns)
    if missing:
        raise ValueError(f"CSV:stä puuttuu sarakkeita: {', '.join(missing)}")
    for col in ["suomi", "italia", "epäsäännöllinen"]:
        df[col] = df[col].astype(str).fillna("").str.strip()
    return df


# --------------------
# Paketinhallinta
# --------------------
def load_packages(words: pd.DataFrame, package_size: int = PACKAGE_SIZE):
    """Lataa olemassa olevat paketit, tarkistaa pituuden"""
    if os.path.exists(PACKAGES_FILE):
        with open(PACKAGES_FILE, "r", encoding="utf-8") as f:
            packages = json.load(f)
        total = sum(len(p) for p in packages.values())
        return packages if total == len(words) else None
    return None

def save_packages(packages: Dict[str, List[int]]):
    """Tallenna pakettijako tiedostoon"""
    with open(PACKAGES_FILE, "w", encoding="utf-8") as f:
        json.dump(packages, f, ensure_ascii=False, indent=2)

def create_packages(words: pd.DataFrame, package_size: int = PACKAGE_SIZE):
    """Luo uusi pakettijako satunnaisesti"""
    indices = list(range(len(words)))
    random.shuffle(indices)
    packages = {}
    for i in range(0, len(indices), package_size):
        p_id = f"paketti_{i // package_size + 1}"
        packages[p_id] = indices[i : i + package_size]
    save_packages(packages)
    return packages

# --------------------
# Ennätysten hallinta
# --------------------
def load_highscores():
    """Lataa ennätykset JSON:ista"""
    if os.path.exists(HIGHSCORES_FILE):
        with open(HIGHSCORES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_highscores(scores):
    """Tallenna ennätykset JSON:iin"""
    with open(HIGHSCORES_FILE, "w", encoding="utf-8") as f:
        json.dump(scores, f, ensure_ascii=False, indent=2)

def reset_highscore(package_key: str | None = None):
    """Nollaa kaikki ennätykset tai tietyn paketin ennätyksen"""
    scores = load_highscores()
    if package_key:
        scores.pop(package_key, None)
    else:
        scores = {}
    save_highscores(scores)
    return scores
