---
layout: post
title: "Analyzing the Musical Battle Royale"
description: "music"
category: music
tags: [music, python]
---
{% include JB/setup %}

My mind defaults to one of three questions while idle, like when I'm running or biking to work. These are:

- What technology would I be able to recreate in the Roman Republic if I fell through a time vortex right now?
- How can the physical laws governing vampires and other paranormal creatures be exploited to build a perpetual motion machine?
- What is the best musical act of all time?

Though the situations are hypothetical, at least the first two have concrete answers. It's hard for me to decide on the best music even when limited to my own personal taste. Plus, the music taste that represents how I see myself as a person is different than the amount of enjoyment derived while listening. Thanks to a [sloppy python script](https://github.com/CatherineH/chusic/blob/master/analyze.py), I can at least answer what musical acts I seem to enjoy listening to the most.

For the past six years I've been running a musical battle royale: I've limited my playlist to 16 Gb and new songs can only be added when old music is deleted. I determine which songs to delete by playing my entire collection on shuffle. In order to skip to the next song, it must be deleted, and once deleted it can never be re-added. I like this system because it requires me to contemplate why a song is annoying, boring, or bad before being issued to the void. 

The most obvious measure of how much I like a band is the number of tracks by that act on my playlist. 

By number of tracks, the ranking is:

1.	Joe Bonamassa (86)
2.	Spock's Beard (60)
3.	Jethro Tull (59)
4.	Steve Vai (54)
5.	Ayreon (46)
6.	The Flower Kings (46)
7.	The Moody Blues	(42)
8.	Katatonia (39)
9.	King Crimson (39)
10.	Yes (38)

This ranking is surprising considering that I panned [Katatonia](http://catherineh.github.io/music/2016/08/02/music-people-recommend-to-me-2.html) last month. The high track count is mostly an indication that it hasn't been in the battle royale long enough to be cut down. 

After seeing this ranking, I decided that a better metric might be the date created, as older tracks mean that I still enjoy them depite being played many times. Unfortunately, this playlist is stored on a linux system so I only have access to the date the file was last modified, and not the date the file was created.

By oldest track modification date, the ranking is:

1. Marduk
2. Sourvein
3. Vektor
4. Tribulation
5. Into Another
6. BADBADNOTGOOD
7. Tengger Cavalry
8. Ketzer
9. Van der Graaf Generator
10. MisþYrming

This list also seemed off: I was listening to more paletable prog rock before venturing into Van der Graaf Generator. Then I remembered that a six months ago I spent a lot of time programmatically fixing the broken mp3 tags in the playlist. This metric is thus a proxy measurement for how broken the tags were when they were added to the list, which usually only indicates whether I bought the music off of bandcamp or acquired it through other means. Many of these tracks have modification dates that differ by only a few seconds. I decided to change this ranking to classify all tracks modified on the same day as having the same age. I can then come up with a combined ranking where the age is weighted at 0.5 as the counts.

By count ranking + 0.5*modification date ranking, the ranking is:

1. Jethro Tull	(3.5)
2. Ayreon	(5.5)
3. The Flower Kings	(6.5)
4. Dream Theater	(13.5)
5. Rush	(14.5)
6. Baroness	(15.5)
7. Vektor	(17.5)
8. Spock's Beard	(20.0)
9. The Alan Parsons Project	(21.5)
10. Sasquatch	(22.5)

This combined metric ranking is the closest to the song that play in my head in the shower, so it feels more accurate than the other two rankings. It's also extremely embarrassing. As much as I'd like to think of myself as having a modern and diversified pallette, it turns out that I really just like middle-aged white guys who sing about aliens and robots. I enjoy rap music or R&B, but the battle royale is hard for tracks that are distracting or without replay value. The ranking also skews away from genres I love but haven't been listening to recently, such as classical, folk, jazz and singer/songwriters of the 60s and 70s. It will be interesting to see how it ranking changes over time.

 

 


