# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

VibeMatch is a small, explainable music recommender. It loads a 20-song CSV, compares every song to a listener's favorite genre, favorite mood, target energy, and acoustic taste, gives each song up to 6 points, and prints the top 5 with the reasons for each score. I tested it on six profiles, including three built to trick it, and found that exact genre and mood matches can outweigh what the listener asked for on energy.

---

## How The System Works

### How real platforms do it

Platforms like Spotify and YouTube mix two main ideas. **Collaborative filtering** predicts what you'll like from the behavior of *other* users: if people who share your listening history loved a track, it gets suggested to you, even if you can't say what the songs have in common. **Content-based filtering** looks at the *items themselves* (tempo, energy, mood, genre, lyrics) and recommends songs whose attributes resemble what you already enjoy. Real systems feed both with behavior signals such as likes, skips, saves, playlist adds, and listening or watch time. Explicit actions (a save or a playlist add) generally count for more than passive ones (a play that happened to finish), and recent activity counts for more than old activity.

### What my version does

My simulator is purely **content-based**. It has no other users to learn from, so it can't do collaborative filtering. It prioritizes, in order: a genre match, a mood match, how *close* a song's energy is to the user's target, and how well its acousticness fits the user's taste. Closeness matters more than "higher is better": a user who wants energy 0.4 should not be pushed toward a 0.93 workout track just because it has more energy.

**`Song` features** (from `data/songs.csv`)

- Used in scoring: `genre`, `mood`, `energy`, `acousticness`
- Loaded but not scored yet (candidates for experiments): `tempo_bpm`, `valence`, `danceability`
- Identifiers shown in output: `id`, `title`, `artist`

**`UserProfile` fields**

- `favorite_genre` (e.g. `"pop"`)
- `favorite_mood` (e.g. `"happy"`)
- `target_energy` (0.0 to 1.0)
- `likes_acoustic` (True/False)

### Algorithm recipe

**Scoring rule** (one song vs. one user; max 6.0 points):

| Component | Points |
|---|---|
| Genre matches `favorite_genre` | +2.0 |
| Mood matches `favorite_mood` | +1.5 |
| Energy closeness: `1.5 × (1 − abs(song.energy − target_energy))` | 0 to 1.5 |
| Acoustic fit: `acousticness` if `likes_acoustic`, else `1 − acousticness` | 0 to 1.0 |

Genre is weighted just above mood (mood is about 0.75× genre). Genre is the steadier taste and should win ties, but mood is the only label that links songs across genres (for example "intense" covers both rock and pop), so it still needs real weight. A song that matches both genre and mood (3.5 points) always beats a song that matches neither (2.5 points at most). Because most genres and moods appear on only one song, the labels only separate the top few results; everything else is ranked by the smooth energy and acousticness scores. These weights were my starting guess; the experiments below check how sensitive the rankings are to them.

**Ranking rule** (whole catalog): score every song with the scoring rule, sort by score from highest to lowest, and return the top `k`. The scoring rule can only say how good *one* song is; the ranking rule turns those separate scores into an ordered list. Each result also carries a short "because..." explanation built from the components that earned points.

**Data flow**

    Input:   user_prefs (genre, mood, energy, likes_acoustic) + data/songs.csv
    Process: for each song -> score_song(user_prefs, song) -> (score, reasons)
    Output:  sort scores high to low -> top K songs with explanations

### Known limits of this design

- A genre match is all-or-nothing, so "indie pop" earns nothing for a "pop" fan even though the two are close. The same is true of moods ("happy" vs. "euphoric").
- Genre carries the most weight, so it can crowd out good songs from other genres (a small filter bubble). For example, Gym Hero (pop, intense) can outrank a better mood match for a pop/happy listener.
- Most genres and moods appear on only one song in the 20-song catalog, so labels only boost the top few results; positions beyond that are ranked by energy and acousticness alone.
- Nothing here learns from skips or likes, so the profile never changes.

---

## Getting Started

### Setup

**1. Create a virtual environment** (optional but recommended):

    python -m venv .venv
    source .venv/bin/activate      # Mac or Linux
    .venv\Scripts\activate         # Windows

**2. Install dependencies:**

    pip install -r requirements.txt

**3. Run the app:**

    python -m src.main

### Running Tests

Run the starter tests with:

    pytest

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output for the starter pop/happy profile (energy 0.8). The current `python -m src.main` prints all six profiles; their outputs are in the experiments section below:

