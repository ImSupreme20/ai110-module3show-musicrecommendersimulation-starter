import csv
from typing import List, Dict, Tuple, Optional, Callable
from dataclasses import dataclass
from enum import Enum

class ScoringMode(Enum):
    """Different scoring strategies for recommendations."""
    BALANCED = "balanced"          # Genre + Mood + Energy
    GENRE_FIRST = "genre_first"    # Heavy weight on genre
    MOOD_FIRST = "mood_first"      # Heavy weight on mood
    ENERGY_FOCUSED = "energy_focused"  # Focus on energy matching
    POPULARITY_DRIVEN = "popularity_driven"  # Consider popularity score

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
    popularity: int = 50
    release_decade: int = 2020
    mood_tags: str = ""

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
    target_valence: float = 0.5
    target_danceability: float = 0.5
    preferred_decades: List[int] = None
    preferred_mood_tags: List[str] = None

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song], scoring_mode: ScoringMode = ScoringMode.BALANCED):
        self.songs = songs
        self.scoring_mode = scoring_mode
        self.seen_artists = set()  # Track artists for diversity penalty

    def recommend(self, user: UserProfile, k: int = 5, apply_diversity: bool = False) -> List[Tuple[Song, float, List[str]]]:
        """Generate recommendations with optional diversity penalty."""
        scored_songs = []
        self.seen_artists = set()  # Reset for new recommendation run
        
        for song in self.songs:
            score, reasons = self.score_song(user, song, apply_diversity)
            scored_songs.append((song, score, reasons))
        
        # Sort by score descending
        scored_songs.sort(key=lambda x: x[1], reverse=True)
        return scored_songs[:k]

    def score_song(self, user: UserProfile, song: Song, apply_diversity: bool = False) -> Tuple[float, List[str]]:
        """Score a single song using the configured scoring mode."""
        if self.scoring_mode == ScoringMode.GENRE_FIRST:
            return self._score_genre_first(user, song, apply_diversity)
        elif self.scoring_mode == ScoringMode.MOOD_FIRST:
            return self._score_mood_first(user, song, apply_diversity)
        elif self.scoring_mode == ScoringMode.ENERGY_FOCUSED:
            return self._score_energy_focused(user, song, apply_diversity)
        elif self.scoring_mode == ScoringMode.POPULARITY_DRIVEN:
            return self._score_popularity_driven(user, song, apply_diversity)
        else:  # BALANCED
            return self._score_balanced(user, song, apply_diversity)

    def _score_balanced(self, user: UserProfile, song: Song, apply_diversity: bool = False) -> Tuple[float, List[str]]:
        """Balanced scoring: Genre (2.0) + Mood (1.5) + Energy (1.5) + Acoustic (1.0)."""
        score = 0.0
        reasons = []

        # Genre match: +2.0 points
        if song.genre.lower() == user.favorite_genre.lower():
            score += 2.0
            reasons.append(f"Genre match: {song.genre} (+2.0)")
        
        # Mood match: +1.5 points
        if song.mood.lower() == user.favorite_mood.lower():
            score += 1.5
            reasons.append(f"Mood match: {song.mood} (+1.5)")
        
        # Energy similarity: 0 to 1.5 points based on distance
        energy_diff = abs(song.energy - user.target_energy)
        energy_score = max(0, 1.5 - (energy_diff * 1.5))
        score += energy_score
        reasons.append(f"Energy similarity (+{energy_score:.2f})")
        
        # Acoustic preference: +1.0 if matches
        if user.likes_acoustic and song.acousticness > 0.5:
            score += 1.0
            reasons.append(f"High acousticness (+1.0)")
        elif not user.likes_acoustic and song.acousticness < 0.5:
            score += 0.5
            reasons.append(f"Low acousticness preference met (+0.5)")
        
        # Valence bonus: 0 to 0.5 points
        valence_diff = abs(song.valence - user.target_valence)
        valence_score = max(0, 0.5 - (valence_diff * 0.5))
        score += valence_score
        reasons.append(f"Valence match (+{valence_score:.2f})")
        
        # Apply diversity penalty if requested
        if apply_diversity and song.artist in self.seen_artists:
            penalty = 2.0
            score -= penalty
            reasons.append(f"Diversity penalty: artist already recommended (-{penalty:.1f})")
        else:
            self.seen_artists.add(song.artist)
        
        return score, reasons

    def _score_genre_first(self, user: UserProfile, song: Song, apply_diversity: bool = False) -> Tuple[float, List[str]]:
        """Genre-first: Heavy weight on genre matching."""
        score = 0.0
        reasons = []

        if song.genre.lower() == user.favorite_genre.lower():
            score += 4.0
            reasons.append(f"Genre match: {song.genre} (+4.0)")
        else:
            score -= 1.0
            reasons.append(f"Genre mismatch (-1.0)")
        
        if song.mood.lower() == user.favorite_mood.lower():
            score += 1.0
            reasons.append(f"Mood match: {song.mood} (+1.0)")
        
        energy_diff = abs(song.energy - user.target_energy)
        energy_score = max(0, 1.0 - (energy_diff * 1.0))
        score += energy_score
        reasons.append(f"Energy similarity (+{energy_score:.2f})")
        
        if apply_diversity and song.artist in self.seen_artists:
            penalty = 2.0
            score -= penalty
            reasons.append(f"Diversity penalty (-{penalty:.1f})")
        else:
            self.seen_artists.add(song.artist)
        
        return max(0, score), reasons

    def _score_mood_first(self, user: UserProfile, song: Song, apply_diversity: bool = False) -> Tuple[float, List[str]]:
        """Mood-first: Heavy weight on mood matching."""
        score = 0.0
        reasons = []

        if song.mood.lower() == user.favorite_mood.lower():
            score += 4.0
            reasons.append(f"Mood match: {song.mood} (+4.0)")
        else:
            score -= 0.5
            reasons.append(f"Mood mismatch (-0.5)")
        
        if song.genre.lower() == user.favorite_genre.lower():
            score += 1.5
            reasons.append(f"Genre match: {song.genre} (+1.5)")
        
        energy_diff = abs(song.energy - user.target_energy)
        energy_score = max(0, 1.0 - (energy_diff * 1.0))
        score += energy_score
        reasons.append(f"Energy similarity (+{energy_score:.2f})")
        
        if apply_diversity and song.artist in self.seen_artists:
            penalty = 2.0
            score -= penalty
            reasons.append(f"Diversity penalty (-{penalty:.1f})")
        else:
            self.seen_artists.add(song.artist)
        
        return max(0, score), reasons

    def _score_energy_focused(self, user: UserProfile, song: Song, apply_diversity: bool = False) -> Tuple[float, List[str]]:
        """Energy-focused: Heavy weight on energy matching."""
        score = 0.0
        reasons = []

        # Energy is primary factor
        energy_diff = abs(song.energy - user.target_energy)
        energy_score = max(0, 3.0 - (energy_diff * 3.0))
        score += energy_score
        reasons.append(f"Energy match (+{energy_score:.2f})")
        
        if song.mood.lower() == user.favorite_mood.lower():
            score += 1.0
            reasons.append(f"Mood match: {song.mood} (+1.0)")
        
        if song.genre.lower() == user.favorite_genre.lower():
            score += 1.0
            reasons.append(f"Genre match: {song.genre} (+1.0)")
        
        danceability_score = abs(song.danceability - user.target_danceability) * 0.5
        score += danceability_score
        reasons.append(f"Danceability match (+{danceability_score:.2f})")
        
        if apply_diversity and song.artist in self.seen_artists:
            penalty = 2.0
            score -= penalty
            reasons.append(f"Diversity penalty (-{penalty:.1f})")
        else:
            self.seen_artists.add(song.artist)
        
        return max(0, score), reasons

    def _score_popularity_driven(self, user: UserProfile, song: Song, apply_diversity: bool = False) -> Tuple[float, List[str]]:
        """Popularity-driven: Factors in song popularity."""
        score = 0.0
        reasons = []

        # Popularity boost: 0 to 2.0 points
        popularity_score = (song.popularity / 100.0) * 2.0
        score += popularity_score
        reasons.append(f"Popularity score ({song.popularity}/100) (+{popularity_score:.2f})")
        
        if song.genre.lower() == user.favorite_genre.lower():
            score += 1.5
            reasons.append(f"Genre match: {song.genre} (+1.5)")
        
        if song.mood.lower() == user.favorite_mood.lower():
            score += 1.5
            reasons.append(f"Mood match: {song.mood} (+1.5)")
        
        energy_diff = abs(song.energy - user.target_energy)
        energy_score = max(0, 1.0 - (energy_diff * 1.0))
        score += energy_score
        reasons.append(f"Energy similarity (+{energy_score:.2f})")
        
        if apply_diversity and song.artist in self.seen_artists:
            penalty = 2.0
            score -= penalty
            reasons.append(f"Diversity penalty (-{penalty:.1f})")
        else:
            self.seen_artists.add(song.artist)
        
        return max(0, score), reasons

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain why a song was recommended."""
        score, reasons = self.score_song(user, song)
        return f"Score: {score:.2f}\n" + "\n".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file and returns Song objects.
    Required by src/main.py
    """
    songs = []
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                song = Song(
                    id=int(row['id']),
                    title=row['title'],
                    artist=row['artist'],
                    genre=row['genre'],
                    mood=row['mood'],
                    energy=float(row['energy']),
                    tempo_bpm=float(row['tempo_bpm']),
                    valence=float(row['valence']),
                    danceability=float(row['danceability']),
                    acousticness=float(row['acousticness']),
                    popularity=int(row.get('popularity', 50)),
                    release_decade=int(row.get('release_decade', 2020)),
                    mood_tags=row.get('mood_tags', '')
                )
                songs.append(song)
    except FileNotFoundError:
        print(f"Error: Could not find {csv_path}")
        return []
    except Exception as e:
        print(f"Error loading songs: {e}")
        return []
    
    print(f"[+] Loaded {len(songs)} songs from {csv_path}")
    return songs

