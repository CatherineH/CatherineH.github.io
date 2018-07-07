---
layout: post
title: "Cairo Tilings with minimal math"
description: "generating svg python cairo tilings without doing much math"
category: programming
tags: [python, svg]
---
{% include JB/setup %}

I generate cairo tilings because I'm working on generating some custom printed fabric. Cairo tilings are an ideal pattern for clothing prints because they can be made from the same pentagon rotated to four different angles, yet still have a semi-regular repetition, meaning that you can clip the tiling at certain places, and copy that clip up and down to make an infinite pattern.

This post goes over my method of generating cairo tilings with minimal math using [my fork of svgpathtools](https://github.com/CatherineH/svgpathtools), and [svgwrite](https://svgwrite.readthedocs.io/en/master/). The full code to generate the tilings is available in my [python-sewing](https://github.com/CatherineH/python-sewing/blob/master/pattern_tiling.py) repository.

Drawing the base pentagon
=========================

According to wikipedia, a cairo tiling can be made with a pentagon with the interior angles of 120, 90, 120, 120, and 90 radians. So I'll start off with with an angle of 120 radians, and a length of 300 radians. I'm going to lay out my pentagon like this:

![a single pentagon with annotated points](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/cairo_tiling/pentagon.png)

*angle01* is the angle from horizontal to point 1 from point 0. I start with point 0 at 0,0:

```python
def cexp(x):
    return pow(exp(1), x)
angle01 = 60.0
length1 = 300
# start with the top corner at 0, 0
points = [0, None, None, None, None]
```

Next, points 1 and 4 are at the projection up and down of *angle01* from point 0:

```python
points[1] = points[0] + length1 * cexp(1j * radians(angle01))
points[4] = points[0] + length1 * cexp(-1j * radians(angle01))
```

points 1 and 4 have interior angles of 90 degrees. To project up from these points, I subtract *angle01* from 90: 
 
```python
angle12 = -(90 - angle01)
points[2] = points[1] + length1 * cexp(1j * radians(angle12))
points[3] = points[4] + length1 * cexp(-1j * radians(angle12))
```

I've drawn a single pentagon with minimal math - I only had to calculate the second projection angle, and the rest came from looking at the pentagon. I'm going to draw the four-groups of cairo tiling the same way.

Drawing the four-pentagon group
===============================

Next, I generate the 4-group:

![4 group of pentagons](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/cairo_tiling/4group.png)

Like before with projecting from already-calculated points, I let svgpathtools do the work - use it to rotate the pentagons, snap them into place, then use the difference between where the points ended up for a list of transforms that I can use later. 


```python
def new_pentagon():
	return Path(*[Line(start=points[i - 1], end=points[i]) for i in range(len(points))])

transforms = [[0, 0]]
cairo_group = [new_pentagon()]
# point 1 of pentagon 1 needs to be attached to point 1 of pentagon 0
cairo_group.append(transform_path(rotate_transform(90), new_pentagon()))
diff = cairo_group[0][1].end - cairo_group[1][1].end
transforms.append([90, diff])
cairo_group[1] = cairo_group[1].translated(diff)
cairo_group.append(transform_path(rotate_transform(180), new_pentagon()))
# point 3 of pentagon 2 needs to be attached to point 2 of pentagon 0
diff = cairo_group[0][2].end - cairo_group[2][3].end
transforms.append([180, diff])
cairo_group[2] = cairo_group[2].translated(diff)
cairo_group.append(transform_path(rotate_transform(-90), new_pentagon()))
# point 4 of pentagon 3 needs to be attached to point 1 of pentagon 0
diff = cairo_group[0][4].end - cairo_group[3][4].end
transforms.append([-90, diff])
cairo_group[3] = cairo_group[3].translated(diff)
```

Finally, I want to calculate the width of the 4-group so that I know where to repeat the 4-group in the next step:

```python
column_offset = cairo_group[0][0].end - cairo_group[1][2].end
```

Drawing the full pattern
========================

The final trick to generating the full tiling is that every other 4-group in each row needs to be moved down by half of the height of the 4-group:


```python
dwg = Drawing("{}/tiling2.svg".format(output_folder), profile="tiny")

current_color = 0
rep_spacing = pent_width * 2 + bottom_length

for y in range(num_down):
    transform = "translate({}, {})".format(0, rep_spacing * y)
    dgroup = dwg.add(dwg.g(transform=transform))
    for x in range(num_across):
        # if x is odd, point 0 of pent 0 needs to be attached to point 2 of pent 1
        if x % 2 == 1:
            dx = int(x / 2) * rep_spacing + pent_width * 2 + column_offset.real
            transform = "translate({}, {})".format(dx, column_offset.imag)
        else:
            transform = "translate({}, {})".format(int(x / 2) * rep_spacing, 0)
        group = dgroup.add(dwg.g(transform=transform))
        for pent in cairo_group:
            group.add(
                dwg.path(**{'d': pent.d(), 'fill': _colors[current_color % len(_colors)],
                            'stroke-width': 4, 'stroke': rgb(0, 0, 0)}))
            current_color += 1
dwg.save(pretty=True)
```

This generates the pattern:

![Full tiling](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/cairo_tiling/tiling3.png)

