from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

GENRE_GROUPS = {
    "chill":      ["lofi", "ambient", "classical"],
    "electronic": ["synthwave", "edm", "pop"],
    "organic":    ["folk", "country", "blues", "jazz", "r&b"],
    "energetic":  ["rock", "hip-hop", "funk", "indie pop"],
}

MOOD_GROUPS = {
    "low_energy":  ["chill", "melancholic", "sad", "relaxed"],
    "mid_energy":  ["focused", "nostalgic", "romantic", "moody"],
    "high_energy": ["happy", "upbeat", "intense", "euphoric", "playful"],
}

def _get_group(value: str, groups: Dict) -> Optional[str]:
    """Returns the group name for a given value, or None if not found."""
    for group, members in groups.items():
        if value in members:
            return group
    return None

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
    """Reads songs.csv and returns a list of dicts with numeric fields cast to float/int."""
    import csv
    songs = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a song against user preferences and returns a (score, reasons) tuple."""
    score = 0.0
    reasons = []

    # --- categorical ---
    user_genre = user_prefs.get("genre")
    song_genre  = song["genre"]
    if song_genre == user_genre:
        score += 2.0
        reasons.append("genre match (+2.0)")
    elif _get_group(song_genre, GENRE_GROUPS) == _get_group(user_genre, GENRE_GROUPS):
        score += 1.0
        reasons.append(f"similar genre to {user_genre} (+1.0)")

    user_mood = user_prefs.get("mood")
    song_mood  = song["mood"]
    if song_mood == user_mood:
        score += 1.0
        reasons.append("mood match (+1.0)")
    elif _get_group(song_mood, MOOD_GROUPS) == _get_group(user_mood, MOOD_GROUPS):
        score += 0.5
        reasons.append(f"similar mood to {user_mood} (+0.5)")

    # --- numerical ---
    if "energy" in user_prefs:
        energy_score = (1 - abs(user_prefs["energy"] - song["energy"])) * 1.5
        score += energy_score
        reasons.append(f"energy score {song['energy']:.2f} (+{energy_score:.2f})")

    if "valence" in user_prefs:
        valence_score = (1 - abs(user_prefs["valence"] - song["valence"])) * 1.0
        score += valence_score
        reasons.append(f"valence score {song['valence']:.2f} (+{valence_score:.2f})")

    if "acousticness" in user_prefs:
        acousticness_score = (1 - abs(user_prefs["acousticness"] - song["acousticness"])) * 0.5
        score += acousticness_score
        reasons.append(f"acousticness score {song['acousticness']:.2f} (+{acousticness_score:.2f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores every song in the catalog, sorts by score descending, and returns the top k."""
    # Judge every song, sort highest to lowest, return top k
    scored = [
        (song, score, ", ".join(reasons) if reasons else "no strong match")
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]
    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]
