---
layout: post
title: "Controlling an Optical Switch via Arduino (Teensy)"
description: ""
category: programming
tags: [electronics, C, python, InstrumentKit]
---
{% include JB/setup %}
    
Aside from fingerprints, there is nothing more annoying, or more damaging to optics equipment than unplugging and
plugging in fiber optics. Every time a fiber tip or port is exposed to air, there's a chance of getting gross human skin
 cells on places where tightly focused high-power light might incinerate them, yet, so many experiments require routing
 light. Wouldn't it be nicer if a robot did the switching for you at 2 am while your gross dust and sweat producing body
  is sleeping?

In experiments, I accomplish this using a teensy LC and a DiCon optical switch.

Electronics Side
================

The optical switch I use is a [DiCon 2x2 prism switch](http://www.diconfiberoptics.com/products/scd0009/scd0009f.pdf),
which is essentially a little piece of glass on a motor.

![A picture of a DiCon fiber optic switch](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/dicon_switch.jpg)

This switch will operate in several modes, but in every mode the first two (blue and purple) pins are used to set the
position and the second two (red and green) pins are used to read the position of the switch.

I chose to operate the switch in *Non-latching 2-pin Control* mode, because it was the least complicated.

I chose to put the two pins that should never change in control mode (purple should always be ground, red should always
be +5V) and the two pins with changing values (blue and green) on the other. This led to a lot of initial confusion, but
 I believe it was a good decision to because it allows me to keep the two pins that need to be hooked up to some external logic together.

![A picture of the headers going into the teensy](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/teensy_switch.jpg)

The threshold voltage for switching is above 3.3V, which is the maximum that the Teensy's output pins can supply. Thus,
I chose to use a solid state relay to bump the signal up to 5V. I use Sharp Microelectronics
[R22MA1](http://www.digikey.com/product-detail/en/sharp-microelectronics/PR22MA11NTZF/425-2602-5-ND/856883) because
they're super cheap (25.65$ for 50) and I have a tendency to accidentally blow electronics up.

My prototype board looks like this:

![Fritzing image of breadboard](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/switch_bb.png)

Imagine the Sharp SSR on the breadboard instead of the Omron SSR. You'll notice that I have left the green pin
unconnected. The switch has always activated when 5V, thus the position information isn't useful right now.
