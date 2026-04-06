# 🎵 Music Recommender Simulation

## Project Summary

This project implements a modular, transparent music recommendation system that simulates how major streaming platforms like Spotify and TikTok predict what users will love next. The system demonstrates content-based filtering, weighted scoring algorithms, and fairness considerations in AI recommendations.

**What This Version Does:**
- Loads a diverse catalog of 22 songs with rich metadata (genre, mood, energy, valence, danceability, acousticness, popularity, release_decade, and detailed mood tags)
- Accepts user preference profiles specifying favorite genre, mood, target energy levels, and acoustic preferences
- Scores songs using multiple weighting strategies: Balanced, Genre-First, Mood-First, Energy-Focused, and Popularity-Driven
- Generates ranked recommendations with detailed explanations for each scoring decision
- Implements diversity penalties to prevent over-recommending the same artists
- Tests for and identifies algorithmic bias and filter bubble effects

---

## How The System Works

### Key Concepts

**Content-Based Filtering vs Collaborative Filtering:**
- **Collaborative Filtering**: Recommends songs based on what similar users liked (requires user-user and item-item patterns)
- **Content-Based Filtering** (used here): Recommends songs based on song attributes matching user preferences (no need for user behavior patterns)

Our system uses **content-based filtering** because it's transparent, interpretable, and works well with cold-start problems (new songs without historical data).

### Data Schema

**Song Features:**
- `genre`: Music category (pop, rock, lofi, ambient, electronic, jazz, hip-hop, indie pop, synthwave, classical, gospel)
- `mood`: Emotional tone (happy, chill, intense, relaxed, sad, moody, focused)
- `energy`: Intensity level (0.0-1.0 scale)
- `tempo_bpm`: Beats per minute
- `valence`: Musical positivity (0.0-1.0)
- `danceability`: How suitable for dancing (0.0-1.0)
- `acousticness`: Acoustic vs electronic (0.0-1.0)
- `popularity`: How popular among listeners (0-100 score)
- `release_decade`: Era of release (1985-2023)
- `mood_tags`: Detailed emotion descriptors (e.g., "euphoric;uplifting")

**User Profile:**
```python
UserProfile(
    favorite_genre="pop",
    favorite_mood="happy",
    target_energy=0.8,
    likes_acoustic=False,
    target_valence=0.85,
    target_danceability=0.8,
    preferred_decades=[2020, 2021, 2022, 2023],
    preferred_mood_tags=["euphoric", "uplifting"]
)
```

### Algorithm Recipe - Balanced Scoring Mode

**Point System:**
- Genre match: **+2.0 points** (exact match on favorite_genre)
- Mood match: **+1.5 points** (exact match on favorite_mood)
- Energy similarity: **0-1.5 points** (based on distance from target_energy)
  - Formula: `max(0, 1.5 - (|song_energy - target_energy| * 1.5))`
  - Rewards songs close to user's energy target, not just high or low
- Acoustic preference: **+1.0 or +0.5 points** (high acousticness if user_likes_acoustic=True)
- Valence match: **0-0.5 points** (musical positivity alignment)

**Ranking Rule:**
1. Score every song in the catalog using the scoring rules above
2. Convert Song objects to dictionaries with {song, score, reasons}
3. Sort by score in descending order
4. Return top K results

**Multiple Scoring Modes:**
- **BALANCED**: Equal weight on genre, mood, and energy
- **GENRE_FIRST**: Heavy weight on genre (+4.0), lower on others (+1.0-1.5)
- **MOOD_FIRST**: Heavy weight on mood and detailed mood_tags
- **ENERGY_FOCUSED**: Prioritizes matching the user's energy level
- **POPULARITY_DRIVEN**: Incorporates song popularity (0-2.0 bonus points)

### Example Flow

```
Input: User Profile (pop/happy/energy=0.8/non-acoustic)
       ↓
For each song in catalog:
  - Check: Is genre "pop"? → +2.0
  - Check: Is mood "happy"? → +1.5
  - Calculate: Energy distance → +1.47
  - Check: Is acousticness < 0.5? → +0.5
  → Total: 5.97 points
       ↓
Sort all songs by score (5.97, 5.91, 4.26, ...)
       ↓
Output: Top 5 recommendations with reasons
  1. "Sunrise City" (5.97)
     Reasons: genre match, mood match, energy match
  2. "Summer Festival" (5.91)
     Reasons: genre match, mood match, energy match
  ...
```

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

