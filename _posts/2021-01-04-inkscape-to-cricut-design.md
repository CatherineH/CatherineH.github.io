---
layout: post
title: "Inkscape to Cricut Design"
description: ""
category: 
tags: [svg, cricut, inkscape]
---
{% include JB/setup %}
[Cricut Design Space](https://design.cricut.com/), the software used to send designs to Cricut cutting plotters, does not handle the transform element on svg very well, which is frustrating because Inkscape loves to render paths with that attribute, rather than applying the transform directly to the path or object.

For example, here's a design I made in inkscape. It has one path object representing the cuts I want to make in a piece of yellow cardstock on the bottom layer, and one group of paths 
to be traced out with a marker on the top layer:

![a screenshot from inkscape](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/cricut_transforms/inkscape_render.PNG)

However, this fails to render correctly in Cricut Design Space:

![failed render](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/cricut_transforms/failed_transform_inkscape.PNG)

The telltale sign about why this is rendered like this is to look at whether a transformation matrix is being applied to this element:

```svg
    <g
       id="g6018"
       transform="matrix(0.3071252,0.01878458,-0.01878458,0.3071252,92.391111,151.00958)"
       style="stroke-width:0.831982;stroke-miterlimit:4;stroke-dasharray:none">
```

There are also transforms applied to layers:

```svg	  
  <g
     inkscape:label="Layer 1"
     inkscape:groupmode="layer"
     id="layer1"
     transform="translate(-24.058,-19.5223)"
     style="display:inline">
```

Some transforms Cricut Design Space can handle okay, but some it cannot. A way I fixed the transforms on this project was:

1. put all elements on the same layer
2. ungroup the line patterns, then group them again

Now it renders as expected:

![after group removal](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/cricut_transforms/after_removal.PNG)

Cricut also can't handle the **rotate** transform. For example, I created a tiling that uses the rotate transform to put the trapezoids in the right place. But in Cricut, the trapezoids ignore this rotation, and all stack on top of each other:

![rotation parsed badly](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/cricut_transforms/trapezoid_ungrouped.PNG)

Unfortunately, there's no ungrouping as a way to get out of this. Fortunately there's a really nice extension called [Apply Transforms](https://github.com/Klowner/inkscape-applytransforms) that will take the the transform and apply it to the path itself. Now the tiling renders correctly:

![rotation parsed correctly](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/cricut_transforms/trapezoid_transform_applied.PNG)



	 