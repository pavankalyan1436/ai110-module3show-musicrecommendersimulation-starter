"""
Weight-shift experiment: compare the baseline weights with a version that
doubles the importance of energy and halves the importance of genre.

Run with:  python -m src.experiment
"""

from src.main import ADVERSARIAL_PROFILES, STANDARD_PROFILES
from src.recommender import DEFAULT_WEIGHTS, load_songs, recommend_songs

SHIFTED_WEIGHTS = {**DEFAULT_WEIGHTS, "genre": DEFAULT_WEIGHTS["genre"] / 2, "energy": DEFAULT_WEIGHTS["energy"] * 2}


def top_titles(user_prefs: dict, songs: list, weights: dict) -> list:
    """Return [(title, score), ...] for the top 5 songs under the given weights."""
    return [(s["title"], sc) for s, sc, _ in recommend_songs(user_prefs, songs, k=5, weights=weights)]


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Baseline weights: {DEFAULT_WEIGHTS}")
    print(f"Shifted weights:  {SHIFTED_WEIGHTS}  (energy x2, genre x0.5)\n")

    for name, prefs in {**STANDARD_PROFILES, **ADVERSARIAL_PROFILES}.items():
        base = top_titles(prefs, songs, DEFAULT_WEIGHTS)
        shifted = top_titles(prefs, songs, SHIFTED_WEIGHTS)
        print(f"Profile: {name}")
        print("  rank  baseline                         shifted")
        for i, ((bt, bs), (st, ss)) in enumerate(zip(base, shifted), start=1):
            marker = "" if bt == st else "   <- changed"
            print(f"  {i}.    {bt:<22} {bs:4.2f}     {st:<22} {ss:4.2f}{marker}")
        print()


if __name__ == "__main__":
    main()
