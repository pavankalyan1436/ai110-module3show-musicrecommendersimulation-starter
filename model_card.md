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

**Biggest weakness: exact label matches outweigh what the listener actually asked for.** In my "Sad but Energetic" test (blues, sad, energy 0.95), the top song was Bayou Midnight, a slow blues track with energy 0.40. It scored 4.42 because matching both genre and mood is worth 3.5 points, while being far off on energy only cost it about 0.8 points. The listener asked for loud, driving music and got the quietest song in the list. When I doubled the energy weight and halved the genre weight, Bayou Midnight was still number one. The score rewards a matching label more than a matching sound, which means anyone whose genre and mood tags point one way and whose energy points the other will be steered by the tags.

Other limits I noticed:

- The catalog is tiny: 15 of its 17 genres appear on exactly one song, so a genre match can only ever boost one or two songs, and the rest of the list is decided by energy and acousticness alone.
- Matches are all-or-nothing, so "indie pop" earns nothing for a "pop" fan and "euphoric" earns nothing for a "happy" fan, even though they are close.
- Genre outweighs mood, so Gym Hero (pop but intense) keeps outranking true "happy" songs for pop fans.
- Some tastes cannot be satisfied by this catalog: nothing is both high-energy and acoustic, so the "Acoustic Lover Wanting Max Energy" profile got one good match and then a sharp drop in score.

---

## 7. Evaluation

**Profiles tested.** Three everyday profiles: High-Energy Pop (pop, happy, energy 0.90), Chill Lofi (lofi, chill, energy 0.40, likes acoustic), and Deep Intense Rock (rock, intense, energy 0.92). Three edge cases built to trick the scoring: Sad but Energetic (blues, sad, energy 0.95), Genre Not in Catalog (k-pop, happy, energy 0.70), and Acoustic Lover Wanting Max Energy (folk, peaceful, energy 0.95, likes acoustic). For each one I looked at the top five songs and whether the reasons printed next to each score made sense.

**What looked right.** Chill Lofi got Library Rain, Midnight Coding, and Focus Flow, all calm, acoustic lofi tracks, and Deep Intense Rock got Storm Runner (5.88), a loud rock song matching genre, mood, and energy. High-Energy Pop put Sunrise City first. These matched my own intuition about what those listeners would want.

**What surprised me.** Gym Hero showed up in three of the six lists (Pop, Rock, and Sad but Energetic). For a friend who just wants happy pop: Gym Hero is a pop song, so it gets the full genre bonus, and it is very high energy, so it is also close to what an energetic listener asked for. It is an intense workout track, not a happy one, but the system can only check whether the mood label matches exactly, and genre is worth more than mood. So it ranks above songs that actually feel happier. The other surprise was the Sad but Energetic result above.

**Weight experiment.** I doubled the weight on energy and halved the weight on genre. For the Pop, Lofi, and Rock profiles the top two songs stayed the same and only positions three to five reshuffled. For Genre Not in Catalog, Rooftop Lights and Sunrise City swapped places. Sad but Energetic still put Bayou Midnight first. So the change made the lists different, but not clearly more accurate. (The maximum possible score also became 6.5, so scores are not directly comparable between the two runs.)

**Comparing pairs of profiles.**

- Pop vs. Lofi: no songs in common. Pop gets bright, fast pop; Lofi gets calm, acoustic lofi, ambient, and jazz. That makes sense because they disagree on genre, mood, energy, and acousticness at once.
- Pop vs. Rock: they share Gym Hero, Laser Horizon, and Storm Runner. Both want energy around 0.9, so the same loud songs fill the lists, and genre and mood only reorder them (Sunrise City leads for Pop, Storm Runner for Rock).
- Pop vs. Sad but Energetic: both want very high energy, but the sad profile's number one is a slow blues song, pulled up by its genre and mood match. Its other four picks are the same loud songs Pop gets.
- Pop vs. Genre Not in Catalog: with no genre match possible, scores drop by about two points (5.70 to 3.64 at the top), and the list is decided by mood and energy, so happy songs like Sunrise City and Rooftop Lights lead.
- Pop vs. Acoustic Lover: both want high energy, but the acoustic lover flips the acoustic score, so electronic pop tracks fall away. The only strong match is Cabin Smoke, a folk song with low energy.
- Lofi vs. Rock: opposite ends of the catalog with no overlap: quiet, acoustic, slow versus loud, electric, fast. This is the clearest sign the scoring separates different tastes.
- Lofi vs. Sad but Energetic: Lofi's wishes agree with each other (calm, chill, acoustic), so its whole list is coherent. The sad profile's wishes conflict, so only the first song is driven by labels and the rest are just the loudest songs.
- Lofi vs. Genre Not in Catalog: Lofi has strong label matches and scores up to 5.79; the k-pop profile has none and tops out at 3.64, so it gets the closest vibe instead of a real match.
- Lofi vs. Acoustic Lover: both like acoustic music, but lofi songs are calm and acoustic, so Lofi is easy to satisfy. No song in the catalog is both high-energy and acoustic, so the acoustic lover gets one label-driven match and then a drop from 4.96 to 1.62.
- Rock vs. Sad but Energetic: they share four songs (Storm Runner, Gym Hero, Laser Horizon, Iron Cathedral). Rock's number one matches on everything, while the sad profile's number one matches on labels and misses on energy.
- Rock vs. Genre Not in Catalog: Rock gets a confident number one (5.88); the k-pop profile gets only mood-and-energy matches, so its scores are much lower and the list is led by happy pop songs.
- Rock vs. Acoustic Lover: both want high energy, but the acoustic lover's list has a cliff and ends up with electronic songs like Storm Runner and Fuego en la Pista in positions four and five, since energy is all that is left to rank on.
- Sad but Energetic vs. Genre Not in Catalog: one perfect label match (Bayou Midnight) jumps to 4.42, while no label match at all gives a smooth, lower list (3.64 down to 2.10). Single exact matches have an outsized effect.
- Sad but Energetic vs. Acoustic Lover: both have conflicting wishes and both put a low-energy song with matching labels first (Bayou Midnight, Cabin Smoke), then drop sharply to high-energy songs with no label match.
- Genre Not in Catalog vs. Acoustic Lover: a missing genre gives a gentle, smooth ranking, while impossible preferences give a sharp cliff. The system handles "no match" better than "conflicting wishes."

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
