"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from recommender import load_songs, recommend_songs
except ModuleNotFoundError:
    from src.recommender import load_songs, recommend_songs


# --- standard profiles ---
HIGH_ENERGY_POP = {
    "name":        "High-Energy Pop",
    "genre":       "pop",
    "mood":        "happy",
    "energy":      0.88,
    "valence":     0.85,
    "acousticness": 0.05,
}

CHILL_LOFI = {
    "name":        "Chill Lofi",
    "genre":       "lofi",
    "mood":        "chill",
    "energy":      0.38,
    "valence":     0.58,
    "acousticness": 0.80,
}

DEEP_INTENSE_ROCK = {
    "name":        "Deep Intense Rock",
    "genre":       "rock",
    "mood":        "intense",
    "energy":      0.92,
    "valence":     0.40,
    "acousticness": 0.08,
}

# --- adversarial / edge case profiles ---
CONFLICTING_SAD_ENERGY = {
    "name":        "Edge Case: High Energy + Sad Mood",
    "genre":       "blues",
    "mood":        "sad",
    "energy":      0.90,   # blues catalog songs are low energy — high energy conflicts with sad/blues
    "valence":     0.20,
    "acousticness": 0.50,
}

GENRE_DOESNT_EXIST = {
    "name":        "Edge Case: Unknown Genre",
    "genre":       "bossa nova",   # not in catalog or any group
    "mood":        "relaxed",
    "energy":      0.45,
    "valence":     0.65,
    "acousticness": 0.70,
}

ALL_MIDPOINT = {
    "name":        "Edge Case: All 0.5 (no strong preference)",
    "genre":       "pop",
    "mood":        "moody",
    "energy":      0.50,
    "valence":     0.50,
    "acousticness": 0.50,
}


def run_profile(profile, songs, k=5):
    name = profile.pop("name")
    print(f"\nProfile: {name}")
    print(f"Prefs:   {profile}")
    print("-" * 55)
    recommendations = recommend_songs(profile, songs, k=k)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"  #{rank}  {song['title']} by {song['artist']}")
        print(f"       Genre: {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}")
        print(f"       Score: {score:.2f}  |  Why: {explanation}")
    profile["name"] = name  # restore so profile dict stays intact


def main() -> None:
    songs = load_songs("data/songs.csv")

    print("\n" + "=" * 55)
    print("  STANDARD PROFILES")
    print("=" * 55)
    run_profile(HIGH_ENERGY_POP,   songs)
    run_profile(CHILL_LOFI,        songs)
    run_profile(DEEP_INTENSE_ROCK, songs)

    print("\n" + "=" * 55)
    print("  ADVERSARIAL / EDGE CASE PROFILES")
    print("=" * 55)
    run_profile(CONFLICTING_SAD_ENERGY, songs)
    run_profile(GENRE_DOESNT_EXIST,     songs)
    run_profile(ALL_MIDPOINT,           songs)


if __name__ == "__main__":
    main()
