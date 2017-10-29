---
layout: post
title: "Is it better to bake cookies in a toaster oven?"
description: ""
category: programming 
tags: [open-zwave, python, zwave]
---
{% include JB/setup %}
My husband and I disagree about whether it's more energy efficient to use our toaster oven or our regular oven for baking. He believes the toaster oven consumes less energy, since the volume is much smaller than the oven. I believe the oven is better to use the oven, since the insulation is much better.

I did some back-of-the-envelope calculations to see if there was an obvious conclusion. I estimate that the total power consumed is the work needed to heat up the volume of air inside the oven to the desired temperature, plus the work lost to heat transfer out of the door. It's also possible that the heat is lost through the other sides, but I didn't take that into account. From the ideal gas law, the work to heat up the air inside the oven is:

\\[ W = D_mVR\triangle T \\]

<p>Where \\(D_m\\) is the molar density of air, \\(V\\) is the volume, \\(R\\) is the ideal gas constant, and \\(\triangle T\\) is the temperature change.</p>

The heat lost through the oven door is:

\\[ Q = kA\triangle Tt \\]

<p>Where \\(k\\) is the heat transfer coefficient, \\(A\\) is the area of the door, and \\(t\\) is the time that the oven is on.</p>

Since both ovens have the same depth, the ratio of the ovens' volume 2.8, is the same for the door area. Some mechanical engineers estimate that the [\\(k\\) of double-paned oven doors is ~3](http://www.esss.com.br/events/ansys2014/colombia/pdf/02_1540.pdf), whereas the toaster oven's single pane of glass is 5.8. The ratio of these coefficients almost exactly cancels out the difference in volume. Because the heat is constantly being leaked out of the ovens, the work due to lost heat is nearly an order of magnitude larger than work required to heat up the oven, so this contribution can be mostly ignored. So to really answer this question, we're going to need to get *experimental*. 

I bought an [Aeotek Smart Energy Meter](https://www.amazon.com/Aeon-Labs-AEDSB09104ZWUS-Aeotec-Monitor/dp/B00DIBSKFU/) (currently on Amazon for 32 USD) and an [Aeotek Z-stick](https://www.amazon.com/Aeotec-Z-Stick-Z-Wave-create-gateway/dp/B00X0AWA6E/) (currently on Amazon for 45 USD)<sup>[1](#myfootnote1)</sup>. The Z-Stick is compatible with [open-zwave](http://www.openzwave.com/) which has a [python interface](https://github.com/OpenZWave/python-openzwave).

My code to grab the power data on linux is:

```python
import time
from openzwave.option import ZWaveOption
from libopenzwave import PyManager
import csv
from matplotlib import pyplot

device="/dev/ttyUSB0"
options = ZWaveOption(device, config_path="/etc/openzwave/", user_path=".", cmd_line="")
options.set_console_output(False)
options.lock()


class PowerMeter(PyManager):
    def __init__(self):
        super(PowerMeter, self).__init__()
        self.create()
        self.addWatcher(self.callback)
        time.sleep(1.0)
        self.addDriver(device)
        self.meter_values = []
        self.start_time = None
        self.units = None
        self.value_id = None

    def get_meter_values(self, num_seconds):
        self.start_time = time.time()
        while time.time() - self.start_time < num_seconds:
            time.sleep(0.10)
            if self.value_id:
                assert self.refreshValue(self.value_id)

    def callback(self, zwargs):
        # get measurement value from the first message tagged with the sensor we want
        if "valueId" in zwargs:
            if zwargs["valueId"]["commandClass"] == "COMMAND_CLASS_METER":
                if zwargs["valueId"]["label"] == "Power" and \
                                zwargs["valueId"]["instance"] == 1 \
                        and self.start_time is not None:
                    self.value_id = zwargs["valueId"]["id"]
                    self.units = zwargs["valueId"]["units"]
                    self.meter_values.append((time.time() - self.start_time,
                                              zwargs["valueId"]["value"]))
                    print("Power", zwargs["valueId"]["value"])


manager = PowerMeter()
# collect data for an hour
manager.get_meter_values(60*60)
# add to a csv
with open('meter_values_%s.csv' % manager.start_time, 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['time (s)', 'meter (%s)' % manager.units])
    for row in manager.meter_values:
        spamwriter.writerow(row)

fig, ax = pyplot.subplots()
ax.plot([point[0]/60.0 for point in manager.meter_values],
            [point[1] for point in manager.meter_values])
ax.set_xlabel("Time (minutes)")
ax.set_ylabel("Meter Value (%s)" % manager.units)
fig.savefig("power_meter_%s.png" % manager.start_time)
```

I believe that *instance 1* is the power on the first probe, which is attached to the *hot* wire of my house's main power. Since probe 2 is attached to the *neutral* wire, I believe it's possible to cancel out most of the noise by subtracting the power on instance 2 from the power on instance 1. I have no idea how these map to European/Austrian three phase systems. 

With the script running, I collected three sets of data: one while the toaster cooked a sheet of cookies, one while the oven cooked a sheet of cookies, and one with neither oven running, just the house lights, routers, and refridgerator. The data, from the start of pre-heating to when the cookies came out, looks like this:

![energy usage for various apartments](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/oven_comparison.png)

The toaster took longer to pre-heat, so it had a longer data collection time. It looks like both ovens and the refridgerator (in the base usage) are driven by square forcing functions that turn off when a desired temperature is reached. The oven's forcing function is a bit more sophisticated than the toaster, it looks like it can heat at two different wattage levels. I think the long period of the oven been off while cooking is proof that the oven does have a lower heat transfer coefficient than the toaster oven.

I can integrate the data I collected using scipy's integrate and numpy's interpolate functions:

```python
from scipy import integrate
from numpy import interp

result = integrate.quad(lambda x: interp(x, data_array[0], data_array[1]),
                        min(data_array[0]), max(data_array[0]))[0] 
```

I also subtract off the base usage in each case. After integrating, I estimate that the toaster uses 0.45 kWh to bake a single sheet of cookies, and the oven uses 0.70 kWh. 

The toaster is more efficient at baking a single sheet of cookies, so I'd conclude that the heat transfer coefficient of the toaster is not as bad as expected. However, the oven can handle two sheets at once, and is faster. If you want to shave 8 minutes off of your cook time, it's only an extra 0.15 kWh, which in Florida costs two cents. However, the oven has an advantage over the toaster in that it can cook more than a single sheet at a time, and then the energy cost per cookie favors the oven.
 


<script type="text/javascript" async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>


<a name="myfootnote1">1</a>: It is my personal opinion that Z-Wave compatible devices are 2-3 times more expensive than they should be, given the underlying hardware. I think this is because Z-Wave is not open source, so development takes longer and costs more. I would not invest in a Z-Wave system now. It would be nice to be able to turn off my overhead light from a smartphone app so that I don't have to get out of bed, but just putting a long piece of twine on the pull chain seems to be an adequate solution.

