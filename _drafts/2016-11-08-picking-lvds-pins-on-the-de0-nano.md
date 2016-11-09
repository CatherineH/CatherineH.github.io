---
layout: post
title: "Picking LVDS pins on the DE0 Nano"
description: ""
category: programming 
tags: [fpga, verilog]
---
{% include JB/setup %}


Suppose you want to annoy the people around you by running as many speakers or HDMI displays as possible at the same time off of your DE0-Nano Cyclone-IV based FPGA development board. Figuring out where to plug in your HDMI pins is stricky because is tricky because Altera provides little documentation on exactly which pins in which banks on the Cyclone IV E chip can support LVDS, many pins are already routed to the peripherals on the DE0 Nano, some pins are input-only, and LVDS pins must be at least 4 spaces from any other signal pins. In this post, through a lot of trial and error and fussing with the pin planner, I'll document everything I know about which pins can be used.

Assigning LVDS Pins
===================

Quartus' pin planner is frustrating and often behaves unpredictably, especially when assigning pins in pairs. I would not recommend using it.

You can get around it by adding the following lines:

```
set_instance_assignment -name IO_STANDARD LVDS -to HDMI[0]
set_location_assignment PIN_K15 -to HDMI[0]
set_location_assignment PIN_K16 -to "HDMI[0](n)"
```

to a *.tcl* file, which you can then add to your project by adding the line:

```
set_global_assignment -name SOURCE_TCL_SCRIPT_FILE pins.tcl
```

to your project's *.qsf* file. Alternatively, you can always directly copy and paste these lines into the *.qsf* file, but I like to keep them separate for readability.

Pin Survivor
============

Out of the 256 pins on the Cyclone IV 4 EP4CE22 device, here are the 47 LVDS pairs:

$ALL_PINS$

Removing all pins not accessible through JP1, JP2, and JP3 on the DE0-Nano leaves us with 19 pairs:

$ACCESSIBLE_PINS$ 

Certain pins are input only. Assuming that you want output, the table reduces only six outputs: 

$OUTPUT_PINS$

Which means you can ultimately only run one HDMI cable + 2 speakers off of your DE0-Nano.

I've highlighted which pins these are here:

![de0 nano with lvds pairs highlighted](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/de0nano_lvds/lvds_pins.png)

White borders indicate p, black borders indicate n. The colours correspond to <span style="color:blue">K15, K16</span>, <span style="color:red">N15, N16</span>, <span style="color:yellow">R16, P16</span>, <span style="color:green"> L15, L16 </span>, <span style="color:magenta">F15, F16</span> and <span style="color:aqua">G15, G16</span>. 

Finally, LVDS pins must be at least 4 pins away from any other used outputs. That means you may have trouble using KEY[0] and the (K15, K16) LVDS pins simultaneously, and as well as using (F15, F16) or (G15, G16) pin pairs simultaneously. Sometimes the fitter is able to cram both all pins on the same design, sometimes it can't. Several of the DRAM pins look close to the LVDS ports, but I haven't extensively studied which ones.

Re-Assigning pin F16
====================

If you use pin F15/F16, you'll have to re-assign it off of the programming pin, or else you'll get the error:

```
Error (169014): Cannot place node ~ALTERA_nCEO~ in location F16 because location already occupied by node HDMI[0](n)
```

You can fix this by adding the line:

```
set_global_assignment -name CYCLONEII_RESERVE_NCEO_AFTER_CONFIGURATION "USE AS REGULAR IO"
```

to your *tcl* or *qsf* file.

The TCL File
============

Here's the tcl file for declaring these pins:

```
set_global_assignment -name CYCLONEII_RESERVE_NCEO_AFTER_CONFIGURATION "USE AS REGULAR IO"
set_instance_assignment -name IO_STANDARD LVDS -to LVDSO[0]
set_location_assignment PIN_G15 -to LVDSO[0]
set_location_assignment PIN_G16 -to "LVDSO[0](n)"
set_instance_assignment -name IO_STANDARD LVDS -to LVDSO[1]
set_location_assignment PIN_N15 -to LVDSO[1]
set_location_assignment PIN_N16 -to "LVDSO[1](n)"
set_instance_assignment -name IO_STANDARD LVDS -to LVDSO[2]
set_location_assignment PIN_R16 -to LVDSO[2]
set_location_assignment PIN_P16 -to "LVDSO[2](n)"
set_location_assignment PIN_R8 -to clock_50
set_instance_assignment -name IO_STANDARD LVDS -to LVDSO[3]
set_location_assignment PIN_L15 -to LVDSO[3]
set_location_assignment PIN_L16 -to "LVDSO[3](n)"
set_instance_assignment -name IO_STANDARD LVDS -to LVDSO[4]
set_location_assignment PIN_K15 -to LVDSO[4]
set_location_assignment PIN_K16 -to "LVDSO[4](n)"
set_instance_assignment -name IO_STANDARD LVDS -to LVDSO[5]
set_location_assignment PIN_F15 -to LVDSO[5]
set_location_assignment PIN_F16 -to "LVDSO[5](n)"
```


