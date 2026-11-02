"""
Command line runner for the Music Recommender Simulation.

Loads the song catalog, scores every song for a taste profile,
and prints the top recommendations with the reasons behind each score.
"""

from src.recommender import load_songs, recommend_songs

MAX_SCORE = 6.0


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

    # Starter example profile
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "likes_acoustic": False,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)
    print_recommendations("Pop / Happy", user_prefs, recommendations)


if __name__ == "__main__":
    main()
