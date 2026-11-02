import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv into a list of dicts, converting numeric columns to int/float."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            for key in ("energy", "tempo_bpm", "valence", "danceability", "acousticness"):
                row[key] = float(row[key])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs

# Points available for each part of the scoring recipe (max total = 6.0)
DEFAULT_WEIGHTS = {"genre": 2.0, "mood": 1.5, "energy": 1.5, "acoustic": 1.0}

def score_song(user_prefs: Dict, song: Dict, weights: Optional[Dict] = None) -> Tuple[float, List[str]]:
    """Score one song using the weighted recipe; return (score, reasons)."""
    w = weights or DEFAULT_WEIGHTS
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs["genre"]:
        score += w["genre"]
        reasons.append(f"genre match (+{w['genre']:.1f})")

    if song["mood"] == user_prefs["mood"]:
        score += w["mood"]
        reasons.append(f"mood match (+{w['mood']:.1f})")

    energy_points = w["energy"] * (1 - abs(song["energy"] - user_prefs["energy"]))
    score += energy_points
    reasons.append(f"energy closeness (+{energy_points:.2f})")

    if user_prefs.get("likes_acoustic", False):
        acoustic_points = w["acoustic"] * song["acousticness"]
    else:
        acoustic_points = w["acoustic"] * (1 - song["acousticness"])
    score += acoustic_points
    reasons.append(f"acoustic fit (+{acoustic_points:.2f})")

    return score, reasons

def recommend_songs(
    user_prefs: Dict, songs: List[Dict], k: int = 5, weights: Optional[Dict] = None
) -> List[Tuple[Dict, float, str]]:
    """Score every song with score_song, then return the top k as (song, score, explanation)."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, weights)
        scored.append((song, score, "; ".join(reasons)))
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]
