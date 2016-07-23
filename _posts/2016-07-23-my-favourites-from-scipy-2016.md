---
layout: post
title: "My Favourites from SciPy 2016"
description: "Wheels, Linting Text and Imputation"
category: programming
tags: [python, conference, scipy]
---
{% include JB/setup %}

The SciPy 2016 conference was last week in Austin, Texas. Despite the 
suffocating heat, I got to visit the Lyndon B Johnson Presidential 
Library, see Ghostbusters in the Alamo Drafthouse, and sleep in an 
airstream trailer in someone's back yard. More importantly, I had 
the opportunity to 
[talk about pyglet_helper](https://www.youtube.com/watch?v=lrk6erM3mkI), 
and learn a lot of useful things about python. Here are a few personal highlights.


Making Python Packages for Windows is Hard
==========================================

Frequent visitors to PyPI may have noticed that many common packages have 
recently switched to using wheels. No longer will we twiddle our thumbs 
restlessly as we watch setup.py install churn through line after line of
 gcc warnings! That is due to the excellent efforts of Nathaniel Smith, 
 who spoke about his work:
 
[![Reinventing the .whl](http://img.youtube.com/vi/oE5iePv8nD8/0.jpg)](https://www.youtube.com/watch?v=oE5iePv8nD8)


Wheels can be built for several different versions of python using a 
provided docker image. The Numpy and Scipy builds are built with OpenBLAS,
 which is an exciting development. Smith seems confident that it will be 
 possible to bundle OpenBLAS with Numpy wheels on Windows soon as well, 
 which will be a big time-saver for me. 
 
At 9:12, he describes exactly what is needed to easily compile wheels 
for Windows - the lack of a good compiler. This was brought up by an 
audience member at the python core developers panel at Euro Python a few
 days ago and the panellists seemed surprised. I think the problem is 
 that the people with the domain knowledge of compilers are exclusively 
 linux users and windows users would prefer to use Anaconda. In between 
 are a few like me, who both need to use Windows for device 
 drivers but also want to use obscure packages in PyPI, without fussing 
 with the visual studio compiler.

Linting Text
============

As much joy as writing this blog has been, it has forced me to confront 
the fact that I am not a good writer and I should be better at editing 
my text. I acquired an appreciation for style guides from the 
one journalism class I took in undergrad, but 10 years later I've 
forgotten most of the rules. Thus, I am keenly interested in Michael 
Pacer and Jordan Suchow's project, proselint:


[![A linter for prose](http://img.youtube.com/vi/S55EFUOu4O0/0.jpg)](https://www.youtube.com/watch?v=S55EFUOu4O0)

I've tried it out for myself on my blog posts, and at the moment it has 
difficulty with markdown, especially in accidentally prose-linting code 
blocks. Regular expressions have only a limited ability to fix bad 
writing, but I will take all the help I can get. I'm interested in 
building a PyCharm extension for proselint and in incorporating proselint
 into my githubio build process. I'm not sure how successful I will be 
 in my current set-up, as my build uses ruby.

EPIC Async
==========

Though I have been working in experimental physics for the past six 
years, I had never heard of the [Experimental Physics and Industrial 
Control System (EPICS)](http://www.aps.anl.gov/epics/) until Daniel 
Allen's talk. I work on experiments with only up to one control computer
 at a time, whereas EPICS is used big, hundred-party experiments such as
  Synchrotrons or LIGO. From a conceptual level, it reminds me of the 
  Robotics Operating System, with its publishers and subscribers. In his
   talk, Allan describes an experimentalists' dream: capture your data 
   along with the operations in a retrievable format, and have a system 
   that can roll back to a recoverable state if something goes wrong.
    

[![Experiments as Iterators](http://img.youtube.com/vi/0WoSJS3_mC0/0.jpg)](https://www.youtube.com/watch?v=0WoSJS3_mC0)


These are design goals for my projects as well, even if they 
 only have 3 users. I have limited time with my equipment as well, and 
 needing to repeat an experiment because some metadata was missing is a 
 waste. I don't quite understand the usage of asyncio in 
 this context, but I'm eager to learn how it could benefit my 
 experimental automation.

Imputation is Important for the Real World
==========================================

John's recently-defended PhD thesis is about applying machine learning 
techniques to filling missing data (imputation) on incomplete ranked 
ballots in order to maximize the fairness of elections. Imputation is an
 important consideration when applying algorithms to data in the real 
 world, as Deborah Hanus demonstrated in her talk, featuring her work 
 with optimizing the treatments for HIV patients: 

[![Dealing with Missing Data](http://img.youtube.com/vi/cHzahWjaA7o/0.jpg)](https://www.youtube.com/watch?v=cHzahWjaA7o)

Due to issues surrounding shift work and childcare, transportation 
access, or human error, HIV patients sometimes miss their regularly 
scheduled blood tests. Imputation allows the machine learning 
algorithm to predict optimal dosages even in the presence of missing 
data. Aside from being interesting research, the talk also provides a 
good layman's explanation of imputing random walks over time.
   