def score_song(user_prefs: Dict, song: Dict, mode: ScoringMode = ScoringMode.BALANCED) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences (functional version).
    Expected return format: (score, reasons)
    """
    score = 0.0
    reasons = []

    # Genre match: +2.0 points
    if song.get('genre', '').lower() == user_prefs.get('genre', '').lower():
        score += 2.0
        reasons.append(f"Genre match: {song.get('genre')} (+2.0)")
    
    # Mood match: +1.5 points
    if song.get('mood', '').lower() == user_prefs.get('mood', '').lower():
        score += 1.5
        reasons.append(f"Mood match: {song.get('mood')} (+1.5)")
    
    # Energy similarity: 0 to 1.5 points
    try:
        energy_diff = abs(float(song.get('energy', 0.5)) - user_prefs.get('energy', 0.5))
        energy_score = max(0, 1.5 - (energy_diff * 1.5))
        score += energy_score
        reasons.append(f"Energy similarity (+{energy_score:.2f})")
    except (ValueError, TypeError):
        pass
    
    # Acoustic preference: +1.0 if matches
    acoustic_pref = user_prefs.get('likes_acoustic', False)
    acousticness = float(song.get('acousticness', 0.5))
    if acoustic_pref and acousticness > 0.5:
        score += 1.0
        reasons.append(f"High acousticness preference met (+1.0)")
    elif not acoustic_pref and acousticness < 0.5:
        score += 0.5
        reasons.append(f"Low acousticness preference met (+0.5)")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Song], k: int = 5, 
                   scoring_mode: ScoringMode = ScoringMode.BALANCED,
                   apply_diversity: bool = False) -> List[Tuple[Dict, float, List[str]]]:
    """
    Functional implementation of the recommendation logic.
    Expected return format: (song_dict, score, explanation_reasons)
    """
    recommender = Recommender(songs, scoring_mode)
    recommendations = []
    
    # Convert user_prefs dict to UserProfile if needed
    if isinstance(user_prefs, dict):
        user_profile = UserProfile(
            favorite_genre=user_prefs.get('genre', 'pop'),
            favorite_mood=user_prefs.get('mood', 'happy'),
            target_energy=user_prefs.get('energy', 0.5),
            likes_acoustic=user_prefs.get('likes_acoustic', False),
            target_valence=user_prefs.get('valence', 0.5),
            target_danceability=user_prefs.get('danceability', 0.5)
        )
    else:
        user_profile = user_prefs
    
    scored_songs = recommender.recommend(user_profile, k, apply_diversity)
    
    # Convert Song objects back to dicts for compatibility
    for song, score, reasons in scored_songs:
        song_dict = {
            'id': song.id,
            'title': song.title,
            'artist': song.artist,
            'genre': song.genre,
            'mood': song.mood,
            'energy': song.energy,
            'tempo_bpm': song.tempo_bpm,
            'valence': song.valence,
            'danceability': song.danceability,
            'acousticness': song.acousticness,
            'popularity': song.popularity,
            'release_decade': song.release_decade,
            'mood_tags': song.mood_tags
        }
        recommendations.append((song_dict, score, reasons))
    
    return recommendations
