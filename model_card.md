# Model Card: Music Recommender Simulation

## 1. Model Name

VibeFinder 1.0

---

## 2. Goal / Task

VibeFinder suggests songs from a small catalog that match a user's musical taste. Given a preference profile — a genre, a mood, and a few numerical targets like energy level — it scores every song in the catalog and returns the top matches ranked from best to worst. It does not learn or update over time. It makes one pass, scores everything, and hands back a list.

---

## 3. Data Used

The catalog is 18 songs stored in `data/songs.csv`. Each song has 10 fields: id, title, artist, genre, mood, energy, tempo, valence, danceability, and acousticness. The numerical fields (energy, valence, danceability, acousticness) are all on a 0.0 to 1.0 scale, similar to Spotify's audio features API. Genres represented include lofi, pop, rock, jazz, ambient, synthwave, indie pop, edm, hip-hop, country, funk, r&b, blues, classical, and folk. The dataset started as 10 songs and was expanded to 18 to cover more genres and moods. Limits: 18 songs is far too small for a real system, there are no actual users or listening histories, and the numerical values were hand-assigned rather than measured from real audio.

---

## 4. Algorithm Summary

The recommender works like a judge scoring contestants on a rubric. For each song in the catalog, it checks how well that song matches what the user said they like, awards points for each match, and adds them all up into a final score.

The rules are:

- If the song's genre exactly matches what the user wants, it gets 2 points. If the genre is in the same family (for example, lofi and ambient are both "chill" genres), it gets 1 point.
- If the mood matches exactly, it gets 1 point. If the mood is in the same energy group (for example, happy and euphoric are both high-energy moods), it gets half a point.
- For energy, valence, and acousticness, the score depends on how close the song's value is to the user's target. A perfect match gives the full weight. A large gap gives very few points.

Once every song has a total score, the list is sorted from highest to lowest and the top results are returned. Each result also prints the specific reasons it scored the way it did.

---

## 5. Strengths

The system works best when the user has a clear, consistent preference and the catalog has multiple songs in that genre. The Chill Lofi profile returned all three lofi songs in the top three, and they were genuinely the most similar songs in the catalog. The Deep Intense Rock profile put Storm Runner at #1 with a large gap to #2, which was the correct and intuitive result. The explainability is also a real strength — every recommendation prints exactly why it was chosen, which makes it easy to understand and debug. Most real recommenders give you a result with no explanation at all.

---

## 6. Limitations and Bias

The most significant weakness is that the genre and mood bonuses are so large that they can override a very poor numerical match. When a "High Energy + Sad Blues" profile was tested, the system returned "Last Train" as the top result — a slow, quiet blues song — because the genre and mood matched exactly, earning +3.0 points that the energy mismatch (user wanted 0.9, song has 0.33) could not overcome. A user asking for intense, energetic blues would get sleepy music instead.

A second bias comes from catalog imbalance. There are three lofi songs but only one rock, one blues, and one classical song. This means chill/lofi users get tighter, more accurate matches than users of underrepresented genres simply because there is more to compare against. The system is unintentionally better at serving certain tastes.

Finally, the system has no diversity mechanism. It will always return the same songs in the same order for the same profile. A real recommender would mix in occasional surprises to help users discover music outside their usual taste.

---

## 7. Evaluation Process

Six user profiles were tested — three standard personas and three adversarial edge cases.

Standard profiles tested:
- High-Energy Pop (genre=pop, mood=happy, energy=0.88)
- Chill Lofi (genre=lofi, mood=chill, energy=0.38)
- Deep Intense Rock (genre=rock, mood=intense, energy=0.92)

Adversarial profiles tested:
- High Energy + Sad Mood (genre=blues, mood=sad, energy=0.90) — to see if conflicting preferences break the system
- Unknown Genre (genre=bossa nova) — to see how the system handles a genre not in its vocabulary
- All 0.5 Midpoint — to see what happens when no preference is strong enough to dominate

The standard profiles all returned sensible results. The biggest surprise was Gym Hero appearing at #2 for the happy pop user — it has an "intense" mood, not "happy," but its pop genre match and close energy kept it near the top. The adversarial profiles confirmed the categorical dominance problem and showed that the unknown genre case actually fails more gracefully than the conflicting preferences case.

A weight shift experiment was also run — energy weight was doubled and genre weight was halved. This improved accuracy for the rock profile but broke coherence for the blues edge case, confirming that fixed weights are a core limitation.

---

## 8. Intended Use and Non-Intended Use

**Intended use:** Classroom exploration of how content-based filtering works. Useful for understanding how scoring rules, feature weights, and catalog composition affect recommendation quality. Intended for a single simulated user in an educational context.

**Not intended for:** Real users, production music apps, or any context where recommendation quality affects people's experience. The catalog is too small, the user profiles are manually defined rather than learned from real behavior, and the system has no safeguards against filter bubbles, repetition, or bias toward overrepresented genres.

---

## 9. Ideas for Improvement

1. **Per-user weights** — instead of fixed weights for genre and energy, let users signal which feature matters most to them. A user who only cares about energy should be able to say so, and the system should adjust accordingly.

2. **Multi-user collaborative filtering** — add a table of user listening histories so the system can say "users who liked what you like also listened to X." This is how Spotify and YouTube actually work at scale and would make recommendations feel much more alive.

3. **Diversity injection** — after ranking, swap out one of the top-5 results for a random song from a different genre group. This prevents the filter bubble where a lofi user only ever sees lofi songs and never discovers that they might also like jazz or classical.

---

## 10. Personal Reflection

The biggest learning moment was realizing how much the weight values matter — not just whether a feature is included, but how many points it is worth relative to everything else. When the genre bonus is +2.0 and the maximum energy contribution is +1.5, genre effectively controls the outcome for most comparisons. Changing that ratio during the weight shift experiment immediately reshuffled rankings in ways that were sometimes better and sometimes worse depending on the profile. That tension — categorical labels vs numerical closeness — is something real systems like Spotify deal with at massive scale, and even here with 18 songs it was non-trivial to balance.

Using AI tools during this project helped most when I was unsure about the math, like when deciding between Manhattan distance, Euclidean distance, and cosine similarity. The explanations made the tradeoffs clear and I could immediately test them. Where I needed to double-check was when the output looked plausible but felt off — Gym Hero appearing for happy pop users looked fine on paper because the score math was correct, but intuitively a workout song and a party song are not the same thing. That gap between "mathematically correct" and "actually useful" is something you only catch by looking at real examples, not by trusting the numbers alone.

What surprised me most was how quickly a simple points-based rubric starts to feel like a real recommendation. Running the Chill Lofi profile and seeing Library Rain and Midnight Coding at the top — both genuinely chill, acoustic lofi songs — felt like the system understood something. It did not. It just added numbers. But the structure of the scoring captured enough of what makes songs similar that the result was indistinguishable from something smarter. That is both the power and the danger of simple algorithms: they can look much more intelligent than they are.

If I extended this project, the first thing I would add is real user interaction data — even fake play counts per song per user — so I could layer collaborative filtering on top of the content scoring. The current system treats every user identically except for their stated preferences. A real recommender notices that you skipped a song after 10 seconds and learns from that, and that feedback loop is what makes systems like YouTube feel personal rather than just filtered.
