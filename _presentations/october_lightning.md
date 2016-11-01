---
author: Catherine Holloway
company: Qubitekk
twitter: femion
title: Honey I shrunk the Python
layout: bright


permalink: october_lightning.html

style: |
    #NoHeaderArduino h2,  #NoHeaderpyOpenGL h2, #NoHeaderpyOpenGL2 h2,
    #NoHeaderpyOpenGL2 h2, #NoHeaderpyOpenGL3 h2, #NoHeaderpyglet h2,
    #NoHeaderpyglet2 h2, #NoHeaderpyglet3 h2, #NoHeaderpyglet4 h2,
    #NoHeaderpythonmultiple h2, #NoHeaderpyOpenGLSmall h2,
    #NoHeaderphysics h2, #NoHeaderphysics2 h2{
        margin:0px 0 0;
        text-align:center;
        font-size:0px;
        }

    .leftcol {
        float: left;
    }
    .rightcol {
        float: right;
    }

    #NoHeaderpyOpenGLSmall code{
        font-size:14px;
    }

    #CodeSmallHeaderiterators h2{
        margin:0px 0 0;
        text-align:center;
        font-size:20px;
        }


    #Cover h2 {
        margin:30px 0 0;
        color:#FFF;
        text-align:center;
        font-size:70px;
        }
    #Cover p {
        margin:10px 0 0;
        text-align:center;
        color:#FFF;
        font-style:italic;
        font-size:20px;
        }
        #Cover p a {
            color:#FFF;
            }
---

# Honey I shrunk the Python {#Cover}
{: .slide .cover .w }

Catherine Holloway (@femion, CatherineH)

## Comparing Pis to teensies

<table border="0">
<tr><td><img width="400" src="https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_presentations/october_lightning/raspberry_pi.jpg"></td><td><img width="400" src="https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_presentations/october_lightning/teensyparts.jpg"></td></tr>
</table>

Images from Adafruit

## Pis to Teensies {#NoHeaderArduino}

<table border="0">
<tr><td></td><td>Raspberry Pi Zero*</td><td>Teensy 3.2</td></tr>
<tr><td>Price</td><td>5$ (20$) + 5$</td><td><b>12$ (20$)</b></td></tr>
<tr><td>Boot time</td><td>35 s </td><td> <b>< 1 s</b></td></tr>
<tr><td>Digital I/O</td><td>18 pins </td><td><b> 34 pins</b></td></tr>
<tr><td>Digital I/O speed</td><td><b>22 MHz**</b></td><td>115 kHz</td></tr>
<tr><td>Analog I/O</td><td>None </td><td><b> 14 pins</b></td></tr>
<tr><td>Storage</td><td><b>14 GB</b></td><td>262 kB</td></tr>
<tr><td>RAM</td><td><b>512 MB</b></td><td>64 kB</td></tr>
</table>

\* 16 Gb storage card with Rasbpian lite 
\*\* C + RasPi hardware libraries

## Use the Pi Zero when you:

- don't need **analog input**
- want to use existing **linux libraries**
- have a device that will stay **on all the time**
- need **fast** digital electronics communication (and can program in C)
- need a lot of **storage** or **RAM**

## Use the Teensy when you:

- need **analog I/O** or a lot of **digital I/O**
- need to **security audit** your code
- will be turning your **device on and off** frequently

## MicroPython: an alternative to C++

- original kickstarter by Damien George, a **physicist** at Cambridge
- used by the BBC micro:bit
- compatible with the Teensy 3.+ (but not the LC... yet?)
- stripped-down standard library

## Interactive MicroPython Prompt

( show serial connection)

## boot.py and main.py

- boot executes first, then main
- add to hex and upload!
(show code for other board) 

## For more...

- Blog post on setting up toolchain: http://**catherineh**.github.io/programming/2016/09/18/getting-started-with-micropython-on-the-teensy.html
- my MicroPython demo board: **micropython-teensy-demo**
- my fake-micropython tool: **fake-micropython**
- my teensy build scripts: **teensy-python-makefile**






