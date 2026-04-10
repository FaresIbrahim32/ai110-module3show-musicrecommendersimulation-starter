# Reflection: Profile Comparisons

## High-Energy Pop vs Chill Lofi

These two profiles produce completely opposite results, which makes sense because they are opposite in almost every preference. The High-Energy Pop profile wants fast, loud, upbeat songs — it surfaces pop and EDM. The Chill Lofi profile wants slow, quiet, acoustic songs — it surfaces lofi and ambient. What is interesting is that no song appears in both top-5 lists. The numerical features (energy and acousticness especially) are pulling so hard in opposite directions that there is zero overlap. This is the system working correctly — two very different users get two very different playlists.

---

## Chill Lofi vs Deep Intense Rock

Both profiles have a clear genre that exists in the catalog, so both get strong exact-match bonuses. The difference shows up in #2 through #5. Chill Lofi's lower results are all acoustic, low-tempo songs from the chill genre group (ambient, classical, jazz). Deep Intense Rock's lower results are all high-energy songs from the energetic genre group (hip-hop, funk, indie pop). This makes sense — when the best genre match is gone, both profiles fall back to energy closeness, and because their target energies are at opposite ends of the scale (0.38 vs 0.92), they recruit completely different pools of songs.

---

## High-Energy Pop vs Deep Intense Rock

Both want high-energy songs, so they share some overlap in the middle rankings — Gym Hero appears in both top-5 lists. The difference is in what separates the top from the bottom. Pop profile rewards happy, upbeat mood and penalizes anything dark. Rock profile rewards intense mood and low valence (less positive). Gym Hero scores well for both because its energy is high and it shares a genre group with pop while also having the "intense" mood that rock wants. It is a song that sits at the border of both tastes, which is exactly why it keeps appearing — it is the safest recommendation when the system is not sure which direction to go.

---

## High Energy + Sad Mood (edge case) vs All 0.5 Midpoint (edge case)

These two edge cases fail in different ways. The High Energy + Sad profile gets a confident but wrong answer — Last Train wins decisively because genre and mood match, but the song is the opposite of what the energy preference asked for. The All 0.5 Midpoint profile gets a technically correct but meaningless answer — every song scores similarly because 0.5 preferences do not strongly penalize anything, so small categorical differences decide the rankings. One profile has too strong a signal that overrides everything else; the other has no signal at all. Both reveal that the scoring system needs the user to give it a genuine, internally consistent preference to work well.

---

## Unknown Genre (bossa nova) vs Chill Lofi

Both profiles end up recommending similar songs (Coffee Shop Stories, Midnight Coding, Library Rain, Spacewalk Thoughts) even though their stated genres are different. This happens because the unknown genre profile has no genre points at all, so it falls back entirely on mood and numerical features — and its target values (energy=0.45, acousticness=0.70, mood=relaxed) happen to be very close to what the Chill Lofi profile also prefers numerically. The lesson here is that when genre is removed from the equation, users with similar numerical taste end up in the same place. In a real system like Spotify, this would be a feature — genre labels are often inconsistent, and falling back to audio features is more reliable.
