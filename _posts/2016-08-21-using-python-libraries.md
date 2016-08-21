---
layout: post
title: "Using Python Libraries"
description: "Fantastic modules and where to find them"
category: programming
tags: [python, instrumentkit, windows, library]
---
{% include JB/setup %}


The plethora of libraries is a key feature of using python in the sciences. In this post, I advize on finding and installing libraries, as well as the libraries I use on a regular basis.

Finding New Libraries
=====================

When looking for code, I first turn to the [Python Package Index (PyPI)](https://pypi.python.org/pypi) for packages. If I don't find what I want there, I search the publicly available repositories tagged with 'Python' on [GitHub](https://github.com/search?l=Python&type=Repositories&utf8=%E2%9C%93) to see if someone has also worked on the same problem but has not released python modules on a package manager.

[conda](https://conda.anaconda.org/conda-forge) is alternative package management system aimed at data scientists. I have stopped using it as it had too few packages. 


Installing libraries
====================

There are two ways to install python libraries: either building from source or downloading a .whl file (called wheels), which often include a compiled binary. 'Building' in this context is a bit of a misnomer: python is an interpreted library thus the installation procedure is merely copying some python source code to your python dist-packages or lib folders. However, certain packages, especially those that do intensive numerical calculations, have sections written in C or FORTRAN that need to be compiled. Some python packages release wheels on PyPI, some release wheels outside of PyPI, some python packages on PyPI link to code on github or some other online repository and will automatically download this source and compile and copy files it when it is installed from the package manager, and some packages can only be installed by downloading the source code and compiling. 

Installing from PyPI
--------------------

Read the PyPI package description website to make sure that your operating system and python version are supported by this package. If it is, then open a terminal on Linux, or a command prompt on Windows, and type:

```
pip install module_name
```

If Windows complains that it can't find pip, one of two things may have happened: either pip was not installed when python was installed, in which case it can be installed by running the installation MSI file with scripts selected for installation, or the *C:/Python34/Scripts* path has not been added to the path environment variable.

pip can also install several libraries at once, by specifying each library on a new line in a file (typically called *requirements.txt*). This file can then be called using:

```
pip install -r requirements.txt
```

Many python projects will have a *requirements.txt* file in the main directory.

You can download and install .whl packages with:

```
pip install /path/to/your/wheel.whl
```
You can upgrade an existing package using:

```
pip install --upgrade module_name
```

You can check which version of a library you have installed using:

```
pip show module_name
```

You can uninstall libraries using the command:

```
pip uninstall module_name
```

Installing from github repositories
-----------------------------------

If a module is unavailable as a *.whl or as a package on PyPI, do not despair! It is often possible to install from source.

Assuming the code you want to install has a setup.py file, you can do one of two things: install the repository using pip, or running the setup script.

To install using pip, run (using my pyOmniDriver library as an example):

```
pip install -e git+git://github.com/CatherineH/pyOmniDriver.git#egg=Package
```

This method is not preferable, as pip will copy the code and generated egg-info to a directory called *src/package*, not to the python lib or dist-packages folders, and if this directory is deleted, you will need to re-install the module. The alternate method is to clone the source code, then run the setup file:

```
git clone git@github.com:CatherineH/pyOmniDriver.git
cd pyOmniDriver
python setup.py install
```
When installed this way, source code and builds are copied to the python lib or dist-packages folders and deleting the folder with the cloned repository will not remove the module from the operating system.

Problems on Windows
-------------------

Installing and using python libraries that depend on the Basic Linear Algebra Subprograms (BLAS) specification are a little tricky on Windows, as the Microsoft visual studio compilers have a hard time compiling them without some changes to configuration. There is work towards using open-source compilers and open-source implementations of BLAS, however, not all libraries have implemented this yet (for example, NumPy and SciPy). On Windows, pip installing NumPy will download a .whl compiled with open-blas; SciPy does not yet have a corresponding library. Attempting to install SciPy will result in the error:

```
      File "scipy\linalg\setup.py", line 20, in configuration
        raise NotFoundError('no lapack/blas resources found')
    numpy.distutils.system_info.NotFoundError: no lapack/blas resources found
```

Christoph Golke maintains a [collection of compiled .whl files for windows python libraries](http://www.lfd.uci.edu/~gohlke/pythonlibs/), all built on the Intel Math Kernel Library (MKL) and the Microsoft Visual C++ compiler. I would strongly recommend downloading and installing these packages instead of messing around with the Visual Studio compilers on your own. However, if you install the MKL version of libraries that depend on NumPy while your NumPy package has been installed from PyPI and uses open-blas, you will get the same error as above.

If this happens, uninstall NumPy, then install NumPy from the whl's:

```
pip uninstall numpy
pip install numpy-1.11.1+mkl-cp27-cp27m-win_amd64.whl
```

Make sure the .whl's you download match the python version number and system architecture of your system. You can check these versions by looking at the lines that are printed when python starts up.
If you attempt to install an incompatible whl, you will get the error message:

```
numpy-1.11.1+mkl-cp27-cp27m-win32.whl is not a supported wheel on this platform.
```

If you still get this error message when your python version and system architecture are the same, upgrade pip:

```
pip install --upgrade pip
```


Libraries for Experimental Quantum Optics
=========================================

Here's a short introduction to many useful libraries for doing quantum optics research.

Simulating Data
---------------

[NumPy](http://www.numpy.org/) mimics the array manipulations data syntax introduced in MATLAB. Although its primary functionality is in speeding up numerical operations, I hardly ever call these directly, and instead use NumPy for its array initialization functions. Most other scientifically useful libraries, such as QuTIP, SciPy and pandas are built on top of NumPy objects and operations.

[QuTIP](http://qutip.org/) is the quantum toolbox in python. Though a lot of the functionality is aimed simulating and analyzing more complex quantum systems with long-term time evolution and coupled system, it is still useful for creating entangled photon states using nonlinear optics, applying wave-plates and calculating the probability amplitudes after squashing the states down to classical measurements. 

[PyZZDE](https://github.com/indranilsinharoy/PyZDDE) a python interface to Zemax. Useful for automating optical analysis, for example, optimizing coupling by iteratively moving elements around in the optical system.  

[DEAP](http://deap.gel.ulaval.ca/doc/default/) DEAP stands for Distributed Evolutionary Algorithms in Python and is a versatile library for creating and running genetic programs in python. 

Gathering Data
--------------

[pyserial](https://pythonhosted.org/pyserial/) allows for writing and reading to serial ports from Windows and Linux. It also provides some helper functionality for inspecting available serial ports. 

[InstrumentKit](https://github.com/Galvant/InstrumentKit) is a library that abstracts away the communication protocols to scientific instruments, as well as handling the common and known bugs in these devices.

[PyOmniDriver](https://github.com/CatherineH/pyOmniDriver) is my library for communicating with Ocean Optics spectrometers.

[PyHighFinesse](https://github.com/CatherineH/pyHighFinesse) is my library for communicating with Angstrom/High Finesse spectrometers.

[RPi.GPIO](https://sourceforge.net/projects/raspberry-gpio-python/) is a library for communicating with the raspberry pi's GPIO port, which is allows the raspberry pi to be used as a cheap and simple data acquisition device. 

Analyzing Data
--------------

[pandas](http://pandas.pydata.org/) provides a data storage object called a DataFrame, which is accessed like R's DataFrame. When stored in a DataFrame, data can be easily sliced on a query - i.e., pick out all spectrometer intensities where the oven temperature was 34 degrees C between the ranges of 800 to 815 nm, then manipulated as a NumPy matrix or array, printed in a human-readable format, or written to a comma separated file.

[scipy.signal](http://docs.scipy.org/doc/scipy/reference/signal.html) can be useful in analyzing spectrums and oscilloscope traces, however many of these libraries are overkill. The same task can often be accomplished in a more transparent and effective fashion using curve-fitting.

[scipy.stats](http://docs.scipy.org/doc/scipy/reference/stats.html) contains methods for fitting data to several probability distributions that can arise from experimental data, for example, gaussians, poissonians, chi-squared and log-normal, as well as multi-variate analysis.

[scipy.optimize](http://docs.scipy.org/doc/scipy/reference/optimize.html) contains methods for performing simple numerical optimizations, such as curve-fitting and root-finding. Though not as sophisticated as some other machine-learning algorithms, when applied correctly it is powerful enough. 

Visualizing Data
----------------

[matplotlib](http://matplotlib.org/) is a versatile 2-d plotter. If data can be drawn as a collection of 2-d shapes, it can be created programmatically using matplotlib. Matplotlib has methods for simple scatter-plots and bar charts, but its versatility comes from its artist layer, which allows any two-dimensional shape or annotation to be added to the plot. Another key feature is that care has been put into making the default style and color schemes attractive in the latest version.

[svgwrite](https://svgwrite.readthedocs.io/en/latest/) allows scalable vector graphics to be created from within python. Useful for creating iterative experimental schematics that can be scaled for any resolution (for example, when printing in an article pdf) or viewed in a web browser.

[PySide](https://wiki.qt.io/PySide) is a python implementation of Qt, a robust cross-platform graphical user interface library. PySide is particularly useful as it has a license that allows it to be used for commercial applications. One drawback is that it is not yet compatible with python 3.5. 

[PyQtGraph](http://pyqtgraph.org/) allows plots to be embedded in Qt applications. Although it is possible to render matplotlib graphs in Qt GUI's, they do not respond well to multi-threaded programs. PyQtGraph, on the other hand, is based on Qt and thus can be used in a Qt thread. Responsive experimental GUI's require threading, thus responsive experimental graphs require PyQtGraph. It is not as versatile or as attractive as matplotlib, but adequate for real-time GUI's. 


If there is a library you find useful not included in the above, let me know!


