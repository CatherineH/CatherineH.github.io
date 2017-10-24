---
layout: post
title: "Emoji data markers in matplotlib"
description: ""
category: programming
tags: [python, matplotlib]
---
{% include JB/setup %}

Using matplotlib's **axes.transData** and **get_sample_data**, it's possible to replace data markers with images, such as the poo emoji:

![a sine wave of poo](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/poo_plot.png)

This is fun and silly, but it's also important for accessibility for people with colorblindness or with shitty printers, like me.

**axes.transData** can transform x/y coordinates into the plot's pixel location on the plot output.
In order to then convert the pixel location to the figure's 0.0-1.0 scale, divide by these locations by the size of the figure's bounding box.

```python
from os.path import join, dirname, abspath
from matplotlib import pyplot
from matplotlib.cbook import get_sample_data
from numpy import linspace
from numpy.core.umath import pi
from numpy.ma import sin

# poo-mark came from emojipedia:
# https://emojipedia-us.s3.amazonaws.com/thumbs/120/apple/96/pile-of-poo_1f4a9.png
poo_img = pyplot.imread(get_sample_data(join(dirname(abspath(__file__)), "poo-mark.png")))

x = linspace(0, 2*pi, num=10)
y = sin(x)

fig, ax = pyplot.subplots()
plot = ax.plot(x, y, linestyle="-")

ax_width = ax.get_window_extent().width
fig_width = fig.get_window_extent().width
fig_height = fig.get_window_extent().height
poo_size = ax_width/(fig_width*len(x))
poo_axs = [None for i in range(len(x))]
for i in range(len(x)):
    loc = ax.transData.transform((x[i], y[i]))
    poo_axs[i] = fig.add_axes([loc[0]/fig_width-poo_size/2, loc[1]/fig_height-poo_size/2,
                               poo_size, poo_size], anchor='C')
    poo_axs[i].imshow(poo_img)
    poo_axs[i].axis("off")
fig.savefig("poo_plot.png")
```