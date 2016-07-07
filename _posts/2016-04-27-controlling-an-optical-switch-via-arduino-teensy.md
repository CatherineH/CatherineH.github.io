---
layout: post
title: "Controlling an Optical Switch via Arduino (Teensy)"
description: ""
category: programming
tags: [electronics, C, python, InstrumentKit]
---
{% include JB/setup %}

Aside from fingerprints, there is nothing more annoying, or more damaging to optics equipment than unplugging and
plugging in fiber optics. Every time a fiber tip or port is exposed to air, there's a chance of getting gross human skin
 cells on places where tightly focused high-power light might incinerate them, yet, so many experiments require routing
 light. Wouldn't it be nicer if a robot did the switching for you at 2 am while your gross dust and sweat producing body
  is sleeping?

In experiments, I accomplish this using a teensy LC and a DiCon optical switch.

Electronics Side
================

The optical switch I use is a [DiCon 2x2 prism switch](http://www.diconfiberoptics.com/products/scd0009/scd0009f.pdf),
which is essentially a little piece of glass on a motor.

![A picture of a DiCon fiber optic switch](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/dicon_switch.jpg)

This switch will operate in several modes, but in every mode the first two (blue and purple) pins are used to set the
position and the second two (red and green) pins are used to read the position of the switch.

I chose to operate the switch in *Non-latching 2-pin Control* mode, because it was the least complicated.

I chose to put the two pins that should never change in control mode (purple should always be ground, red should always
be +5V) and the two pins with changing values (blue and green) on the other. This led to a lot of initial confusion, but
 I believe it was a good decision to because it allows me to keep the two pins that need to be hooked up to some external logic together.

![A picture of the headers going into the teensy](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/teensy_switch.jpg)

The threshold voltage for switching is above 3.3V, which is the maximum that the Teensy's output pins can supply. Thus,
I chose to use a solid state relay to bump the signal up to 5V. I use Sharp Microelectronics
[R22MA1](http://www.digikey.com/product-detail/en/sharp-microelectronics/PR22MA11NTZF/425-2602-5-ND/856883) because
they're super cheap (25.65$ for 50) and I have a tendency to accidentally blow electronics up.

My prototype board looks like this:

![Fritzing image of breadboard](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/switch_bb.png)

Imagine the Sharp SSR on the breadboard instead of the Omron SSR. You'll notice that I have left the green pin
unconnected. The switch has always activated when 5V, thus the position information isn't useful right now.

Arduino Code
============

This teensy is also used to control several other pieces of experimental hardware, so I've excerpted it here.

I want to be able to read the current position state and write a new position state using a SCPI-compliant serial
connection.

My .ino code looks like this:

```
#include "scpi_comm.h"
#include "optical_switch.h"
int switch_led_pin = 13;
int out_pin = 9;
settings _settings = {.switch_setting = 1, .motor = _state};

void setup()
{
  Serial.begin(9600);
  pinMode(switch_led_pin, OUTPUT);
  pinMode(out_pin, OUTPUT);
}

void loop()
{
  update_optical_switch(_settings.switch_setting, out_pin, switch_led_pin);
  if (Serial.available() > 0) {
    comm_protocol(Serial.read(), &_settings);
  }
}
```

My *scpi_comm.h* contains an internal state machine which collects characters into a string until the termination
character is received, then attempts to parse the string:

```
typedef struct {
  int switch_setting;
} settings;

char terminationByte = '\r';
int incomingByte = 0;
int string_pos = 0;
int current_state = 1;
char line[15];
char serialsecond[5];
char input_str[8];
char output_str[8];

void comm_protocol(byte incomingByte, settings *settings){
   line[string_pos] = incomingByte;
   string_pos += 1;
   if(incomingByte == terminationByte)
   {
     if(strncmp(line, ":OUTP", 5)==0)
     {
         char * loc = strchr(line, ':');
          loc = strchr(loc+1, ' ');
          memcpy(serialsecond, loc+1, 3);
          if(strncmp(serialsecond, "1", 1) == 0)
          {
             settings->switch_setting = 1;
          }
          else
          {
            settings->switch_setting = 0;
          }
          sprintf(output_str, "Set Switch to %d%c", settings->switch_setting, terminationByte);
          Serial.write(output_str);
     }
     else if(strncmp(line, "OUTP", 4)==0 && strpbrk(line, "?") != 0)
     {
         sprintf(output_str, "%d%c",  settings->switch_setting, terminationByte);
         Serial.write(output_str);
     }
     else{
        sprintf(output_str, "Unknown command%c", terminationByte);
        Serial.write(output_str);
     }
     // reset the string
     string_pos = 0;
     line[0] = '\0';
   }
}
```

Lastly, my *optical_switch.h* code simply reads the settings and makes the Teensy's indicator LED also go high when the
switch position is high:

```
void update_optical_switch(int optical_state, int switch_pin, int led_pin)
{
  if(optical_state==1)
  {
    digitalWrite(switch_pin, HIGH);
    digitalWrite(led_pin, HIGH);
  }
  else
  {
    digitalWrite(switch_pin, LOW);
    digitalWrite(led_pin, LOW);
  }
}
```