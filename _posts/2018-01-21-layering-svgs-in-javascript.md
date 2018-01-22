---
layout: post
title: "Layering SVGs in JavaScript"
description: ""
category: programming
tags: [svg, web development, javascript]
---
{% include JB/setup %}

If you want to create or manipulate SVGs, there several great JavaScript libraries, such
as [d3](https://d3js.org/) or [Snap.js](http://snapsvg.io/). However, right now I just
want to stack a set of already-existing SVGs. I've created a
[gist](https://gist.github.com/CatherineH/5d923ec585acdb89ab2df34c095a681c) with my code
to stack SVGs, I'm going to go over it in this post.

This post assumes that the SVGs to stack are the strings of the file contents of the SVGs.
 You can acquire these strings by either reading in a user-supplied input file, or by
 making an HTTP request, but that is beyond the scope of this post.

Quick and Dirty
---------------

To extract the svg contents out of a string, you could do some string manipulations to
strip everything up to the opening \<svg\> tag and after the closing \</svg\> tag. But
since JavaScript was created with the goal of being able to manipulate XML files, this
seems unnecessary. Instead, I use the DOMParser object to extract the SVG contents:

```javascript
function getSVGContents(inputString){
    let domParser = new DOMParser();
    let svgDOM = domParser.parseFromString(inputString, 'text/xml')
        .getElementsByTagName('svg')[0];
    return svgDOM.innerHTML
}
```

Then, you can simply concatenate the strings:

```javascript
document.getElementById("quickSVG").innerHTML =
         getSVGContents(circle)+getSVGContents(star);
```

SVGs have no z-index, like CSS. The elements that appear on the top are just the last
elements to be added. So the above code would create the svg:

![star over circle SVG](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/layering_svgs/star_over_circle.png)

Whereas if you change the order of 'circle' and 'star' in the string concatenation:

```javascript
document.getElementById("quickSVG").innerHTML =
         getSVGContents(star)+getSVGContents(circle);
```

The star will now be under the circle:

![circle over star SVG](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/layering_svgs/circle_over_star.png)

Less Quick, more OOPy
---------------------

The above method is okay if you want to just layer the SVGs without manipulating them.
But since we already have our strings parsed to DOM elements, we can combine the elements
directly. We can initialize a SVG element, then use *appendChild* to move the child nodes
from one element to another:

```javascript
function addSVGs(inputStrings){
    // takes a list of strings of SVGs to merge together into one large element
    let svgMain = document.createElement("svg");
    for(let stringI=0;stringI<inputStrings.length;stringI++){
        let domParser = new DOMParser();
        let svgDOM = domParser.parseFromString(inputStrings[stringI], 'text/xml')
            .getElementsByTagName('svg')[0];
        while(svgDOM.childNodes.length>0){
            svgMain.appendChild(svgDOM.childNodes[0]);
        }
    }
    return svgMain

}
var svgMain = addSVGs([circle, star]);
document.getElementById("appendSVG").innerHTML = svgMain.innerHTML;
```

The things I found confusing about this method were twofold:

- first, unlike other XML parsers, DOMParser does not ignore whitespace. The tabs I put
in to make my SVG strings more readable get read in as **#text** nodes. These strings will
get rendered as whitespace, which don't effect the final SVG.
- **appendChild** removes the element from the input element's parent, hence why it's the
first childNodes added to the mainSVG, and why I keep appending until there are no more
childNodes in the svgDOM.
