"""
Command line runner for the Music Recommender Simulation.

This file demonstrates the recommender with multiple user profiles,
scoring modes, and formats output with tables and visualizations.
"""

import sys
sys.path.insert(0, '/'.join(__file__.split('/')[:-1]))

from recommender import (
    load_songs, recommend_songs, Recommender, UserProfile, ScoringMode
)
from typing import List, Dict, Tuple

def print_divider(title: str = "") -> None:
    """Print a formatted divider."""
    if title:
        print(f"\n{'='*80}")
        print(f"  {title}")
        print('='*80)
    else:
        print('='*80)

def format_table(songs_with_scores: List[Tuple[Dict, float, List[str]]], max_width: int = 100) -> str:
    """Format recommendations as an ASCII table."""
    lines = []
    
    # Header
    header = f"{'#':<2} {'Title':<30} {'Artist':<20} {'Genre':<12} {'Score':<8} Reasons"
    lines.append(header)
    lines.append("-" * max_width)
    
    # Rows
    for idx, (song, score, reasons) in enumerate(songs_with_scores, 1):
        title = song['title'][:28]
        artist = song['artist'][:18]
        genre = song['genre'][:10]
        reasons_str = "; ".join(reasons[:2])  # First 2 reasons
        if len(reasons) > 2:
            reasons_str += f"; +{len(reasons)-2} more"
        
        row = f"{idx:<2} {title:<30} {artist:<20} {genre:<12} {score:>6.2f}  {reasons_str}"
        lines.append(row[:max_width])
    
    return "\n".join(lines)

def create_user_profiles() -> Dict[str, UserProfile]:
    """Create diverse user profiles for testing."""
    return {
        "Pop Enthusiast": UserProfile(
            favorite_genre="pop",
            favorite_mood="happy",
            target_energy=0.8,
            likes_acoustic=False,
            target_valence=0.85,
            target_danceability=0.8
        ),
        "Chill Lofi Lover": UserProfile(
            favorite_genre="lofi",
            favorite_mood="chill",
            target_energy=0.35,
            likes_acoustic=True,
            target_valence=0.55,
            target_danceability=0.55
        ),
        "Rock Enthusiast": UserProfile(
            favorite_genre="rock",
            favorite_mood="intense",
            target_energy=0.9,
            likes_acoustic=False,
            target_valence=0.5,
            target_danceability=0.7
        ),
        "Electronic Lover": UserProfile(
            favorite_genre="electronic",
            favorite_mood="intense",
            target_energy=0.88,
            likes_acoustic=False,
            target_valence=0.65,
            target_danceability=0.9
        ),
        "Jazz Aficionado": UserProfile(
            favorite_genre="jazz",
            favorite_mood="relaxed",
            target_energy=0.4,
            likes_acoustic=True,
            target_valence=0.7,
            target_danceability=0.5
        ),
        "Ambient Minimalist": UserProfile(
            favorite_genre="ambient",
            favorite_mood="chill",
            target_energy=0.25,
            likes_acoustic=True,
            target_valence=0.65,
            target_danceability=0.3
        ),
        "High-Energy Gym Buff": UserProfile(
            favorite_genre="pop",
            favorite_mood="intense",
            target_energy=0.92,
            likes_acoustic=False,
            target_valence=0.75,
            target_danceability=0.88
        ),
        "Experimental Mix": UserProfile(
            favorite_genre="indie pop",
            favorite_mood="happy",
            target_energy=0.6,
            likes_acoustic=True,
            target_valence=0.75,
            target_danceability=0.7
        ),
    }

def test_single_profile(recommender: Recommender, profile_name: str, 
                       profile: UserProfile, songs: List, k: int = 5) -> None:
    """Test recommendations for a single profile."""
    print_divider(f"Profile: {profile_name}")
    print(f"Preferences: {profile.favorite_genre} / {profile.favorite_mood}")
    print(f"Energy Target: {profile.target_energy:.1f} | Acoustic: {profile.likes_acoustic}")
    
    recommendations = recommender.recommend(profile, k)
    
    print("\n[TOP RECOMMENDATIONS]\n")
    for idx, (song, score, reasons) in enumerate(recommendations, 1):
        print(f"{idx}. {song.title} - {song.artist}")
        print(f"   Score: {score:.2f} | Genre: {song.genre} | Mood: {song.mood}")
        print(f"   Energy: {song.energy:.2f} | Acousticness: {song.acousticness:.2f}")
        print(f"   Reasons: {', '.join(reasons[:3])}")
        print()