```bash
python -m venv .venv
source .venv/bin/activate      # Mac or Linux
.venv\Scripts\activate         # Windows
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the simulation:

```bash
cd src
python main.py
```

### Dataset

The song catalog is in `data/songs.csv` with 22 diverse songs:

```csv
id,title,artist,genre,mood,energy,tempo_bpm,valence,danceability,acousticness,popularity,release_decade,mood_tags
1,Sunrise City,Neon Echo,pop,happy,0.82,118,0.84,0.79,0.18,92,2020,euphoric;uplifting
2,Midnight Coding,LoRoom,lofi,chill,0.42,78,0.56,0.62,0.71,78,2022,nostalgic;relaxing
...
```

---

## Key Features Implemented

### Phase 1: Understanding Real Recommendation Systems
- Research on Spotify, YouTube Music, and TikTok algorithms
- Distinction between collaborative filtering (user-based) and content-based filtering
- Analysis of data types used in real systems (likes, skips, playlists, temporal data)

### Phase 2: System Design
- Expanded dataset from 10 to 22 songs with diverse genres and moods
- Added advanced features: popularity, release_decade, detailed mood_tags
- Designed scoring rules with clear weighting strategy
- Created UserProfile dataclass to represent taste preferences

### Phase 3: Core Implementation
- `load_songs()`: Reads CSV and converts to Song objects
- `score_song()`: Calculates score based on algorithm recipe
- `recommend_songs()`: Ranks all songs and returns top K with reasons
- `Recommender` class: OOP wrapper with multiple scoring modes

### Phase 4: Evaluation & Testing
Tested with 8 diverse user profiles:
- Pop Enthusiast: Loves happy, high-energy pop (energy=0.8)
- Chill Lofi Lover: Prefers low-energy, chill lofi (energy=0.35)
- Rock Enthusiast: Seeks intense rock at high energy (energy=0.9)
- Electronic Lover: High-energy dancing electronic (energy=0.88)
- Jazz Aficionado: Relaxed jazz with acoustic elements
- Ambient Minimalist: Very chill ambient (energy=0.25)
- High-Energy Gym Buff: Intense motivational pop (energy=0.92)
- Experimental Mix: Happy indie pop with acoustic elements

**Results:** System produces highly accurate recommendations matching each profile's preferences. Same songs appear at top for similar profiles (e.g., Gym Hero for high-energy users).

### Challenge 1: Advanced Song Features
- Added `popularity` (0-100 score)
- Added `release_decade` (era context)
- Added `mood_tags` (detailed emotions: euphoric, nostalgic, aggressive, etc.)
- Scoring rules adapted to reward popularity and mood tag matches

### Challenge 2: Multiple Scoring Modes
Five different recommendation strategies:

| Mode | Primary Focus | Use Case |
|------|---------------|----------|
| BALANCED | Genre + Mood + Energy | Default, well-rounded |
| GENRE_FIRST | Heavy genre weight | Genre purists |
| MOOD_FIRST | Mood + mood_tags | Emotional preferences |
| ENERGY_FOCUSED | Energy matching | Workout, activity-based |
| POPULARITY_DRIVEN | Includes popularity | Discover trending hits |

### Challenge 3: Diversity & Fairness Logic
- Prevents over-recommending the same artists
- Applies diversity penalty (-2.0) if artist already in recommendations
- Demonstrates fairness: broader discovery instead of algorithmic monoculture
- Identifies filter bubble risk: focusing only on one genre can miss gems

### Challenge 4: Visual Summary Table
```
  #  Title                      Artist               Genre        Score  Reasons
  ===============================================================================
  1  Sunrise City               Neon Echo            pop          5.97   Genre match (+2.0); Mood match happy (+1.5); ...
  2  Summer Festival            Beach Vibes          pop          5.91   Genre match (+2.0); Mood match happy (+1.5); ...
