---
layout: post
title: "3 ways of cutting SVG shapes"
description: "removing negative space"
category: programming
tags: [python, svg, shapely]
---
{% include JB/setup %}

SVGs will display the last added shape on top. This means you can very easily create the Canadian flag by layering a white rectangle on top of a red rectangle, but [that correctly representing merged SVGs is difficult](http://catherineh.github.io/programming/2018/01/21/layering-svgs-in-javascript). It also means that, if you're using SVGs to generate things in meatspace, like with a 3D printer, laser cutter or computerized sewing machine, you're going to waste material and reduce the quality of the output. Before sending the SVG to the device, you'll probably want to cut out the later shapes out of the lower shapes. Doing this is kind of tricky, and I'll go over two methods that work, with trade-offs and one complicated method that I haven't completed implementing. The code for this post is in my [python-embroidery](https://github.com/CatherineH/python-embroidery/) library. 

Subtract the Paths
==================

In SVGs, if you add one path string to another after the first string, SVG will render the second d string as a cut-out of the first d string. This means that you can go through the SVG paths and add the next two together:

```python
for i in range(1, len(all_paths)):
    remove_path = all_paths[i].d()
    current_path = all_paths[i-1].d()
    all_paths[i-1] = parse_path(current_path+" "+remove_path)
```

This works well for shapes without the holes, so for example the shape:

![svg rendering of a green star on a blue circle](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/cutting_svgs/stack1.png)

will be cut into the shapes:

![svg rendering of a green star cut out of a blue circle](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/cutting_svgs/stack_inversion_1.png)

However, for shapes that already have holes, like the shape:

![svg rendering of a green star on a blue ring](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/cutting_svgs/stack2.png)

will be cut into the shapes:

![svg rendering of a green star cut out of a blue ring incorrectly](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/cutting_svgs/stack_difference_2.png)

Cutting a path on an existing negative space turns it into a positive space. This makes sense if you have only an on or off setting for each fill area. So this method works well for simple shapes, but not for shapes that already have negative spaces. As soon as you try to stack multiple shapes, you're going to be double-negating lots of shapes.

Use Computational Geometry
==========================

Computational Geometry is a tricky subject, luckily we can leverage that is used extensively in GIS code to avoid doing our own calculations. The [Shapely](https://toblerity.org/shapely) python package has functions to perform all set operations on polygon points, including differencing. It doesn't support curves, so you must first convert the SVG paths into polygons, do the difference, then convert the polygon into an SVG path:


```python
from svgpathtools import Line, Path
from shapely.geometry import Polygon

def path_difference_shapely(path1, path2):
    # convert both paths to polygons
    def path_to_poly(inpath):
        points = []
        for path in inpath:
            if isinstance(path, Line):
                points.append([path.end.real, path.end.imag])
            else:
                num_segments = ceil(path.length() / minimum_stitch)
                for seg_i in range(int(num_segments + 1)):
                    points.append([path.point(seg_i / num_segments).real,
                                    path.point(seg_i / num_segments).imag])
        return Polygon(points)
    poly1 = path_to_poly(path1)
    poly2 = path_to_poly(path2)
    diff_poly = poly1.difference(poly2)
    points = diff_poly.exterior.coords
    new_path = []
    for i in range(len(points)-1):
        new_path.append(Line(start=points[i-1][0]+points[i-1][1]*1j,
                             end=points[i][0]+points[i][1]*1j))
    new_path.append(Line(start=points[-1][0]+points[-1][1]*1j,
                             end=points[0][0]+points[0][1]*1j))
    # make a new path from these points
    return Path(*new_path)
```

Here I'm sampling along any non-Line segments in the curve at intervals of **minimum_stitch**, which is the smallest stitch I'm going to tell my computerized sewing machine to make. 

This cuts out our negative space the way we'd like:

![svg rendering of a green star cut out of a blue ring correctly](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/cutting_svgs/shapely_stack_difference_2.png)

Which is what we want. Unfortunately, doing this requires transforming our wonderful continuous Bezier curves into gross discrete polygons. This isn't a problem if you know the lower resolution of the device that is going to render your SVG, like the minimum stitch of my sewing machine.

Use Inkscape
==================

So what if you want to preserve your curves? Inkscape is able to do differences between shapes remarkably well, unfortunately [their code](https://gitlab.com/inkscape/inkscape/blob/master/src/livarot/ShapeSweep.cpp#L838) for doing this is a thousand lines that is not linted, has no comments, and has methods and variables written in Franglish. Eventually, I'd like to understand what it is doing. Inkscape is a really wonderful tool and I understand that it is difficult to make a professional-level codebase on 0 income. If you want to just use Inkscape's operations in your python code, you can use the [inx-pathops](https://gitlab.com/su-v/inx-pathops) package.



