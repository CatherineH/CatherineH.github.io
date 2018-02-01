---
layout: post
title: "Text to SVG Paths"
description: ""
category: programming
tags: [svg, python]
---
{% include JB/setup %}

Most paper cutters, laser engravers, and 3D printers can't handle fonts, and so ignore <pre><text></pre> tags in SVGs. Instead, text elements need to first be converted to paths by a program like Inkscape. This post describes how to automate text to path conversion in python using the [freetype](https://github.com/rougier/freetype-py), [svgpathtools](https://github.com/mathandy/svgpathtools), and [svgwrite](https://github.com/mozman/svgwrite) libraries. I used the freetype [rendering in matplotlib example](https://github.com/rougier/freetype-py/blob/04c62af91c66b3268051921d609c9552d93560aa/examples/glyph-vector-2.py) as a guide.

First, load the svgpathtools paths, and define a tuple_to_imag function to convert between freetype's tupple point representation to svgpathtools' imaginary numbers:

```python
from svgpathtools import wsvg, Line, QuadraticBezier, Path
def tuple_to_imag(t):
    return t[0] + t[1] * 1j
```

Load your font and initialize a character:


```python
from freetype import Face
face = Face('./Vera.ttf')
face.set_char_size(48 * 64)
face.load_char('a')
```

We'll be converting a string character by character. After converting this character to a path, you use the same method to convert the next character to a path, offset by the kerning:

```python
face.get_kerning('a', 'b')
```

You'll need to flip the y values of the points in order to render the characters right-side-up:

```python
outline = face.glyph.outline
y = [t[1] for t in outline.points]
# flip the points
outline_points = [(p[0], max(y) - p[1]) for p in outline.points]
```

The face has three lists of interest: the points, the tags, and the contours. The points are the x/y coordinates of the start and end points of lines and control points. The tags indicate what type of point it is, where tag values of 0 are control points. Finally, the contours are the end point list index for each shape. Characters like i or ! have two shapes, most others have only one contour. So, for each contour, we want to pick out only the tags and points for that contour.

```python
start, end = 0, 0
paths = []

for i in range(len(outline.contours)):
    end = outline.contours[i]
    points = outline_points[start:end + 1]
    points.append(points[0])
    tags = outline.tags[start:end + 1]
    tags.append(tags[0])
```

Next, we want to split the points up into path segments, using the tags. If the tags are 0, add the point to the current segment, else create a new segment, so that control points stay with their path segments:

```python
    segments = [[points[0], ], ]
    for j in range(1, len(points)):
        segments[-1].append(points[j])
        if tags[j] and j < (len(points) - 1):
            segments.append([points[j], ])
```

Then convert the segments to lines. For lines with two control points (segment length 4), I could use the CubicBezier, but I find that breaking it into two Quadratic Beziers where the end point for the first and the start point of the second curve is the average of the control points, is more attractive:

```
    for segment in segments:
        if len(segment) == 2:
            paths.append(Line(start=tuple_to_imag(segment[0]),
                              end=tuple_to_imag(segment[1])))
        elif len(segment) == 3:
            paths.append(QuadraticBezier(start=tuple_to_imag(segment[0]),
                                         control=tuple_to_imag(segment[1]),
                                         end=tuple_to_imag(segment[2])))
        elif len(segment) == 4:
            C = ((segment[1][0] + segment[2][0]) / 2.0,
                 (segment[1][1] + segment[2][1]) / 2.0)

            paths.append(QuadraticBezier(start=tuple_to_imag(segment[0]),
                                         control=tuple_to_imag(segment[1]),
                                         end=tuple_to_imag(C)))
            paths.append(QuadraticBezier(start=tuple_to_imag(C),
                                         control=tuple_to_imag(segment[2]),
                                         end=tuple_to_imag(segment[3])))
```


Set the start location to the end location and continue. You can use the svgpathtools *Path* to merge the paths:

```python
    start = end + 1

path = Path(*paths)
wsvg(path, filename="text.svg")
```

text.svg looks like:

<svg baseProfile="full" height="600px" version="1.1" viewBox="50.304 -180.096 1691.392 2152.192" width="472px" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">
	<defs/>
	<path d="M 1060.0,896.0 Q 714.0,896.0 581.0,970.5 Q 448.0,1045.0 448.0,1225.0 Q 448.0,1368.0 548.0,1452.0 Q 648.0,1536.0 820.0,1536.0 Q 1057.0,1536.0 1200.5,1377.5 Q 1344.0,1219.0 1344.0,956.0 L 1344.0,896.0 L 1060.0,896.0 M 1600.0,761.0 L 1600.0,1728.0 L 1344.0,1728.0 L 1344.0,1472.0 Q 1249.0,1636.0 1107.0,1714.0 Q 965.0,1792.0 759.0,1792.0 Q 499.0,1792.0 345.5,1641.0 Q 192.0,1490.0 192.0,1236.0 Q 192.0,941.0 380.5,790.5 Q 569.0,640.0 944.0,640.0 L 1344.0,640.0 L 1344.0,616.0 Q 1344.0,444.0 1218.5,350.0 Q 1093.0,256.0 865.0,256.0 Q 721.0,256.0 583.5,288.0 Q 446.0,320.0 320.0,384.0 L 320.0,128.0 Q 470.0,64.0 610.5,32.0 Q 751.0,0.0 884.0,0.0 Q 1244.0,0.0 1422.0,189.0 Q 1600.0,378.0 1600.0,761.0" fill="none" stroke="#000000" stroke-width="1.792"/>
</svg>

You can see the full code in [this gist](https://gist.github.com/CatherineH/499a312a04582a00e7559ac0c8f133fa).
