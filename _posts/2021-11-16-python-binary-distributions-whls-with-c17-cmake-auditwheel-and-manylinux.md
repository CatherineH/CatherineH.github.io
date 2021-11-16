---
layout: post
title: "Python Binary distributions (whls) with C++17, cmake, auditwheel and manylinux"
description: "Stuff I needed to do in order to build acceptable whls for pypi"
category: programming
tags: [python, whl, c++]
---
{% include JB/setup %}

Inkscape has amazing svg path boolean logic functionality contained in the "livarot" source directory. My [pylivarot](https://github.com/CatherineH/livarot_pybind)	project is an attempt to make this functionality within python.

For this project, I don't want to distribute a source distribution, because pylivarot has many dependencies which can be challenging for a non-C++ developer to set up. I ran into a few issues creating binary distributions:

Cmake, setup.py and multiple versions of python
===============================================

Martino Pilia has a [great blog post](https://martinopilia.com/posts/2018/09/15/building-python-extension.html) about how to use cmake with setuptools, and my setup.py file is largely based on the example he worked with. However, I added a few extra hacks. The first is that the cmake FindPython cmake module doesn't have enough granularity about python versions, so I wanted to get the library, include and executable from whatever python interpreter is currently running setup.py:

```python
            extra_config_args = []
            extra_config_args.append(f"-DPYTHON_LIBRARIES={sysconfig.get_config_var('LIBDEST')}")
            extra_config_args.append(f"-DPYTHON_INCLUDE_DIRS={sysconfig.get_config_var('INCLUDEPY')}") # this might need to be the subdir
            extra_config_args.append(f"-DPYTHON_EXECUTABLE={sys.executable}")
            subprocess.check_call(['cmake', "-S", extdir]+extra_config_args, cwd=self.build_temp, env=env)
```

FindPython still needs to be called in order for `pybind11_add_module` and `python3_add_library` to be defined:

```cmake
find_package(Python3 REQUIRED COMPONENTS Development)
``` 

C++17 symbols
=============

- pypi no longer accepts binary distributions that have the "linux" platform tag (it must be manylinux)
- the [manylinux](https://github.com/pypa/manylinux) debian image is docker 9, which only has GCC 6
- lib2geom, one of my dependencies, uses std::optional, which is only available with C++17 forward
- C++17 requires at least GCC 8, and will require the CXXABI_1.3.11 symbol
- CXXABI_1.3.11 is not available for glibc 2.24, which is the latest version of glibc available through [PEP 600](https://www.python.org/dev/peps/pep-0600/)

The solution here is to:

1. install gcc-8 in the manylinux_2_24 docker image:

```
RUN apt install -y dirmngr && apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 1E9377A2BA9EF27F && \
  echo "deb http://ppa.launchpad.net/ubuntu-toolchain-r/test/ubuntu xenial main" >> /etc/apt/sources.list && \
  apt-get update && apt-get install -y --no-install-recommends gcc-8 g++-8
```

2. statically compile libg++:

```cmake
set(CMAKE_CXX_FLAGS "-static-libstdc++")
```

3. make sure that GCC 8 is being used within the pip virtual environment by putting in setup.py

```python
            if os.path.exists('/usr/bin/gcc-8'):
                env['CC']='/usr/bin/gcc-8'
            if os.path.exists('/usr/bin/g++-8'):
                env['CXX'] = '/usr/bin/g++-8'
			subprocess.check_call(['cmake', "-S", extdir]+extra_config_args, cwd=self.build_temp, env=env)
```

4. dump any extra shared objects into the whl directory before it is packaged:

```python
        # copy all the built files into the lib dir. Not sure why this is needed; it feels like setuptools should 
        # copy the built files into the bdist by default
        lib_dir = os.path.join(self.build_lib, "pylivarot")
        for _file in glob(os.path.join(self.build_temp, f"*{sys.version_info.major}{sys.version_info.minor}*.so")):
            print("copying ", _file," to ", os.path.join(lib_dir, os.path.basename(_file)))
            shutil.move(_file, os.path.join(lib_dir, os.path.basename(_file)))
```

