---
layout: post
title: "Finding mounted drives by USB Product or Vendor id"
description: "kind of a hack"
category: programming
tags: [python, hardware, usb]
---
{% include JB/setup %}

I recently purchased a [Computerized Sewing Machine](https://www.amazon.com/Brother-LB6800PRW-Computerized-Embroidery-Sewing/dp/B003EPLBMO/). Designs can be uploaded to internal storage via USB, which ubuntu automatically recognizes and mounts:

![my ubuntu ultrabook and my brother sewing machine](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/brother_sewing.jpg)

This compatibility with linux out of the box is fantastic; unfortunately designs must be in Brother's undocumented binary file format, and the sewing machine gives no feedback regarding parsing errors. This means that I've been creating binaries for embroidery patterns with a lot of trial and error. In order to script some of the process, I'd like to upload and test new designs without human intervention.

To find where ubuntu has mounted the sewing machine, I could either: 

1. write some udev rules
2. get python to figure it out from linux commands

In this case, method 2 is a bit nicer since I'm already using Python to generate the binary files. 

First, I use the output of df to generate a mapping of where ubuntu has mounted the external drives:

```python
mount_points = {}
out = check_output(["df"]).split("\n")
for line in out:
    if line.find("/media") >= 0:
        mount_location = line.split("%")[-1]
        line = line.split(" ")
        mount_points[line[0]] = mount_location.strip()
```

Next, get the vendor ids for each device, and if it matches, call that my mount location:

```python
mount_destination = None
for mount_point in mount_points:
    out = check_output(["udevadm", "info", "--name="+mount_point, "--attribute-walk"])
    if out.find('ATTRS{idVendor}=="04f9"')> 0:
        print("found brother device, assuming embroidery machine")
        mount_destination = mount_points[mount_point]
        break
```

So I can now use *shutil.copyfile()* to move the files over to *mount_destination*. This is kind of a hacky solution because it may also catch Brother printers, or fail to recognize embroidery machines from other manufacturers, but since I have neither of these situations, it's good enough for now.


