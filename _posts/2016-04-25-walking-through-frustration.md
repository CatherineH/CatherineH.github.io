---
layout: post
title: "Walking Through Frustration"
description: "My Failure at SpaceApps 2016"
category: programming
tags: [python, cpp]
---
{% include JB/setup %}

Six months ago I participated in a hackathon for the City of Waterloo. I built a WebGL application that built a little model of Waterloo that you could tilt and zoom in a browser. I used the building footprint data to find the base of the models, then used the latest aerial laser scan data minus the elevation data to estimate the height of the buildings. I coloured the buildings based on what their reported purpose and size were - one color for commercial buildings, one for municipal buildings, and one for residential buildings, then within that sub-shades for the types of buildings - apartment buildings, duplexes, single family dwellings. 

My desire to build this model came from my own curiosity - between the time that I moved to Waterloo in 2010 and left in 2015, an entire neighborhood transformed from 1950’s style bungalows to high-rise student housing, and I wanted to be able to see those buildings spring out of the ground. Also, I wanted an excuse to learn WebGL. The end result was a stylized version of google maps:

![ower screenshot](https://pbs.twimg.com/media/CSMy-TbWoAAUefs.png:large)

I was proud of what I’d put together in 48 hours, but it didn’t win anything. An app that for tracking trees won. It wasn’t technically impressive - Apple and Android both provide sample apps that allow you to add data to maps, and the tree data was provided by the city. City maintenance apps like this have been implemented by cities larger than Waterloo since 2010. But, the guys who won were funny teenagers, and it was impressive for their level of experience. 

After that hackathon I came to a fairly obvious conclusion: hackathons are about showmanship rather than technical ability, but I would rather impress myself than impress a judge. I’ve won hackathons on the basis of good presentations, but they’re not the things I brag about later.

Last weekend was SpaceApps 2016 - a yearly coding challenge organized by NASA. Communities around the world organize events for SpaceApps, and in previous years I’d attended the ones in Kitchener-Waterloo and Toronto. There is no event - at least open to the public - in San Diego, so I signed up for the “everywhere” event. Knowing that there was no competition with a pitch at the end, I decided to go for the most technically challenging project I could find: procedurally generating game environments using web map tile service files of Mars.

The most obvious way to solve the challenge - even cited in the challenge description, was to build something in Minecraft, but I went with the Unreal Engine instead. My reasons were two-fold: modding Minecraft is so easy that it is taught to elementary-aged kids, and secondly: I don’t like Minecraft. I have plenty of creative outlets in my everyday life, so when I sit down to play a video game I want to indulge my destructive impulses. I’d prefer to play first person shooters, hence my interest in building something in the Unreal Engine.

Getting the data
================
NASA is gradually improving their data services. My first encounter with them was in high school, where for a science fair project I downloaded their database of asteroid impact crafters to correlate the size and age using deeply flawed statistics to validate a hypothesis about Jupiter being the solar system’s asteroid dust-buster. Back then, I had to use ftp and some text macros to extract the desired data. It was painful. 

These days they’re moving to web-based APIs, but it’s still not as good as it could be. They claim that their datasets are WTMS-compliant, but I could not get a python WTMS library working with any of the datasets I wanted. I had two possible options - use the HiRISE data, which involves downloading large binary files via FTP, and then writing my own scripts to parse the binary data to a format I could use just as I had in high school, or going through the NASA  API to pull down much lower-resolution data sets and pulling them down one image at a time. This being a hackathon, I went with the second option.

I used the Mars Orbital Laser Altimeter to get grayscale png images for elevation, then pulled down the images from the Viking missions for colors and texture information. The highest resolution for both datasets were different, so I had to stitch together images, but thanks to the urllib and pillow python libraries, this was trivially easy.

Unreal Editor can turn grayscale images into level landscapes, and then generate the textures from images. Within four hours of starting my git repo, I had this: 

![false hope screenshot](https://pbs.twimg.com/media/CgvhX-3UcAAzd38.jpg:large)

Great! Challenge solved, time to hand in my solution and spend the rest of the weekend playing Borderlands. I just needed to programmatically spawn the process to generate landscapes and since Unreal Engine and Editor is open-source, I thought it couldn’t be that hard. 

Spoiler Alert: I was *super* wrong.

Failure 1: Automating Landscape Generation
==========================================

The problem is that landscapes are built into the level on build, and are impossible to change at run time. I’m trying to think of any FPS that have terrain that changes while you’re playing through a level or environment, and I can’t really think of any. Unlike top-down RPGs like Diablo, FPS’s rely on a lot of physics and not falling through things that are much harder to guarantee with a procedurally-generated world. Also, the load times on new levels are much faster if you have a pre-baked, compressed description of the landscape. 

At this point I considered giving up, but I kept going because the solution was so tantalizingly close: I could extract the compressed files that contained the landscape information, and somewhere in the source code for the Unreal Editor was the functionality to generate these files. 

After three hours of poking through the Unreal Editor in Visual Studio with IntelliSense (I don’t recommend this, Visual Studio crashed five times during this time), I identified the sections that did the importing and then writing to a file. I attempted to pull them out and build a standalone C++ application that could convert grayscale images to Unreal Editor map files.

However, this code wasn’t intended to operate on its own. As time went on, I was pulling in more and more of the unreal editor - first the menus for generating landscapes, then the new level editor, then the editor gui itself. Basically, I was re-implementing the Unreal Editor with no end in sight. 

At this point, 13 hours in, I considered giving up again. I was tired of Visual Studio crashing, and feeling cheated out of what I thought was a simple operation. But John sent me a tutorial on procedurally generating meshes at runtime and I had a crazy idea - why don’t I just delete the landscape and use a spawned mesh object instead?

Success 1: Generating Meshes
============================

For reasons my sleep-deprived post-hackathon brain can’t remember, the mesh tutorial code didn’t work with Unreal Engine 4.11, but did with 4.7. So, after spending an hour removing 4.11/Visual Studio 2015 and installing 4.7/Visual Studio 2013, I was back in business.

I intended that my Unreal Engine mesh generator code would check the tile cache for the desired section of Mars to render, and if it didn’t exist, execute the python script for pulling down the missing tiles. I encountered a problem implementing this: the windows C SDK does not play nicely with the Unreal Engine API. This is for good reason - Unreal Engine wants to be cross-platform, so they have re-implemented all the standard functionality of C independent of each operating system. If you attempt to include both the Unreal Engine and the Windows SDK in the same application, Visual Studio will bug out because it’s not sure which version of *int* you want to use.

I scrapped that idea. Luckily, I wasn’t totally out of luck for feeding data into Unreal Engine at runtime because networking is required for multiplayer games. So, after another four hours, I had a python server communicating with my Unreal Engine application. My first ground meshes looked like this: 

![mesh screenshot](https://pbs.twimg.com/media/Cg08v0AU8AAymmo.jpg:large)

It’s off the ground because I hadn’t sorted out the math yet, and it suddenly turns into a giant vertical wall because it turns out a TCP packet is not large enough to store the raw data required to render a 400 km-across section of Mars. So, I wrote the first compression method I could think of, and was able to serve mars up 3 Kbytes at a time. The result looked like this:

![final mesh screenshot](https://pbs.twimg.com/media/Cg1TEqbUYAAk8Vr.jpg:large)

That red planet sure is… red. 

Failure 2: Colouring the ground
=============================== 
 
Like landscape files, textures are compressed and baked into the levels prior to runtime. No problem, I’d solve that issue like I had with the meshes: change the color of the triangles in the mesh to match the corresponding pixel in the images. 

I had all of this implemented two hours before the deadline, but then shit started crashing. I was hitting a breakpoint in the memory allocation functionality of Unreal Engine. In addition, color images aren’t as smooth as surface data, so my poorly-implemented compression method wasn’t cutting it anymore. I would guess that these two issues are related. At this point, frustrated and exhausted, I decided to pack up and submit what I had. 

Conclusion
==========

So that was it. In the end, I tracked 29 hours working on SpaceApps this year, compared to 15 hours in 2015, and this year was way more stick-your-head-through-your-keyboard inducing than last year.

For reference, this is what John and I together were able to create at the end of SpaceApps 2015: 

![DBNN.NASA screenshot](https://pbs.twimg.com/media/CCZY3zHUAAAOsVm.png:large)

That project was much less frustrating than this one because it involved 
machine-learning analysis of experimental data in python, which is pretty 
much what John and I do for work. All of the code was built on existing tools
 used by scientists, who, despite what people may think, maintain their code 
 better than video game developers. Game developers are under constant pressure to release the next big game and thus don’t have much time or incentive to contribute back to the community, whereas (good) scientists’ reputation depends on other people being able to use the frameworks they create. 

Throughout this challenge, I was often attempting to use things in ways 
they weren’t meant to be used: using meshes as landscapes the player could walk on, using the networking protocol to serve massive texture data instead of the locations of other players. 

Since my project crashed with two hours left on the clock, I wasn’t able to make a video of what it looks like to walk around in my generated Mars. This means the project likely won’t win anything. That’s fine: like with the Waterloo hackathon, impressing myself was more important than impressing a judge, and in that goal I succeeded. Not because of what I learned: though I learned a lot about how the unity engine and editor work, the real takeaway was that I really don’t want to be a AAA game developer if these are the tools they have to use. I’m impressed with myself because several times this weekend in the face of a problem - like automating the landscape generation - I was miserable and had decided to quit. But every time I did, I would go nap on the couch for a bit, wake up, and go right back to banging my head through the keyboard.