```text
============================================================
Profile: Pop / Happy
  genre=pop, mood=happy, energy=0.8, likes_acoustic=False
============================================================

1. Sunrise City by Neon Echo
   Score: 5.79 / 6.00
   Why:
     - genre match (+2.0)
     - mood match (+1.5)
     - energy closeness (+1.47)
     - acoustic fit (+0.82)

2. Gym Hero by Max Pulse
   Score: 4.25 / 6.00
   Why:
     - genre match (+2.0)
     - energy closeness (+1.30)
     - acoustic fit (+0.95)

3. Rooftop Lights by Indigo Parade
   Score: 3.59 / 6.00
   Why:
     - mood match (+1.5)
     - energy closeness (+1.44)
     - acoustic fit (+0.65)

4. Concrete Crown by Verse Theory
   Score: 2.35 / 6.00
   Why:
     - energy closeness (+1.47)
     - acoustic fit (+0.88)

5. Laser Horizon by Pulsewave
   Score: 2.25 / 6.00
   Why:
     - energy closeness (+1.28)
     - acoustic fit (+0.98)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

### Profile stress test (top 5 for each profile)

<!-- profile-output:start -->
### High-Energy Pop

```text
============================================================
Profile: High-Energy Pop
  genre=pop, mood=happy, energy=0.9, likes_acoustic=False
============================================================

1. Sunrise City by Neon Echo
   Score: 5.70 / 6.00
   Why:
     - genre match (+2.0)
     - mood match (+1.5)
     - energy closeness (+1.38)
     - acoustic fit (+0.82)

2. Gym Hero by Max Pulse
   Score: 4.41 / 6.00
   Why:
     - genre match (+2.0)
     - energy closeness (+1.46)
     - acoustic fit (+0.95)

3. Rooftop Lights by Indigo Parade
   Score: 3.44 / 6.00
   Why:
     - mood match (+1.5)
     - energy closeness (+1.29)
     - acoustic fit (+0.65)

4. Laser Horizon by Pulsewave
   Score: 2.41 / 6.00
   Why:
     - energy closeness (+1.43)
     - acoustic fit (+0.98)

5. Storm Runner by Voltline
   Score: 2.38 / 6.00
   Why:
     - energy closeness (+1.48)
     - acoustic fit (+0.90)
```

### Chill Lofi

```text
============================================================
Profile: Chill Lofi
  genre=lofi, mood=chill, energy=0.4, likes_acoustic=True
============================================================

1. Library Rain by Paper Lanterns
   Score: 5.79 / 6.00
   Why:
     - genre match (+2.0)
     - mood match (+1.5)
     - energy closeness (+1.42)
     - acoustic fit (+0.86)

2. Midnight Coding by LoRoom
   Score: 5.68 / 6.00
   Why:
     - genre match (+2.0)
     - mood match (+1.5)
     - energy closeness (+1.47)
     - acoustic fit (+0.71)

3. Focus Flow by LoRoom
   Score: 4.28 / 6.00
   Why:
     - genre match (+2.0)
     - energy closeness (+1.50)
     - acoustic fit (+0.78)

4. Spacewalk Thoughts by Orbit Bloom
   Score: 3.74 / 6.00
   Why:
     - mood match (+1.5)
     - energy closeness (+1.32)
     - acoustic fit (+0.92)

5. Coffee Shop Stories by Slow Stereo
   Score: 2.35 / 6.00
   Why:
     - energy closeness (+1.46)
     - acoustic fit (+0.89)
```

### Deep Intense Rock

```text
============================================================
Profile: Deep Intense Rock
  genre=rock, mood=intense, energy=0.92, likes_acoustic=False
============================================================

1. Storm Runner by Voltline
   Score: 5.88 / 6.00
   Why:
     - genre match (+2.0)
     - mood match (+1.5)
     - energy closeness (+1.48)
     - acoustic fit (+0.90)

2. Gym Hero by Max Pulse
   Score: 3.93 / 6.00
   Why:
     - mood match (+1.5)
     - energy closeness (+1.48)
     - acoustic fit (+0.95)

3. Laser Horizon by Pulsewave
   Score: 2.44 / 6.00
   Why:
     - energy closeness (+1.46)
     - acoustic fit (+0.98)

4. Iron Cathedral by Black Furnace
   Score: 2.40 / 6.00
   Why:
     - energy closeness (+1.43)
     - acoustic fit (+0.97)

5. Fuego en la Pista by Los Ritmos
   Score: 2.18 / 6.00
   Why:
     - energy closeness (+1.38)
     - acoustic fit (+0.80)
```

### Conflicting: Sad but Energetic

```text
============================================================
Profile: Conflicting: Sad but Energetic
  genre=blues, mood=sad, energy=0.95, likes_acoustic=False
============================================================

1. Bayou Midnight by Lucille Gray
   Score: 4.42 / 6.00
   Why:
     - genre match (+2.0)
     - mood match (+1.5)
     - energy closeness (+0.68)
     - acoustic fit (+0.24)

2. Laser Horizon by Pulsewave
   Score: 2.48 / 6.00
   Why:
     - energy closeness (+1.50)
     - acoustic fit (+0.98)

3. Iron Cathedral by Black Furnace
   Score: 2.44 / 6.00
   Why:
     - energy closeness (+1.47)
     - acoustic fit (+0.97)

