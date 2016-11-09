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

<table border="1"><tr><td style = "background-color: #AAFFA0;">(A10,	B10)</td><td style = "background-color: #AAFFA0;">(A11,	B11)</td><td style = "background-color: #AAFFA0;">(A12,	B12)</td><td style = "background-color: #AAFFA0;">(A13,	B13)</td><td style = "background-color: #AAFFA0;">(A2,	A3)</td><td style = "background-color: #AAFFA0;">(A4,	B4)</td><td style = "background-color: #AAFFA0;">(A5,	B5)</td><td style = "background-color: #AAFFA0;">(A6,	B6)</td></tr><tr><td style = "background-color: #AAFFA0;">(A7,	B7)</td><td style = "background-color: #AAFFA0;">(A8,	B8)</td><td style = "background-color: #AAFFA0;">(A9,	B9)</td><td style = "background-color: #AAFFA0;">(C1,	C2)</td><td style = "background-color: #AAFFA0;">(C14,	D14)</td><td style = "background-color: #AAFFA0;">(C16,	C15)</td><td style = "background-color: #AAFFA0;">(C9,	D9)</td><td style = "background-color: #AAFFA0;">(D1,	D2)</td></tr><tr><td style = "background-color: #AAFFA0;">(D11,	D12)</td><td style = "background-color: #AAFFA0;">(E16,	E15)</td><td style = "background-color: #AAFFA0;">(E8,	F8)</td><td style = "background-color: #AAFFA0;">(F1,	F2)</td><td style = "background-color: #AAFFA0;">(F16,	F15)</td><td style = "background-color: #AAFFA0;">(G1,	G2)</td><td style = "background-color: #AAFFA0;">(G16,	G15)</td><td style = "background-color: #AAFFA0;">(J1,	J2)</td></tr><tr><td style = "background-color: #AAFFA0;">(J16,	J15)</td><td style = "background-color: #AAFFA0;">(K1,	K2)</td><td style = "background-color: #AAFFA0;">(K16,	K15)</td><td style = "background-color: #AAFFA0;">(L1,	L2)</td><td style = "background-color: #AAFFA0;">(L16,	L15)</td><td style = "background-color: #AAFFA0;">(M1,	M2)</td><td style = "background-color: #AAFFA0;">(M16,	M15)</td><td style = "background-color: #AAFFA0;">(N1,	N2)</td></tr><tr><td style = "background-color: #AAFFA0;">(N16,	N15)</td><td style = "background-color: #AAFFA0;">(N6,	N5)</td><td style = "background-color: #AAFFA0;">(P1,	P2)</td><td style = "background-color: #AAFFA0;">(P16,	R16)</td><td style = "background-color: #AAFFA0;">(P3,	N3)</td><td style = "background-color: #AAFFA0;">(T10,	R10)</td><td style = "background-color: #AAFFA0;">(T11,	R11)</td><td style = "background-color: #AAFFA0;">(T12,	R12)</td></tr><tr><td style = "background-color: #AAFFA0;">(T13,	R13)</td><td style = "background-color: #AAFFA0;">(T15,	T14)</td><td style = "background-color: #AAFFA0;">(T3,	R3)</td><td style = "background-color: #AAFFA0;">(T5,	R5)</td><td style = "background-color: #AAFFA0;">(T6,	R6)</td><td style = "background-color: #AAFFA0;">(T7,	R7)</td><td style = "background-color: #AAFFA0;">(T9,	R9)</td><td></td></tr></table>

Removing all pins not accessible through JP1, JP2, and JP3 on the DE0-Nano leaves us with 19 pairs:

