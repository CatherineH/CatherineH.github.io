---
layout: post
title: "PNGs to Embroidery Patterns"
description: ""
category: programming
tags: [python, svg]
---
{% include JB/setup %}

Within five minutes of releasing the first version of my web interface to my [python-embroidery](https://github.com/CatherineH/python-embroidery/) package, [embroidery-maker.com](https://embroidery-maker.com), it was broken by my first user uploading a PNG image instead of an SVG. Though SVGs are much easier to work with, as the list of stitches that gets sent to the sewing machine is much closer in data to a vector than a grid of pixels, I recognize that my user-base is more familiar with opening and editing PNGs than SVGs. Luckily adding support for PNGs was relatively painless thanks to the [Potrace](http://potrace.sourceforge.net) contour-tracing tool, and the [python bindings](https://github.com/flupke/pypotrace).


First, I convert the individual pixels in the image into valid thread colors. At this point, it might also be useful to restrict the total number of colors in the image, which can be done using the Python Imaging Library's *convert* method. My sewing machine seems willing to support an arbitrarily large number of different thread colors in patterns, but it can be a pain to have to take out and re-thread the machine many times.

```python
def posturize(_image):
    pixels = defaultdict(list)
    for i, pixel in enumerate(_image.getdata()):
        x = i % _image.size[0]
        y = int(i/_image.size[0])
        if len(pixel) > 3:
            if pixel[3] == 255:
                pixels[nearest_color(pixel)].append((x,y, pixel))
        else:
            pixels[nearest_color(pixel)].append((x, y, pixel))
    return pixels
```

Next, I trace the image. Potrace can only handle two-color images, so I keep track of all of the thread colors, then go make a masked image with only the pixels of that thread color. 

```python
for color in pixels:
    data = zeros(_image.size, uint32)
    for pixel in pixels[color]:
        data[pixel[0], pixel[1]] = 1
    # Create a bitmap from the array
    bmp = potrace.Bitmap(data)
    # Trace the bitmap to a path
    path = bmp.trace()
```

Next, I want to convert this traced path into the [svgpathtools](https://github.com/CatherineH/svgpathtools) curve objects, so that they can be used in the rest of the digitizer code as if it was parsed in from an SVG. I also need to keep track of the start locations of each segment, so that I can check whether the segment is a closed loop. If it is, I can add a fill and stroke color.
 
```python
# Iterate over path curves
for curve in path:
    svg_paths = []
    start_point = curve.start_point
    true_start = curve.start_point
    for segment in curve:
        if true_start is None:
            true_start = segment.start_point
        if start_point is None:
            start_point = segment.start_point
        if isinstance(segment, BezierSegment):
            svg_paths.append(
                CubicBezier(start=start_point[1] + 1j * start_point[0],
                            control1=segment.c1[1] + segment.c1[0] * 1j,
                            control2=segment.c2[1] + segment.c2[0] * 1j,
                            end=segment.end_point[1] + 1j * segment.end_point[0]))
        elif isinstance(segment, CornerSegment):
            svg_paths.append(Line(start=start_point[1] + 1j * start_point[0],
                                  end=segment.c[1] + segment.c[0] * 1j))
            svg_paths.append(Line(start=segment.c[1] + segment.c[0] * 1j,
                                  end=segment.end_point[1] + 1j *
                                                             segment.end_point[
                                                                 0]))
        else:
            print("not sure what to do with: ", segment)
        start_point = segment.end_point
        # is the path closed?
        if true_start == start_point:
            output_paths.append(Path(*svg_paths))
            color = pixel[2]
            rgb = "#%02x%02x%02x" % (color[0], color[1], color[2])
            fill = rgb
            attributes.append({"fill": fill, "stroke": rgb})
            true_start = None
            start_point = None
            svg_paths = []
```

Then, I need to [cut the shapes above out of the shapes below](http://catherineh.github.io/programming/2018/04/03/25-ways-of-cutting-svg-shapes) so that the SVG is only one layer deep.

Feeding these paths into my digitizer, it can turn PNG images like<sup>[1](#myfootnote120180404)</sup>:

![the flag of Nova Scotia with an emoji cat face](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/digitizing_images/emoji_flag.png)

into:

![the flag of Nova Scotia with an emoji cat face, as a series of stitches](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/digitizing_images/ns_flag_emoji.png)

<a name="myfootnote120180404">1</a>: I've replaced the lion rampant on the flag of Nova Scotia with the emoji cat because it has too many curves to render nicely in stitches, and also because it amuses me


