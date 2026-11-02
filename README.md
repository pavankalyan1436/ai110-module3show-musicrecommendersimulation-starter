# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

### How real platforms do it

Platforms like Spotify and YouTube mix two main ideas. **Collaborative filtering** predicts what you'll like from the behavior of *other* users: if people who share your listening history loved a track, it gets suggested to you, even if you can't say what the songs have in common. **Content-based filtering** looks at the *items themselves* (tempo, energy, mood, genre, lyrics) and recommends songs whose attributes resemble what you already enjoy. Real systems feed both with behavior signals such as likes, skips, saves, playlist adds, and listening or watch time. Explicit actions (a save or a playlist add) generally count for more than passive ones (a play that happened to finish), and recent activity counts for more than old activity.

### What my version does

My simulator is purely **content-based**. It has no other users to learn from, so it can't do collaborative filtering. It prioritizes, in order: a genre match, a mood match, how *close* a song's energy is to the user's target, and a small nudge for acoustic taste. Closeness matters more than "higher is better": a user who wants energy 0.4 should not be pushed toward a 0.93 workout track just because it has more energy.

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

**Scoring rule** (one song vs. one user; max 5.0 points):

| Component | Points |
|---|---|
| Genre matches `favorite_genre` | +2.0 |
| Mood matches `favorite_mood` | +1.0 |
| Energy closeness: `1.5 × (1 − abs(song.energy − target_energy))` | 0 to 1.5 |
| Acoustic fit: `0.5 × acousticness` if `likes_acoustic`, else `0.5 × (1 − acousticness)` | 0 to 0.5 |

Genre is weighted above mood because a genre mismatch is usually a bigger "wrong vibe" than a mood mismatch. These weights are a starting guess that I will test and tune in Phase 3.

**Ranking rule** (whole catalog): score every song with the scoring rule, sort by score from highest to lowest, and return the top `k`. The scoring rule can only say how good *one* song is; the ranking rule turns those separate scores into an ordered list. Each result also carries a short "because..." explanation built from the components that earned points.

### Known limits of this design

- A genre match is all-or-nothing, so "indie pop" earns nothing for a "pop" fan even though the two are close.
- With a 10-song catalog, a heavy genre weight can crowd out good songs from other genres (a small filter bubble).
- Nothing here learns from skips or likes, so the profile never changes.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   `````bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

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

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

`````
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
`````

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

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
`````

After pasting, save the file and check it:

`````bash
grep -n '^## ' README.md
`````

You should see seven headings. Then commit and push:

`````bash
git add README.md
git commit -m "Fix README: restore all sections and add Phase 1 design"
git push
`````

Paste the `grep` output once it's done, and we'll move on to the extra songs.