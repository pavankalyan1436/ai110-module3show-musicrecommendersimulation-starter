"""
Command line runner for the Music Recommender Simulation.

Loads the song catalog, scores every song for several taste profiles,
and prints the top recommendations with the reasons behind each score.
"""

from src.recommender import load_songs, recommend_songs

MAX_SCORE = 6.0

# Three distinct everyday profiles
STANDARD_PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.90, "likes_acoustic": False},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.40, "likes_acoustic": True},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.92, "likes_acoustic": False},
}

# Edge cases designed to test whether the scoring can be "tricked"
ADVERSARIAL_PROFILES = {
    "Conflicting: Sad but Energetic": {"genre": "blues", "mood": "sad", "energy": 0.95, "likes_acoustic": False},
    "Genre Not in Catalog": {"genre": "k-pop", "mood": "happy", "energy": 0.70, "likes_acoustic": False},
    "Acoustic Lover Wanting Max Energy": {"genre": "folk", "mood": "peaceful", "energy": 0.95, "likes_acoustic": True},
}


def print_recommendations(name: str, user_prefs: dict, recommendations: list) -> None:
    """Print a titled, numbered list of recommendations with score and reasons."""
    line = "=" * 60
    print(line)
    print(f"Profile: {name}")
    print(
        f"  genre={user_prefs['genre']}, mood={user_prefs['mood']}, "
        f"energy={user_prefs['energy']}, likes_acoustic={user_prefs.get('likes_acoustic', False)}"
    )
    print(line)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']} by {song['artist']}")
        print(f"   Score: {score:.2f} / {MAX_SCORE:.2f}")
        print("   Why:")
        for reason in explanation.split("; "):
            print(f"     - {reason}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    all_profiles = {**STANDARD_PROFILES, **ADVERSARIAL_PROFILES}
    for name, user_prefs in all_profiles.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(name, user_prefs, recommendations)


if __name__ == "__main__":
    main()
