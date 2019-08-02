---
layout: post
title: "Limiting Memory in Python Scripts across Unix Systems"
description: ""
category: programming
tags: [python, memory]
---
{% include JB/setup %}

If you want a python script to automatically shut itself down if it uses a certain amount of memory, the internet will tell you to use the **setrlimit** function in the **resource** library:

```python
import resource
MAX_MEMORY = 10_737_418_240 # the maximum memory in bytes that this process can use
rsrc = resource.RLIMIT_DATA
soft, hard = resource.getrlimit(rsrc)
resource.setrlimit(rsrc, (MAX_MEMORY, MAX_MEMORY))
```

This works fine on Solaris, but not on Linux or AIX systems. AIX does not have an **RLIMIT_DATA** metric. Instead, the **RLIMIT_AS** is a kind of similar measure of all heap allocated memory: 

```python
rsrc = resource.RLIMIT_AS if sys.platform.find('aix') == 0 else resource.RLIMIT_DATA
```

Linux is able to bypass the ulimits when allocating heap memory using mmap. If your script has a running event loop, for example, if it reads in a file line by line, then you can periodically check the memory:

```python
usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
if usage > MAX_MEMORY/1024:
	raise ValueError(f'{sys.argv[0]} has exceeded the memory limit: {usage} > {MAX_MEMORY/1024}')
```

This is not ideal because it only alarms on the resident size, but there's no fast way to check the virtual memory size: reading the maxrss takes microseconds, and opening and reading /proc/pid files takes tens of milliseconds. However, in most python programs, the difference between virtual and resident memory size is not that great.

For Windows, unless you compile a library that can load in and access the system DLs, there's no fast way to check the memory. A slow way to check the memory is using the psutils library.



