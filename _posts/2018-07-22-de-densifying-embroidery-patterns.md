---
layout: post
title: "De densifying Embroidery Patterns"
description: "saving needles"
category: programming
tags: [sewing, python, embroidery]
---
{% include JB/setup %}

My [python automatic digitizer](https://github.com/CatherineH/python-embroidery) can now turn pngs, text, and a SVGs produced by a variety of software into computerized sewing machine embroidery patterns. However, I am hesitant to release and advertise this project because every other pattern ends up breaking a needle when loaded onto a sewing machine. Though needles are 25 cents each, it breaks the thread, and pieces of the need can end up lost under the base plate. My sewing machine manual suggests that this happens because there are three layers of threads. 

I wrote some python code to measure the density of stitches. The heatmap looks like:

![density of stitches](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/dedensifying_patterns/density_before.png)

Some locations in the pattern have more than 7 points - and that location corresponds to the point where the needle breaks on the sewing machine. My strategy for reducing the density is discretize the pattern into a grid, and move the fourth stitch on every grid location to the next nearest grid location with fewer than three stitches. To do this, I create a generator:

```python
# spiral around a point until you find the next available location
class NextAvailableGrid(object):
    def __init__(self, i, j):
        self.i = i # i is the x coordinate
        self.j = j # j is the y coordinate
        self.direction = "left"
        self.stepsize = 1
        self.current_step = 0

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        directions = ["left", "down", "right", "up"] # go counter-clockwise
        # do the transforms
        if self.direction == "left":
            self.i += 1
        if self.direction == "down":
            self.j += 1
        if self.direction == "right":
            self.i -= 1
        if self.direction == "up":
            self.j -= 1
        self.current_step += 1
        if self.current_step == self.stepsize:
            self.direction = directions[(directions.index(self.direction) + 1)
                                        % len(directions)]
            self.current_step = 0
            if self.direction in ["right", "left"]:
                self.stepsize += 1

        return self.i, self.j
```

This will spiral out from the grid location i, j forever:

![grid spiral](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/dedensifying_patterns/next_available_grid.png)


Then, the code to move the stitches is:

```python
def de_densify(pattern):
    density, boundx, boundy, x_bins, y_bins = initialize_grid(pattern)
    # convert the density list of lists to a dict
    density = {i: {j: block for j, block in enumerate(density[i])}
               for i in range(len(density))}
    for block_i, block in enumerate(pattern.blocks):
        for stitch_i, stitch in enumerate(block.stitches):
            i = int((stitch.x - boundx[1]) / minimum_stitch)
            j = int((stitch.y - boundy[1]) / minimum_stitch)
            # if there is room for that stitch, continue
            if density[j][i] <= MAX_STITCHES:
                density[j][i] += 1
                continue
            for next_i, next_j in NextAvailableGrid(i, j):
                if density[next_j][next_i] >= MAX_STITCHES:
                    continue
                print("moving stitch from {} {}".format(stitch.x, stitch.y))
                pattern.blocks[block_i].stitches[stitch_i].x = next_i * minimum_stitch + boundx[1]
                pattern.blocks[block_i].stitches[stitch_i].y = next_j * minimum_stitch + \
                                                               boundy[1]
                print("to {} {}".format(pattern.blocks[block_i].stitches[stitch_i].x, pattern.blocks[block_i].stitches[stitch_i].y))
                density[next_j][next_i] += 1
                break
    return pattern
```

The density map after moving the stitches is:

![density of stitches after](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/dedensifying_patterns/density_after.png)


And this gets stitched out without breaking a needle:

![stitched out pattern](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/dedensifying_patterns/python_pattern.jpg)

It's still not where I want it - the jumps are too large and the threads cross over each other too frequently, but stitching without needle breaks is progress.