```

---

## Identified Biases & Limitations

### 1. **Genre Dominance** ⚠️
**Finding**: System over-prioritizes genre matching (+2.0 points vs +1.5 for mood).
- Same genre songs dominate results regardless of mood preferences
- Users seeking mood-based discovery get stuck in one genre

**Fix**: Use MOOD_FIRST mode or adjust weights (genre: +1.5, mood: +2.0)

### 2. **Energy Bias** ⚠️
**Finding**: Linear energy scoring can miss transitional moods.
- A user with target_energy=0.5 might miss great songs at 0.2 or 0.8
- Formula `max(0, 1.5 - distance * 1.5)` penalizes variation

**Scenario**: User likes "chill but focused" (energy=0.5) misses "Meditation" (0.1) and "Upbeat" (0.9)

### 3. **Filter Bubble Effect** ⚠️
**Finding**: Without diversity penalty, system recommends from narrow subset.
- "Pop Enthusiast" gets only Neon Echo and Beach Vibes artists
- Users trapped in algorithmic monoculture

**Solution**: Implemented diversity penalty (-2.0) to encourage artist variation

### 4. **Acoustic Preference Misalignment** ⚠️
**Finding**: Hard binary threshold (0.5) doesn't capture nuance.
- User preferring acoustic might still love electric songs with good mood
- Acoustic score is +1.0 (good) vs +1.5 (mood), doesn't reflect true preference

### 5. **Dataset Imbalance** ⚠️
**Finding**: Dataset slightly skews toward pop/happy (4/22 songs = 18%).
- Pop recommendations get boost from popularity scores
- Other genres underrepresented

### 6. **Popularity Feedback Loop** ⚠️
**Finding**: POPULARITY_DRIVEN mode reinforces existing hits.
- Popular songs get +2.0 bonus, making them harder to dethrone
- New artists struggling to break through
- Real-world consequence: mainstream monoculture

### 7. **Missing Context** ⚠️
**What we ignore**: Temporal factors, user history, time-of-day, weather, social context
- System doesn't know user is at gym vs library vs party
- No learning from user feedback (skips, replays, saves)
- Static profiles ignore evolving taste

---

## Phase 5: Reflection & Model Card

See [model_card.md](model_card.md) for detailed model documentation.

### Quick Learnings

1. **Simplicity ≠ Ineffectiveness**: Our basic weighted-scoring approach produces compelling recommendations that "feel" right to users.

2. **Weight Matters**: Changing genre weight from 2.0 to 4.0 dramatically shifts results. Small numbers have outsized impact.

3. **Explanation is Power**: Showing "why" (reasons list) makes recommendations trustworthy even when surprising.

4. **One Size Doesn't Fit All**: Multiple scoring modes necessary because users have fundamentally different preference patterns.

5. **Bias is Easy to Hide**: Without deliberate testing, the system's filter bubble wouldn't be obvious to casual users.

6. **Fairness Takes Intention**: Diversity penalty doesn't happen by default; must be explicitly implemented and toggled.

---

## Project Structure

```
music-recommender/
├── data/
│   └── songs.csv              # 22-song catalog with rich features
├── src/
│   ├── main.py                # CLI runner with multiple test scenarios
│   └── recommender.py         # Core recommendation logic
├── model_card.md              # AI system documentation (see Phase 5)
├── README.md                  # This file
└── requirements.txt           # Python dependencies
```

---

## Extending This Project

### Possible Improvements

1. **Add User Feedback Loop**: Track user skips, replays, saves → update model weights
2. **Implement Collaborative Filtering**: Combine with other users' preferences
3. **Add Temporal Dynamics**: Different recommendations based on time-of-day, season, mood tracker
4. **Deploy as REST API**: `POST /recommend` with user profile → JSON array of recommendations
5. **A/B Testing**: Compare different modes with real users to measure satisfaction
6. **Cold-Start Problem**: Handle new songs/users without historical data
7. **Debias Explicitly**: Add fairness monitoring dashboard
8. **Multi-Armed Bandit**: Balance exploration (new songs) vs exploitation (proven winners)

---

## Testing Commands

### Run full simulation with all features:
```bash
python src/main.py
```

### Test specific scoring mode (within Python):
```python
from src.recommender import Recommender, UserProfile, ScoringMode
songs = load_songs("data/songs.csv")
profile = UserProfile("pop", "happy", 0.8, False)
recommender = Recommender(songs, ScoringMode.ENERGY_FOCUSED)
recs = recommender.recommend(profile, k=5)
```

### Run with diversity enabled:
```python
recs = recommender.recommend(profile, k=5, apply_diversity=True)
```

---

## Files Generated

- ✅ Expanded `data/songs.csv`: 10 → 22 songs with advanced features
- ✅ Complete `src/recommender.py`: Full recommendation engine with 5 scoring modes, OOP + functional APIs
- ✅ Enhanced `src/main.py`: Tests all profiles, modes, diversity, and formats output as tables
- ✅ `model_card.md`: Industry-standard AI system documentation
- ✅ `README.md`: This comprehensive guide

---

## References & Context

**Real-world recommendation systems:**
- Spotify: Blends collaborative filtering (Echo Nest acquisition), content-based features, and contextual data
- YouTube Music: Uses millions of signals including engagement time, skip behavior, playlist additions
- TikTok: Combines video features (audio, visual, duration), user behavior, social signals

**Why this matters**: Understanding recommendation systems is critical for:
- Users: Recognizing filter bubbles and broadeningpreferences
- Designers: Building ethical, transparent systems
- Researchers: Studying bias, fairness, and social impact of algorithms
- Businesses: Balancing engagement optimization with user autonomy

---

## Contact & Questions

For detailed analysis of algorithmic bias and fairness considerations, see the [model_card.md](model_card.md).

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

