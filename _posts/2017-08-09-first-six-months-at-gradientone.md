---
layout: post
title: "First Six Months at GradientOne"
description: "All the functionality"
category: programming
tags: [python, javascript, hardware]
---
{% include JB/setup %}

Six months ago I moved to Florida and started working at GradientOne, a startup building a web-based platform for interacting with scientific and testing instruments and performing data analysis. It's directly in the center of my interests and has kept me pretty occupied. Between my new job and [working on the electrical wiring of my new house](https://code.likeagirl.io/three-ways-programming-made-me-a-better-electrician-7403539088f), I haven't had much time for side-projects or reviewing the music I've been listening to.

However, I have been blogging for dollars about the things I've built for GradientOne, and I'm going to use this blog post as an opportunity to show off what I've built. If any of this functionality interests you, you should [contact GradientOne](http://www.gradientone.com/contact-us.html) to get API access or talk about your specific required functionality.

[CANOpen Support](http://www.gradientone.com/blog/canopen-in-the-cloud-part-1-polling)
======================================================

I added support for CANOpen devices, which was quite different from the SCPI-compliant devices GradientOne had previously supported. Unlike SCPI, I had never really worked on CAN protocols before, which was much more like TCP/IP than a serial communication protocol. I created a web-based CANOpen frame interpreter, so others learning CANOpen might find it easier in the future.

![screenshot of the frame interpreter](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/gradientone6months/interpreted-frames_orig.png)

[Trace Pattern Matching](http://www.gradientone.com/blog/trace-pattern-matching)
================================================================================

There have been many occasions where in the process of debugging a piece of equiment, I have observed a plot and had it trigger a sense of deja-vu. Shapes can stick in memory a lot easier than a list of numbers. The trace pattern matching tool I created allows sections of a set of x-y data to be tagged and then searched against all previous trace data. This means that if there is a consistent blip in an experiment that happens one in a thousand times, the blip can be identified, even if the blip appears at different times and locations, or even multiple times. Once patterns have been defined, they can be used to define other measurements, so you could do something like calculate the time between the start of a clock signal and the appearance of a specific byte.

![screenshot of full analysis](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/gradientone6months/full-analysis_orig.png) 


[Pass/Fail Criteria definition](http://www.gradientone.com/blog/passfail-criteria)
==================================================================================

Most modern factories operate on PLCs, where each individual process boils down to true/false boolean values when determining future branching processes. To that end, I created an interface for defining tests to add pass/fail criteria to collected data. The Pass/Fail criteria can come at the end of a series of multiple different measurements. Calculated pass/fail measurements are added to the search index so that existing measurements can be quickly sorted based on passes and failures.

![screenshot of pass/fail criteria editor](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/gradientone6months/pass-fail-suite-editor_orig.png) 


[GradientOne Command Language](http://www.gradientone.com/blog/gradientone-command-language)
============================

Knowing exactly how to communicate with a new device once you get it is an annoying pain. Although devices that are SCPI compliant are a bit easier to use than those that use some new communications protocol developed by an engineer throwing darts at a keyboard, as a lot of devices developed outside of the US seem to do, many device manufacturers fail to make their SCPI protocols SCPI-compliant. The GradientOne Command Language uses python-like syntax and tries to provide a consistent grammar for writing and querying instruments. Once a device's functionality has been added to GradientOne, incorporating it into the Command Language means that the web editor can hint the user about all available functionality.

![screenshot of editor command hinting](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/gradientone6months/auto-complete_orig.png)

 
Those are the four big projects I've shipped in the past six months. I'm currently working on using machine learning for decoding digital signals, and have planned support for more devices.