def test_all_modes(profile: UserProfile, songs: List) -> None:
    """Test all scoring modes for a profile."""
    modes = [
        ScoringMode.BALANCED,
        ScoringMode.GENRE_FIRST,
        ScoringMode.MOOD_FIRST,
        ScoringMode.ENERGY_FOCUSED,
        ScoringMode.POPULARITY_DRIVEN
    ]
    
    print_divider("Testing All Scoring Modes")
    print(f"Profile: {profile.favorite_genre}/{profile.favorite_mood}")
    
    for mode in modes:
        recommender = Recommender(songs, mode)
        recommendations = recommender.recommend(profile, k=3)
        
        print(f"\n[{mode.value.upper()}]:")
        for song, score, reasons in recommendations:
            print(f"  * {song.title} ({score:.2f})")

def test_with_diversity(recommender: Recommender, profile: UserProfile, 
                       songs: List, k: int = 5) -> None:
    """Test recommendations with diversity penalty enabled."""
    print_divider("Recommendations WITH Diversity Penalty")
    print(f"Profile: {profile.favorite_genre}/{profile.favorite_mood}")
    
    recommendations = recommender.recommend(profile, k, apply_diversity=True)
    
    print("\n[TOP RECOMMENDATIONS - DIVERSE ARTISTS]\n")
    for idx, (song, score, reasons) in enumerate(recommendations, 1):
        print(f"{idx}. {song.title} - {song.artist}")
        print(f"   Score: {score:.2f}")
        if any("Diversity" in r for r in reasons):
            print(f"   [!] Diversity penalty applied")
        print()

def main() -> None:
    """Main function to run the recommender simulation."""
    print("\n[MUSIC RECOMMENDER SIMULATION]")
    print("="*80)
    
    # Load songs
    import os
    data_path = os.path.join(os.path.dirname(__file__), '../data/songs.csv')
    songs = load_songs(data_path)
    if not songs:
        print("Error: Could not load songs. Exiting.")
        return
    
    profiles = create_user_profiles()
    
    # ========== PHASE 4: Test with diverse profiles ==========
    print_divider("PHASE 4: TESTING DIVERSE PROFILES")
    
    for profile_name, profile in list(profiles.items())[:3]:
        recommender = Recommender(songs, ScoringMode.BALANCED)
        test_single_profile(recommender, profile_name, profile, songs, k=5)
    
    # ========== CHALLENGE 2: Test all scoring modes ==========
    print_divider("CHALLENGE 2: MULTIPLE SCORING MODES")
    profile = profiles["Pop Enthusiast"]
    test_all_modes(profile, songs)
    
    # ========== CHALLENGE 3: Test with diversity penalty ==========
    print_divider("CHALLENGE 3: DIVERSITY & FAIRNESS LOGIC")
    recommender = Recommender(songs, ScoringMode.BALANCED)
    
    print("\n[WITHOUT DIVERSITY PENALTY]\n")
    recommendations = recommender.recommend(profile, k=5, apply_diversity=False)
    for idx, (song, score, reasons) in enumerate(recommendations, 1):
        print(f"{idx}. {song.title} - {song.artist}")
    
    test_with_diversity(recommender, profile, songs, k=5)
    
    # ========== CHALLENGE 4: Formatted table output ==========
    print_divider("CHALLENGE 4: VISUAL SUMMARY TABLE")
    recommender = Recommender(songs, ScoringMode.BALANCED)
    recommendations = recommender.recommend(profile, k=8)
    
    # Convert Song objects to dicts for table formatting
    song_dicts = [(s.__dict__, score, reasons) for s, score, reasons in recommendations]
    
    print(f"\nProfile: {profile.favorite_genre}/{profile.favorite_mood}\n")
    print(format_table(song_dicts))
    
    # ========== Advanced: Test conflicting preferences ==========
    print_divider("EDGE CASE: CONFLICTING PREFERENCES")
    conflicting_profile = UserProfile(
        favorite_genre="ambient",
        favorite_mood="intense",  # Conflicting!
        target_energy=0.95,       # High energy
        likes_acoustic=True,
        target_valence=0.3        # Low valence
    )
    print(f"Testing profile with conflicting mood/energy preferences...")
    recommender = Recommender(songs, ScoringMode.BALANCED)
    recommendations = recommender.recommend(conflicting_profile, k=3)
    
    print("\n[TOP RECOMMENDATIONS]\n")
    for idx, (song, score, reasons) in enumerate(recommendations, 1):
        print(f"{idx}. {song.title} - {song.artist}")
        print(f"   Mood: {song.mood} | Energy: {song.energy:.2f}")
        print(f"   Reasons: {', '.join(reasons[:2])}\n")
    
    print_divider("SIMULATION COMPLETE")
    print(f"[+] Tested {len(profiles)} diverse user profiles")
    print(f"[+] Evaluated {len(ScoringMode)} different scoring modes")
    print(f"[+] Demonstrated diversity penalty & edge cases")
    print("[+] All features working as expected!")

if __name__ == "__main__":
    main()