4. Gym Hero by Max Pulse
   Score: 2.42 / 6.00
   Why:
     - energy closeness (+1.47)
     - acoustic fit (+0.95)

5. Storm Runner by Voltline
   Score: 2.34 / 6.00
   Why:
     - energy closeness (+1.44)
     - acoustic fit (+0.90)
```

### Genre Not in Catalog

```text
============================================================
Profile: Genre Not in Catalog
  genre=k-pop, mood=happy, energy=0.7, likes_acoustic=False
============================================================

1. Sunrise City by Neon Echo
   Score: 3.64 / 6.00
   Why:
     - mood match (+1.5)
     - energy closeness (+1.32)
     - acoustic fit (+0.82)

2. Rooftop Lights by Indigo Parade
   Score: 3.56 / 6.00
   Why:
     - mood match (+1.5)
     - energy closeness (+1.41)
     - acoustic fit (+0.65)

3. Concrete Crown by Verse Theory
   Score: 2.26 / 6.00
   Why:
     - energy closeness (+1.38)
     - acoustic fit (+0.88)

4. Night Drive Loop by Neon Echo
   Score: 2.21 / 6.00
   Why:
     - energy closeness (+1.42)
     - acoustic fit (+0.78)

5. Laser Horizon by Pulsewave
   Score: 2.10 / 6.00
   Why:
     - energy closeness (+1.12)
     - acoustic fit (+0.98)
```

### Acoustic Lover Wanting Max Energy

```text
============================================================
Profile: Acoustic Lover Wanting Max Energy
  genre=folk, mood=peaceful, energy=0.95, likes_acoustic=True
============================================================

1. Cabin Smoke by Willow & Ash
   Score: 4.96 / 6.00
   Why:
     - genre match (+2.0)
     - mood match (+1.5)
     - energy closeness (+0.53)
     - acoustic fit (+0.94)

2. Dusty Back Roads by Wade Calloway
   Score: 1.62 / 6.00
   Why:
     - energy closeness (+0.95)
     - acoustic fit (+0.68)

3. Rooftop Lights by Indigo Parade
   Score: 1.56 / 6.00
   Why:
     - energy closeness (+1.22)
     - acoustic fit (+0.35)

4. Storm Runner by Voltline
   Score: 1.54 / 6.00
   Why:
     - energy closeness (+1.44)
     - acoustic fit (+0.10)

5. Fuego en la Pista by Los Ritmos
   Score: 1.53 / 6.00
   Why:
     - energy closeness (+1.33)
     - acoustic fit (+0.20)
```
<!-- profile-output:end -->

### Experiment notes

**Weight shift: energy x2, genre x0.5.** I changed the energy weight from 1.5 to 3.0 and the genre weight from 2.0 to 1.0 (mood and acoustic stayed the same, so the maximum score became 6.5). Run it with `python -m src.experiment`.

- High-Energy Pop, Chill Lofi, and Deep Intense Rock: the top two songs stayed the same. Only positions 3 to 5 reshuffled (for example, Storm Runner and Laser Horizon swapped for Pop, and Focus Flow and Spacewalk Thoughts swapped for Lofi).
- Genre Not in Catalog: Rooftop Lights and Sunrise City swapped first and second place, because without a genre match the energy score decides.
- Sad but Energetic: Bayou Midnight (energy 0.40) was still first, even though the listener asked for energy 0.95.
- Conclusion: the change made the lists different but not clearly more accurate. Exact genre and mood matches still outweigh the energy the listener asked for.

---

## Limitations and Risks

- The catalog has only 20 songs, and 15 of its 17 genres appear on a single song, so a genre match can only boost one or two songs.
- Exact label matches (genre 2.0 + mood 1.5) can outweigh energy (max 1.5): a slow blues song ranked first for a listener who asked for energy 0.95.
- Matches are all-or-nothing, so close genres and moods ("pop" and "indie pop") earn nothing.
- It ignores lyrics, language, tempo, valence, and danceability, and it never learns from skips or likes.

See the [Model Card](model_card.md) for the full discussion.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

**How recommenders turn data into predictions.** This project showed me that a recommender turns data into a prediction in three simple steps: describe each song with numbers and labels, describe the listener the same way, then score how well the two match and sort the results. The model never "knows" music. It only compares labels and measures distances. The reasons list next to each score made that easy to see, and it made bad picks easy to spot.

**Where bias or unfairness can show up.** Bias shows up in the choices behind the score. I made genre worth more than mood, so Gym Hero (pop but intense) outranked happier songs for pop fans. Exact matching meant "indie pop" counted for nothing for a "pop" fan. And with 15 of 17 genres on a single song, most labels could only help one or two songs. In a real app, choices like these, plus whose listening data gets collected, could quietly favor some listeners and artists over others.
