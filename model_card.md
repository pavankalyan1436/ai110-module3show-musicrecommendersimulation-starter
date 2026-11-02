# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works

Think of the recommender as a judge that grades every song in the catalog against one listener's wish list, then hands back the best matches.

**What describes each song.** Every song has a genre, a mood, an energy level from 0 (very calm) to 1 (very intense), and an acousticness from 0 (fully electronic) to 1 (fully acoustic). The catalog also stores tempo, valence, and danceability, but the model does not use those yet.

**What the listener tells it.** A favorite genre, a favorite mood, a target energy level, and whether they like acoustic-sounding music.

**How a song earns points (out of 6):**

- 2.0 points if the genre matches the listener's favorite exactly.
- 1.5 points if the mood matches exactly.
- Up to 1.5 points for energy. The closer the song's energy is to the listener's target, the more points it gets. A perfect match earns the full 1.5, and the points shrink as the gap grows. This is about closeness, not "more is better": someone who wants calm music is not rewarded for a high-energy song.
- Up to 1.0 point for acoustic fit. Listeners who like acoustic music give more points to acoustic songs, and everyone else gives more points to electronic ones.

**How it picks what to recommend.** The model grades every song one by one, sorts all the grades from highest to lowest, and returns the top five. Each recommendation also comes with a short list of reasons (for example, "genre match" or "energy closeness") so the listener can see why it was chosen.

**What I changed from the starter.** The starter code just returned the first few songs in the file with a placeholder explanation. I wrote the code that loads the song file, the scoring rule that produces a score plus reasons, and the ranking step. I also grew the catalog from 10 to 20 songs, gave mood slightly more weight than the suggested starting point (1.5 instead of 1.0) so it can connect songs across genres, and added the acoustic-fit score.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
