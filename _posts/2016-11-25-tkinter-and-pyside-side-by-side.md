---
layout: post
title: "Tkinter and PySide side-by-side"
description: "A python GUI Rosetta Stone"
category: programming
tags: [python, tkinter, pyside]
---
{% include JB/setup %}

Out of the [long list of cross-platform python GUI options](https://wiki.python.org/moin/GuiProgramming), the two that I'm most familiar with are [Tkinter](https://wiki.python.org/moin/TkInter) and [PySide](http://www.pyside.org/). The purpose of this post is to demonstrate how to create the same application with a separate data acquisition thread using both of these libraries and discuss the differences between them. The code for these sample applications is available in my github repository [python-gui-demos](https://github.com/CatherineH/python-gui-demos).

# The Program

The demo program measures the amount of waking day elapsed, calculated by comparing the current time against the a set wake time and bed time in the config file. The waking day elapsed is displayed using a progress bar and a label, a pause button prevents these elements from updating, and a quit button closes the application. 

This is accomplished by defining a *GuiPart* object and a *ThreadedClient* object which can communicate between each other. For the sake of comparison, I've used the same names for both implementations:

<svg width="500" height="165">
	<rect x="10" y="10" width="150" height="151" rx="15" ry="15" fill="#c0d6f9" stroke-width="5" stroke="black"/>
        <rect x="300" y="10" width="150" height="79" rx="15" ry="15" fill="#c0d6f9" stroke-width="5" stroke="black"/>
	<rect x="13" y="35" width="145" height="72" fill="#f9e4c0" stroke-width="0" />
	<rect x="303" y="35" width="145" height="24" fill="#f9e4c0" stroke-width="0" />
	<text x="85" y="30" font-family="Verdana" font-size="15" text-anchor="middle">GuiPart</text>
	<text x="375" y="30" font-family="Verdana" font-size="15" text-anchor="middle">ThreadedClient</text>
	<line x1="10" y1="35" x2="160" y2="35" stroke-width="2" stroke="black" stroke-width="5"/>
	<line x1="300" y1="35" x2="450" y2="35" stroke-width="2" stroke="black" stroke-width="5"/>
	<text x="85" y="52" font-family="Verdana" font-size="12" text-anchor="middle">thread</text>
	<text x="85" y="64" font-family="Verdana" font-size="12" text-anchor="middle">day_bar</text>
	<text x="85" y="76" font-family="Verdana" font-size="12" text-anchor="middle">day_label</text>	
	<text x="85" y="88" font-family="Verdana" font-size="12" text-anchor="middle">pause_button</text>
	<text x="85" y="100" font-family="Verdana" font-size="12" text-anchor="middle">quit_button</text>
	<line x1="10" y1="107" x2="160" y2="107" stroke-width="2" stroke="black"/>
	<text x="85" y="122" font-family="Verdana" font-size="12" text-anchor="middle">pause()</text>
	<text x="85" y="134" font-family="Verdana" font-size="12" text-anchor="middle">quit_click()</text>	
	<text x="85" y="146" font-family="Verdana" font-size="12" text-anchor="middle">update(current_datetime)</text>
	<text x="375" y="52" font-family="Verdana" font-size="12" text-anchor="middle">parent</text>
	
	<line x1="300" y1="59" x2="450" y2="59" stroke-width="2" stroke="black"/>
	<text x="375" y="74" font-family="Verdana" font-size="12" text-anchor="middle">run()</text>
	<line x1="160" y1="48" x2="300" y2="19" stroke-width="0.5" stroke="black" stroke-width="5" stroke-dasharray="5, 5"/>
	<line x1="160" y1="19" x2="300" y2="48" stroke-width="0.5" stroke="black" stroke-width="5" stroke-dasharray="5, 5"/>
	
	
	
</svg>

The GUI uses a grid layout and looks like this:

<svg width="500" height="500">
	<rect x="10" y="10" width="480" height="480" fill="#538cd5" stroke="black" />
	<line x1="250" y1="10" x2="250" y2="490" stroke="black" />
	<line x1="10" y1="200" x2="250" y2="200" stroke="black" />
	<line x1="10" y1="400" x2="490" y2="400" stroke="black" />
	<rect x="20" y="410" width="220" height="70" fill="#538cd5" stroke="black" />
	<rect x="260" y="410" width="220" height="70" fill="#538cd5" stroke="black" />
	<rect x="20" y="220" width="220" height="170" fill="#ffffff" stroke="black" />
	<rect x="320" y="20" width="100" height="370" fill="#ffffff" stroke="black" />	
	<rect x="320" y="320" width="100" height="70" fill="#00b050" stroke="black" />
	<text x="0" y="0" transform="rotate(90 60,300)" font-family="Verdana" font-size="16" text-anchor="middle">day_bar</text>
	<text x="130" y="260" font-family="Verdana" font-size="16" style="fill: #00b050;" text-anchor="middle">day_label</text>
	<text x="130" y="110" font-family="Verdana" font-size="16" style="fill: #ffffff;" text-anchor="middle">program_label</text>
	<text x="130" y="450" font-family="Verdana" font-size="16" style="fill: #ffffff;" text-anchor="middle">pause_button</text>
	<text x="370" y="450" font-family="Verdana" font-size="16" style="fill: #ffffff;" text-anchor="middle">quit_button</text>
</svg>

The grid layout has 3 rows and 2 columns, and the progress bar spans two rows.


# Implementation

## Setting Up Objects

Through Qt, PySide has a thread object - the QtCore *QThread*. Tkinter does not provide a tk-flavoured thread object, so we'll use the standard library thread object. In python 2, the tkinter Tk object is implemented as a *classobj* instead of a *type*, so in order for our GUI to inherit it be have to make it a metaclass of *Tk* and *object*.

<table><tr><td><b>PySide</b></td><td><b>Tkinter</b></td></tr>
<tr><td><div class="highlighter-rouge"><pre class="highlight"><code><span class="k">class</span> <span class="nc">GuiPart</span><span class="p">(</span><span class="n">QtGui</span><span class="o">.</span><span class="n">QWidget</span><span class="p">):</span>
    <span class="o">...</span>

<span class="k">class</span> <span class="nc">ThreadedClient</span><span class="p">(</span><span class="n">QtCore</span><span class="o">.</span><span class="n">QThread</span><span class="p">):</span>
    <span class="o">...</span>
</code></pre>
</div></td><td><div class="highlighter-rouge"><pre class="highlight"><code><span class="k">class</span> <span class="nc">GuiPart</span><span class="p">(</span><span class="n">tk</span><span class="o">.</span><span class="n">Tk</span><span class="p">,</span> <span class="nb">object</span><span class="p">):</span>
    <span class="o">...</span>

<span class="k">class</span> <span class="nc">ThreadedClient</span><span class="p">(</span><span class="n">threading</span><span class="o">.</span><span class="n">Thread</span><span class="p">):</span>
    <span class="o">...</span>
</code></pre>
</div></td></tr>
</table>

## Widget Layout

In PySide, the layout is a separate object from the main window's *QWidget* called *QGridLayout*. GUI widgets are then added to this main layout with the row/column/rowspan and columnspan information. In Tkinter, the main window is passed as the first variable to each GUI widget, and then can be packed into a grid using the *.grid()* method. You can also add elements without a grid layout using *.pack()*, but combining calls to *.pack()* and *.grid()* will result in errors.

<table><tr><td><b>PySide</b></td><td><b>Tkinter</b></td></tr>
<tr><td><div class="highlighter-rouge"><pre class="highlight"><code><span class="bp">self</span><span class="o">.</span><span class="n">main_layout</span> <span class="o">=</span> <span class="n">QtGui</span><span class="o">.</span><span class="n">QGridLayout</span><span class="p">()</span>
<span class="bp">self</span><span class="o">.</span><span class="n">day_bar</span> <span class="o">=</span> <span class="n">QtGui</span><span class="o">.</span><span class="n">QProgressBar</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">day_label</span> <span class="o">=</span> <span class="n">QtGui</span><span class="o">.</span><span class="n">QLabel</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">pause_button</span> <span class="o">=</span> <span class="n">QtGui</span><span class="o">.</span><span class="n">QPushButton</span><span class="p">(</span><span class="s">"Pause"</span><span class="p">,</span> <span class="bp">self</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">quit_button</span> <span class="o">=</span> <span class="n">QtGui</span><span class="o">.</span><span class="n">QPushButton</span><span class="p">(</span><span class="s">"Quit"</span><span class="p">,</span> <span class="bp">self</span><span class="p">)</span>
<span class="n">program_label</span> <span class="o">=</span> <span class="n">QtGui</span><span class="o">.</span><span class="n">QLabel</span><span class="p">(</span><span class="n">cfg</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">"variables"</span><span class="p">,</span> <span class="s">"main_label"</span><span class="p">),</span> <span class="bp">self</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">main_layout</span><span class="o">.</span><span class="n">addWidget</span><span class="p">(</span><span class="n">program_label</span><span class="p">,</span> <span class="mi">0</span><span class="p">,</span> <span class="mi">0</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">1</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">main_layout</span><span class="o">.</span><span class="n">addWidget</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">day_label</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">0</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">1</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">main_layout</span><span class="o">.</span><span class="n">addWidget</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">day_bar</span><span class="p">,</span> <span class="mi">0</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">,</span> <span class="mi">1</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">main_layout</span><span class="o">.</span><span class="n">addWidget</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">pause_button</span><span class="p">,</span> <span class="mi">2</span><span class="p">,</span> <span class="mi">0</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">1</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">main_layout</span><span class="o">.</span><span class="n">addWidget</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">quit_button</span><span class="p">,</span> <span class="mi">2</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">1</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">setLayout</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">main_layout</span><span class="p">)</span>
</code></pre>
</div>
</td>

<td><div class="highlighter-rouge"><pre class="highlight"><code><span class="bp">self</span><span class="o">.</span><span class="n">day_bar</span> <span class="o">=</span> <span class="n">ttk</span><span class="o">.</span><span class="n">Progressbar</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">day_bar</span><span class="o">.</span><span class="n">grid</span><span class="p">(</span><span class="n">row</span><span class="o">=</span><span class="mi">0</span><span class="p">,</span> <span class="n">column</span><span class="o">=</span><span class="mi">1</span><span class="p">,</span> <span class="n">rowspan</span><span class="o">=</span><span class="mi">2</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">day_label</span> <span class="o">=</span> <span class="n">tk</span><span class="o">.</span><span class="n">Label</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">day_label</span><span class="o">.</span><span class="n">grid</span><span class="p">(</span><span class="n">row</span><span class="o">=</span><span class="mi">1</span><span class="p">,</span> <span class="n">column</span><span class="o">=</span><span class="mi">0</span><span class="p">)</span>
<span class="n">program_label</span> <span class="o">=</span> <span class="n">ttk</span><span class="o">.</span><span class="n">Label</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">text</span><span class="o">=</span><span class="n">cfg</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">"variables"</span><span class="p">,</span> <span class="s">"main_label"</span><span class="p">))</span>
<span class="n">program_label</span><span class="o">.</span><span class="n">grid</span><span class="p">(</span><span class="n">row</span><span class="o">=</span><span class="mi">0</span><span class="p">,</span> <span class="n">column</span><span class="o">=</span><span class="mi">0</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">pause_button</span> <span class="o">=</span> <span class="n">ttk</span><span class="o">.</span><span class="n">Button</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">pause_button</span><span class="o">.</span><span class="n">grid</span><span class="p">(</span><span class="n">row</span><span class="o">=</span><span class="mi">2</span><span class="p">,</span> <span class="n">column</span><span class="o">=</span><span class="mi">0</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">quit_button</span> <span class="o">=</span> <span class="n">ttk</span><span class="o">.</span><span class="n">Button</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">text</span><span class="o">=</span><span class="s">"Quit"</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">quit_button</span><span class="o">.</span><span class="n">grid</span><span class="p">(</span><span class="n">row</span><span class="o">=</span><span class="mi">2</span><span class="p">,</span> <span class="n">column</span><span class="o">=</span><span class="mi">1</span><span class="p">)</span>
</code></pre>
</div></td></tr></table>

## Slots, Signals and Callbacks

In order to have a responsive GUI, signals emitted from user's interaction to the trigger the desired action. PySide Widgets come with several pre-defined signals, or it is possible to define your own. Signals can be connected to the desired method using the *.connect()* method. In Tkinter, buttons have a slot for specifying the action on clicking called *command*. Here's how to define button callbacks:


<table><tr><td><b>PySide</b></td><td><b>Tkinter</b></td></tr>
<tr><td><div class="highlighter-rouge"><pre class="highlight"><code><span class="bp">self</span><span class="o">.</span><span class="n">pause_button</span><span class="o">.</span><span class="n">clicked</span><span class="o">.</span><span class="n">connect</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">pause</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">quit_button</span><span class="o">.</span><span class="n">clicked</span><span class="o">.</span><span class="n">connect</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">quit_click</span><span class="p">)</span>
</code></pre>
</div></td><td><div class="highlighter-rouge"><pre class="highlight"><code><span class="bp">self</span><span class="o">.</span><span class="n">pause_button</span><span class="o">.</span><span class="n">configure</span><span class="p">(</span><span class="n">command</span><span class="o">=</span><span class="bp">self</span><span class="o">.</span><span class="n">pause</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">quit_button</span><span class="o">.</span><span class="n">configure</span><span class="p">(</span><span class="n">command</span><span class="o">=</span><span class="bp">self</span><span class="o">.</span><span class="n">quit_click</span><span class="p">)</span>
</code></pre>
</div></td></tr></table>

Updating the appearance of Widgets does not easily lend itself to side-by-side comparison, because PySide allows signals to be emitted from any defined type in Python, whereas Tkinter allows for only 3 variables - *StringVar*, *IntVar* and *DoubleVar*. In PySide, we can create a custom signal called *current_datetime*, 

<b>PySide</b>

```python
class ThreadedClient(QtCore.QThread):
    current_time = QtCore.Signal(datetime)
    ...
    def run(self):
        while True:
            if not self.parent.paused:
                self.current_time.emit(datetime.now())
            sleep(1)
```

and hook it up to the *.update(current_datetime)* method:

```python
class GuiPart(QtGui.QWidget):
   def __init__(self):
	...
        self.thread.current_time.connect(self.update)
    ...
    @QtCore.Slot(datetime)
    def update(self, current_datetime):
        percent_elapsed_value = percent_elapsed(current_datetime)
        self.day_bar.setValue(percent_elapsed_value)
        self.day_label.setText(str(percent_elapsed_value))
```

Note that the *update(current_datetime)* needs a decorator to describe that the incoming signals are of type *datetime*. 

In Tkinter, Widget attributes must be defined by variables in order to be updated. For example:
<b>Tkinter</b>

```python
class GuiPart(tk.Tk, object):
    def __init__(self):
        ...
        self.day_bar_value = tk.IntVar()
        self.day_label_value = tk.StringVar()
        self.day_bar.configure(variable=self.day_bar_value)
        self.day_label.configure(textvariable=self.day_label_value)
    ...
    def update(self, current_datetime):
        percent_elapsed_value = percent_elapsed(current_datetime)
        self.day_bar_value.set(percent_elapsed_value)
        self.day_label_value.set(str(percent_elapsed_value))
```

We could use *bind* to create a custom event to trigger the GUI update, however, it would not communicate the datetime information back to the GUI. Since we kept a reference to the GUI in the ThreadedClient object, we can call the method directly.

```python
class ThreadedClient(threading.Thread):
    ...
    def run(self):
        while True:
            ...
	    if not self.parent.paused:
                self.parent.update(datetime.now())
            sleep(1)
```

## Styling

PySide allows elements to be styled using CSS, and can be applied to the object using *setStyleSheet*. Like webpage style sheets, styles inherit the style of the encapsulating element unless otherwise specified, so applying the style sheet to the main window will result in the same style sheet being applied to both buttons and the program_label. Tkinter elements can either be styled using the *.configure()* method, if they were *tk* widgets, or using *ttk.Style()* objects. In this example I will style one element using the *tk* style and the others using *ttk*.

<table><tr><td><b>PySide</b></td><td><b>Tkinter</b></td></tr>
<td>
<div class="highlighter-rouge"><pre class="highlight"><code><span class="bp">self</span><span class="o">.</span><span class="n">setStyleSheet</span><span class="p">(</span><span class="s">"QWidget { "</span>
                   <span class="s">"background-color: "</span>
                   <span class="s">"</span><span class="se">\"</span><span class="s">"</span><span class="o">+</span><span class="n">cfg</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">'colors'</span><span class="p">,</span> <span class="s">'background'</span><span class="p">)</span><span class="o">+</span><span class="s">"</span><span class="se">\"</span><span class="s">;"</span>
                   <span class="s">"font-family:"</span><span class="o">+</span><span class="n">cfg</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">'font'</span><span class="p">,</span> <span class="s">'face'</span><span class="p">)</span><span class="o">+</span><span class="s">"; "</span>
                   <span class="s">"font-size: "</span><span class="o">+</span><span class="n">cfg</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">'font'</span><span class="p">,</span> <span class="s">'size'</span><span class="p">)</span><span class="o">+</span><span class="s">"pt;"</span>
                   <span class="s">"color: </span><span class="se">\"</span><span class="s">"</span><span class="o">+</span><span class="n">cfg</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">'colors'</span><span class="p">,</span> <span class="s">'text'</span><span class="p">)</span><span class="o">+</span><span class="s">"</span><span class="se">\"</span><span class="s">;"</span>
                   <span class="s">"}"</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">day_label</span><span class="o">.</span><span class="n">setStyleSheet</span><span class="p">(</span><span class="s">"QLabel { "</span>
                   <span class="s">"background-color: "</span>
                   <span class="s">"</span><span class="se">\"</span><span class="s">"</span><span class="o">+</span><span class="n">cfg</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">'colors'</span><span class="p">,</span> <span class="s">'text'</span><span class="p">)</span><span class="o">+</span><span class="s">"</span><span class="se">\"</span><span class="s">;"</span>
                   <span class="s">"color: </span><span class="se">\"</span><span class="s">"</span><span class="o">+</span><span class="n">cfg</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">'colors'</span><span class="p">,</span> <span class="s">'sub_text'</span><span class="p">)</span><span class="o">+</span><span class="s">"</span><span class="se">\"</span><span class="s">;"</span>
                   <span class="s">"border: "</span><span class="o">+</span><span class="n">cfg</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">'layout'</span><span class="p">,</span> <span class="s">'border_width'</span><span class="p">)</span><span class="o">+</span><span class="s">"px"</span>
                   <span class="s">" solid </span><span class="se">\"</span><span class="s">"</span><span class="o">+</span><span class="n">cfg</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">'colors'</span><span class="p">,</span> <span class="s">'border'</span><span class="p">)</span><span class="o">+</span><span class="s">"</span><span class="se">\"</span><span class="s">;"</span>
                   <span class="s">"}"</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">day_bar</span><span class="o">.</span><span class="n">setStyleSheet</span><span class="p">(</span><span class="s">"QProgressBar{ "</span>
                   <span class="s">"background-color: "</span>
	           <span class="s">"</span><span class="se">\"</span><span class="s">"</span><span class="o">+</span><span class="n">cfg</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">'colors'</span><span class="p">,</span> <span class="s">'text'</span><span class="p">)</span><span class="o">+</span><span class="s">"</span><span class="se">\"</span><span class="s">;"</span>
                   <span class="s">"border: "</span><span class="o">+</span><span class="n">cfg</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">'layout'</span><span class="p">,</span> <span class="s">'border_width'</span><span class="p">)</span><span class="o">+</span><span class="s">"px"</span>
                   <span class="s">" solid </span><span class="se">\"</span><span class="s">"</span><span class="o">+</span><span class="n">cfg</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">'colors'</span><span class="p">,</span> <span class="s">'border'</span><span class="p">)</span><span class="o">+</span><span class="s">"</span><span class="se">\"</span><span class="s">;"</span>
                   <span class="s">" } "</span>
                   <span class="s">"QProgressBar::chunk {    "</span>
                   <span class="s">" background-color: "</span>
                   <span class="s">"</span><span class="se">\"</span><span class="s">"</span><span class="o">+</span><span class="n">cfg</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">'colors'</span><span class="p">,</span> <span class="s">'sub_text'</span><span class="p">)</span><span class="o">+</span><span class="s">"</span><span class="se">\"</span><span class="s">;} "</span><span class="p">)</span>
</code></pre>
</div>
</td>
<td>
<div class="highlighter-rouge"><pre class="highlight"><code><span class="bp">self</span><span class="o">.</span><span class="n">configure</span><span class="p">(</span><span class="n">background</span><span class="o">=</span><span class="n">cfg</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">'colors'</span><span class="p">,</span> <span class="s">'background'</span><span class="p">))</span>
<span class="n">s</span> <span class="o">=</span> <span class="n">ttk</span><span class="o">.</span><span class="n">Style</span><span class="p">()</span>
<span class="n">s</span><span class="o">.</span><span class="n">configure</span><span class="p">(</span><span class="s">'TButton'</span><span class="p">,</span> <span class="n">background</span><span class="o">=</span><span class="n">cfg</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">'colors'</span><span class="p">,</span> <span class="s">'background'</span><span class="p">))</span>
<span class="n">s</span><span class="o">.</span><span class="n">configure</span><span class="p">(</span><span class="s">'TButton'</span><span class="p">,</span> 
            <span class="n">activebackground</span><span class="o">=</span><span class="n">cfg</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">'colors'</span><span class="p">,</span> <span class="s">'background'</span><span class="p">))</span>
<span class="n">s</span><span class="o">.</span><span class="n">configure</span><span class="p">(</span><span class="s">'TButton'</span><span class="p">,</span> <span class="n">foreground</span><span class="o">=</span><span class="n">cfg</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">'colors'</span><span class="p">,</span> <span class="s">'text'</span><span class="p">))</span>
<span class="n">s</span><span class="o">.</span><span class="n">configure</span><span class="p">(</span><span class="s">'TButton'</span><span class="p">,</span> 
            <span class="n">highlightbackground</span><span class="o">=</span><span class="n">cfg</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">'colors'</span><span class="p">,</span> <span class="s">'background'</span><span class="p">))</span>
<span class="n">s</span><span class="o">.</span><span class="n">configure</span><span class="p">(</span><span class="s">'TButton'</span><span class="p">,</span> <span class="n">font</span><span class="o">=</span><span class="p">(</span><span class="n">cfg</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">'font'</span><span class="p">,</span> <span class="s">'face'</span><span class="p">),</span> 
            <span class="nb">int</span><span class="p">(</span><span class="n">cfg</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">'font'</span><span class="p">,</span> <span class="s">'size'</span><span class="p">))))</span>
<span class="n">s</span><span class="o">.</span><span class="n">configure</span><span class="p">(</span><span class="s">'TLabel'</span><span class="p">,</span> <span class="n">background</span><span class="o">=</span><span class="n">cfg</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">'colors'</span><span class="p">,</span> <span class="s">'background'</span><span class="p">))</span>
<span class="n">s</span><span class="o">.</span><span class="n">configure</span><span class="p">(</span><span class="s">'TLabel'</span><span class="p">,</span> <span class="n">foreground</span><span class="o">=</span><span class="n">cfg</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">'colors'</span><span class="p">,</span> <span class="s">'text'</span><span class="p">))</span>
<span class="n">s</span><span class="o">.</span><span class="n">configure</span><span class="p">(</span><span class="s">'TLabel'</span><span class="p">,</span> 
            <span class="n">highlightbackground</span><span class="o">=</span><span class="n">cfg</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">'colors'</span><span class="p">,</span> <span class="s">'background'</span><span class="p">))</span>
<span class="n">s</span><span class="o">.</span><span class="n">configure</span><span class="p">(</span><span class="s">'TLabel'</span><span class="p">,</span> <span class="n">font</span><span class="o">=</span><span class="p">(</span><span class="n">cfg</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">'font'</span><span class="p">,</span> <span class="s">'face'</span><span class="p">),</span> 
            <span class="nb">int</span><span class="p">(</span><span class="n">cfg</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">'font'</span><span class="p">,</span> <span class="s">'size'</span><span class="p">))))</span>
<span class="n">s</span><span class="o">.</span><span class="n">configure</span><span class="p">(</span><span class="s">'Vertical.TProgressbar'</span><span class="p">,</span>  
            <span class="n">background</span><span class="o">=</span><span class="n">cfg</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">'colors'</span><span class="p">,</span> <span class="s">'sub_text'</span><span class="p">))</span>
<span class="n">s</span><span class="o">.</span><span class="n">configure</span><span class="p">(</span><span class="s">'Vertical.TProgressbar'</span><span class="p">,</span>  
            <span class="n">troughcolor</span><span class="o">=</span><span class="n">cfg</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">'colors'</span><span class="p">,</span> <span class="s">'text'</span><span class="p">))</span>
<span class="n">s</span><span class="o">.</span><span class="n">configure</span><span class="p">(</span><span class="s">'Vertical.TProgressbar'</span><span class="p">,</span>  
            <span class="n">highlightbackground</span><span class="o">=</span><span class="n">cfg</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">'colors'</span><span class="p">,</span> <span class="s">'border'</span><span class="p">))</span>
<span class="n">s</span><span class="o">.</span><span class="n">configure</span><span class="p">(</span><span class="s">'Vertical.TProgressbar'</span><span class="p">,</span>  
            <span class="n">highlightthickness</span><span class="o">=</span><span class="nb">int</span><span class="p">(</span><span class="n">cfg</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">'layout'</span><span class="p">,</span> <span class="s">'border_width'</span><span class="p">)))</span>
<span class="bp">self</span><span class="o">.</span><span class="n">day_label</span><span class="o">.</span><span class="n">configure</span><span class="p">(</span><span class="n">background</span><span class="o">=</span><span class="n">cfg</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">'colors'</span><span class="p">,</span> <span class="s">'text'</span><span class="p">))</span>
<span class="bp">self</span><span class="o">.</span><span class="n">day_label</span><span class="o">.</span><span class="n">configure</span><span class="p">(</span><span class="n">foreground</span><span class="o">=</span><span class="n">cfg</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">'colors'</span><span class="p">,</span> <span class="s">'sub_text'</span><span class="p">))</span>
<span class="bp">self</span><span class="o">.</span><span class="n">day_label</span><span class="o">.</span><span class="n">configure</span><span class="p">(</span><span class="n">highlightbackground</span><span class="o">=</span>
                          <span class="n">cfg</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">'colors'</span><span class="p">,</span> <span class="s">'border'</span><span class="p">))</span>
<span class="bp">self</span><span class="o">.</span><span class="n">day_label</span><span class="o">.</span><span class="n">configure</span><span class="p">(</span><span class="n">highlightthickness</span><span class="o">=</span><span class="mi">2</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">day_label</span><span class="o">.</span><span class="n">configure</span><span class="p">(</span><span class="n">font</span><span class="o">=</span><span class="p">(</span><span class="n">cfg</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">'font'</span><span class="p">,</span> <span class="s">'face'</span><span class="p">),</span> 
                         <span class="nb">int</span><span class="p">(</span><span class="n">cfg</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s">'font'</span><span class="p">,</span> <span class="s">'size'</span><span class="p">))))</span>
</code></pre>
</div>
</td>
</table>



## Filling the screen

PySide spaces elements to fill the entire screen by default, but the main window must be set to fullscreen. Tkinter occupies only the minimal amount of space required by default. To get Tkinter elements to expand, certain rows and columns must be given weight:


<table><tr><td><b>PySide</b></td><td><b>Tkinter</b></td></tr>
<td><div class="highlighter-rouge"><pre class="highlight"><code><span class="bp">self</span><span class="o">.</span><span class="n">showFullScreen</span><span class="p">()</span>
</code></pre>
</div></td><td><div class="highlighter-rouge"><pre class="highlight"><code><span class="bp">self</span><span class="o">.</span><span class="n">attributes</span><span class="p">(</span><span class="s">"-fullscreen"</span><span class="p">,</span> <span class="bp">True</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">columnconfigure</span><span class="p">(</span><span class="mi">0</span><span class="p">,</span> <span class="n">weight</span><span class="o">=</span><span class="mi">1</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">rowconfigure</span><span class="p">(</span><span class="mi">0</span><span class="p">,</span> <span class="n">weight</span><span class="o">=</span><span class="mi">1</span><span class="p">)</span>
<span class="bp">self</span><span class="o">.</span><span class="n">rowconfigure</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="n">weight</span><span class="o">=</span><span class="mi">1</span><span class="p">)</span>
</code></pre>
</div></td></table>

# Final Result

After all of that styling, here's the final result:

<table><tr><td><b>PySide</b></td><td><b>Tkinter</b></td></tr>
<td><img src="https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/tkinter_pyside/pyside.jpg" alt="pyside final result"></td><td><img src="https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/tkinter_pyside/tkinter.jpg" alt="tkinter final result"></td></table>

Things that make this not quite a fair comparison are:

- I didn't bother with stickies in my grid layout in Tkinter, hence the difference in sizes in elements.
- I was not able to figure out how to change the border of TProgressBar in Tkinter, though it may still be an option I haven't found
- text is not aligned to center in the PySide version

# Which library should you pick?

Tkinter has the same GNU General Public License as Python. PySide is licensed under the GNU Lesser General Public License. Both of these licenses allow for their use in proprietary software, however the LGPL is a bit friendlier to commercial development than GPL as the requirements to exactly copy the license are less strict. If you're going to use *PySide*, the other parts of your code will almost certainly fall under Python's GPL license, so this point seems moot.

Though both libraries can be employed in object-oriented and procedural fashions, the Tkinter examples tend to use procedural programming and the PySide examples tend to use object-oriented programming, meaning that object-oriented programming neophytes may find PySide intimidating. However, PySide has a greater selection of functionality than Tkinter, in terms of variety of widgets, signals, slots and display options. PySide uses the styles defined in your installed version of Qt, which means that by default PySide programs tend to look less dated than Tkinter programs. PySide is a bit like using LaTeX over Word - though more complicated, the default layout rules are better than Tkinter, allowing design newbs like me to trade technical skill for aesthetics.

In conclusion, my advice would be that Tkinter is good for prototyping simple applications, but if you plan on adding functionality in the future or presenting a polished product, start with PySide.

