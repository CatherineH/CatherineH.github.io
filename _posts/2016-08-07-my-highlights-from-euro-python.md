---
layout: post
title: "My Highlights from Euro Python"
description: "Go, Gravitational Waves, and Graphics"
category: programming 
tags: [python, conference, euro python]
---
{% include JB/setup %}

I went to the Euro Python conference in Bilbao, Spain, directly from SciPy on July 17th. Though severely jet-lagged and with a head full of stuff from SciPy, I enjoyed Euro Python immensely. Bilbao is a lovely (and cheap) city, and I'm glad I had an excuse to visit. Here are my favourite presentations from Euro Python.

I also had another opportunity to [speak about pyglet helper](https://www.youtube.com/watch?v=8GIZW--41oE), but it was near identical to my SciPy presentation.

Python at the European Gravitational Observatory
================================================


[![Elena Cuoco - Python in Gravitational Waves Research Communities](http://img.youtube.com/vi/K6dFEAijY24/0.jpg)](https://www.youtube.com/watch?v=K6dFEAijY24)

Wednesday's keynote was given by Jameson Rollins of LIGO, and while it was good, as a physicist I got more out of Elena Cuoco's talk the day before. While Rollins' keynote was devoted mostly to explaining gravitational waves and their detection to a broad audience, Cuoco dove right into the tools used in the gravitational waves research communities. While most of it, such as the [pyrap](http://www.astron.nl/casacore/trunk/pyrap/docs/index.html) library for radio astronomy data processing and the [pycbc](https://github.com/ligo-cbc/pycbc) library for studying compact binary coalescence (black holes orbiting each other), do not apply to optical quantum computing, the [pykat](http://www.gwoptics.org/pykat/) library for simulating interferometers is. The performance of the entangled photon sources I help design depends on how well an optical interferometer can be stabilized, and I find simulation helpful. Who knows, perhaps the intensive effort that the gravitational wave community has put into clearing up and analyzing optical data can also be helpful in future.

Go and Python Side-by-Side
==========================

[![Max Tepkeev - Do I need to switch to Go(lang) ?](http://img.youtube.com/vi/SCV5froaArg/0.jpg)](https://www.youtube.com/watch?v=SCV5froaArg)

Earlier this year I dipped my toes into the Go language in order to fix some bugs in the [arduino builder](https://github.com/arduino/arduino-builder), and while I managed to fix what I wanted to fix, I was confused by many things in the Go language that introductory presentations on youtube did not clarify. Max Tepkeev's talk introducing Go was exactly what I needed - in addition to placing Go in relation to other languages and describing some use cases, his presentation features several slides of side-by-side python and go examples. I would highly recommend this presentation to any pythonistas going to Go.

Live OpenGL with Python
=======================

[![Roberto De Ioris - Modern OpenGL with Python](http://img.youtube.com/vi/DhS3QWKsOrw/0.jpg)](https://www.youtube.com/watch?v=DhS3QWKsOrw)

Roberto De Ioris teaches computer graphics at an Italian Video Game academy, and gave an hour-long tutorial on the basics of OpenGL using the python bindings. Though a lot of it was stuff you could speed through in a tutorial, De Ioris is a good teacher and the demos brought the material to life. I also appreciated hearing his thoughts on the stability and usability of [Vulkan](https://www.khronos.org/vulkan/) and clarify the difference between various shader and lighting techniques.


The Scientist and the Web Developer should be Friends
=====================================================

[![Gaël Varoquaux - Scientist meets web dev: how Python became the language of data](http://img.youtube.com/vi/ntuOIzxCshM/0.jpg)](https://www.youtube.com/watch?v=ntuOIzxCshM)

In undergrad I worked part-time as a web developer. The skills I picked up there transferred to my summer research projects in bioinformatics, but once I got to grad school, (for experimental physics), my skills were treated as useless. If only I could have made my point as eloquently as Gael Varoquax did in his keynote, perhaps I could have convinced my fellow physicists that databases were good and useful. It's also a great lecture as it explains the background of scientific computing and some of numpy's internals.

Teaching a Computer to Love (or at least when someone else loves something)
===========================================================================

[![Katharine Jarmul - I Hate You, NLP... ;)](http://img.youtube.com/vi/vitEXiOuiEk/0.jpg)](https://www.youtube.com/watch?v=vitEXiOuiEk)

I regret missing seeing this in person - there was a talk on algorithmic trading using python, and I've read one too many Michael Lewis books lately. The algorithmic trading talks was boring - it was a stealth recruitment pitch for a trading company, and with no tutorials on either stock trading or pricing. Katharine Jarmul's talk on using machine learning and natural language processing to determine the emotional intention of human text, such as tweets. It was good because it covered bleeding-edge research with the aim of helping mere programmers build stuff.