<table border="1"><tr><td style = "background-color: #FFAAA0;">(A10,	B10)</td><td style = "background-color: #AAFFA0;">(A11,	B11)</td><td style = "background-color: #FFAAA0;">(A12,	B12)</td><td style = "background-color: #FFAAA0;">(A13,	B13)</td><td style = "background-color: #AAFFA0;">(A2,	A3)</td><td style = "background-color: #AAFFA0;">(A4,	B4)</td><td style = "background-color: #AAFFA0;">(A5,	B5)</td><td style = "background-color: #AAFFA0;">(A6,	B6)</td></tr><tr><td style = "background-color: #AAFFA0;">(A7,	B7)</td><td style = "background-color: #AAFFA0;">(A8,	B8)</td><td style = "background-color: #FFAAA0;">(A9,	B9)</td><td style = "background-color: #FFAAA0;">(C1,	C2)</td><td style = "background-color: #FFAAA0;">(C14,	D14)</td><td style = "background-color: #FFAAA0;">(C16,	C15)</td><td style = "background-color: #FFAAA0;">(C9,	D9)</td><td style = "background-color: #FFAAA0;">(D1,	D2)</td></tr><tr><td style = "background-color: #FFAAA0;">(D11,	D12)</td><td style = "background-color: #FFAAA0;">(E16,	E15)</td><td style = "background-color: #FFAAA0;">(E8,	F8)</td><td style = "background-color: #FFAAA0;">(F1,	F2)</td><td style = "background-color: #AAFFA0;">(F16,	F15)</td><td style = "background-color: #FFAAA0;">(G1,	G2)</td><td style = "background-color: #AAFFA0;">(G16,	G15)</td><td style = "background-color: #FFAAA0;">(J1,	J2)</td></tr><tr><td style = "background-color: #FFAAA0;">(J16,	J15)</td><td style = "background-color: #FFAAA0;">(K1,	K2)</td><td style = "background-color: #AAFFA0;">(K16,	K15)</td><td style = "background-color: #FFAAA0;">(L1,	L2)</td><td style = "background-color: #AAFFA0;">(L16,	L15)</td><td style = "background-color: #FFAAA0;">(M1,	M2)</td><td style = "background-color: #FFAAA0;">(M16,	M15)</td><td style = "background-color: #FFAAA0;">(N1,	N2)</td></tr><tr><td style = "background-color: #AAFFA0;">(N16,	N15)</td><td style = "background-color: #FFAAA0;">(N6,	N5)</td><td style = "background-color: #FFAAA0;">(P1,	P2)</td><td style = "background-color: #AAFFA0;">(P16,	R16)</td><td style = "background-color: #FFAAA0;">(P3,	N3)</td><td style = "background-color: #AAFFA0;">(T10,	R10)</td><td style = "background-color: #AAFFA0;">(T11,	R11)</td><td style = "background-color: #AAFFA0;">(T12,	R12)</td></tr><tr><td style = "background-color: #AAFFA0;">(T13,	R13)</td><td style = "background-color: #AAFFA0;">(T15,	T14)</td><td style = "background-color: #FFAAA0;">(T3,	R3)</td><td style = "background-color: #FFAAA0;">(T5,	R5)</td><td style = "background-color: #FFAAA0;">(T6,	R6)</td><td style = "background-color: #FFAAA0;">(T7,	R7)</td><td style = "background-color: #AAFFA0;">(T9,	R9)</td><td></td></tr></table> 

Certain pins are input only. Assuming that you want output, the table reduces only six outputs: 

<table border="1"><tr><td style = "background-color: #FFAAA0;">(A10,	B10)</td><td style = "background-color: #FFAAA0;">(A11,	B11)</td><td style = "background-color: #FFAAA0;">(A12,	B12)</td><td style = "background-color: #FFAAA0;">(A13,	B13)</td><td style = "background-color: #FFAAA0;">(A2,	A3)</td><td style = "background-color: #FFAAA0;">(A4,	B4)</td><td style = "background-color: #FFAAA0;">(A5,	B5)</td><td style = "background-color: #FFAAA0;">(A6,	B6)</td></tr><tr><td style = "background-color: #FFAAA0;">(A7,	B7)</td><td style = "background-color: #FFAAA0;">(A8,	B8)</td><td style = "background-color: #FFAAA0;">(A9,	B9)</td><td style = "background-color: #FFAAA0;">(C1,	C2)</td><td style = "background-color: #FFAAA0;">(C14,	D14)</td><td style = "background-color: #FFAAA0;">(C16,	C15)</td><td style = "background-color: #FFAAA0;">(C9,	D9)</td><td style = "background-color: #FFAAA0;">(D1,	D2)</td></tr><tr><td style = "background-color: #FFAAA0;">(D11,	D12)</td><td style = "background-color: #FFAAA0;">(E16,	E15)</td><td style = "background-color: #FFAAA0;">(E8,	F8)</td><td style = "background-color: #FFAAA0;">(F1,	F2)</td><td style = "background-color: #AAFFA0;">(F16,	F15)</td><td style = "background-color: #FFAAA0;">(G1,	G2)</td><td style = "background-color: #AAFFA0;">(G16,	G15)</td><td style = "background-color: #FFAAA0;">(J1,	J2)</td></tr><tr><td style = "background-color: #FFAAA0;">(J16,	J15)</td><td style = "background-color: #FFAAA0;">(K1,	K2)</td><td style = "background-color: #AAFFA0;">(K16,	K15)</td><td style = "background-color: #FFAAA0;">(L1,	L2)</td><td style = "background-color: #AAFFA0;">(L16,	L15)</td><td style = "background-color: #FFAAA0;">(M1,	M2)</td><td style = "background-color: #FFAAA0;">(M16,	M15)</td><td style = "background-color: #FFAAA0;">(N1,	N2)</td></tr><tr><td style = "background-color: #AAFFA0;">(N16,	N15)</td><td style = "background-color: #FFAAA0;">(N6,	N5)</td><td style = "background-color: #FFAAA0;">(P1,	P2)</td><td style = "background-color: #AAFFA0;">(P16,	R16)</td><td style = "background-color: #FFAAA0;">(P3,	N3)</td><td style = "background-color: #FFAAA0;">(T10,	R10)</td><td style = "background-color: #FFAAA0;">(T11,	R11)</td><td style = "background-color: #FFAAA0;">(T12,	R12)</td></tr><tr><td style = "background-color: #FFAAA0;">(T13,	R13)</td><td style = "background-color: #FFAAA0;">(T15,	T14)</td><td style = "background-color: #FFAAA0;">(T3,	R3)</td><td style = "background-color: #FFAAA0;">(T5,	R5)</td><td style = "background-color: #FFAAA0;">(T6,	R6)</td><td style = "background-color: #FFAAA0;">(T7,	R7)</td><td style = "background-color: #FFAAA0;">(T9,	R9)</td><td></td></tr></table>

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


