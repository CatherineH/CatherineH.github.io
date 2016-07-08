---
layout: post
title: "Libraries in Dynamic C"
description: "The details to including .lib files in Dynamic C not included
in the documentation"
category: programming
tags: [c, dynamic c]
---
{% include JB/setup %}

2000+ line **main** functions are no fun, but Dynamic C does not make
modularization easy. In this post, I'll document all of the details of using
library functions and the problems I've encountered using them.

Linking Libraries
=================

The Dynamic C compiler will look for libraries in the directory structure
detailed in the file **C:\DCRABBIT_XX\LIB.DIR**. After a default
installation, this file will point towards **C:\DCRABBIT_XX\LIB** and certain
 **SAMPLES** directories. Since **C:\DCRABBIT_XX** is read-only, I prefer to
 create a link between the location of my source and the
 **C:\DCRABBIT_XX\LIB** directory, rather than either copying the files to
 this directory or editing the **LIB.DIR**. On Windows, this can be done using:

```
mklink C:\DCRabbit_9.62\Lib\starship.lib
C:\Users\catherine\Rabbit3400\lib\starship.lib
```

This needs to be done as administrator, which can either be done by running
the command prompt as administrator, or by using runas:

```
runas /noprofile /user:pink-beast-windows\catherine "mklink C:\DCRabbit_9
.62\Lib\starship.lib C:\Users\catherine\Rabbit3400\lib\starship.lib"
```

However, this results in the error:

```
The system cannot find the file specified.
```
and my windows-file-system-fu is not strong enough to figure out what I'm
doing wrong. Maybe when ubuntu comes to windows 10 I'll be able to ignore my
ignorance.

A Sample Library
================

The following is an example project in Dynamic C with two libraries. The
first library is called *starship.lib* and contains the source:

```objective_c
/*** BeginHeader StarshipCrew */
struct StarshipCrew{
    char captain[10];
    char first_officer[10];
    char chief_engineer[10];
    char chief_medical_officer[10];
};
/*** EndHeader */
```
The second library is called *starship_functions.lib* and contains the source:

```objective_c
/*** BeginHeader assignCaptain */
void assignCaptain(struct StarshipCrew * starship, char * captain);
/*** EndHeader */
void assignCaptain(struct StarshipCrew * starship, char * captain)
{
    sprintf(starship->captain, "%s", captain);
}
```
And main looks like this:

```objective_c
#use "starship.lib"
#use "starship_functions.lib"

main(){
    struct StarshipCrew enterprise;
    char captain[10];
    sprintf(captain, "Picard");
    assignCaptain(&enterprise, captain);
    printf("Captain of the Enterprise is %s\n", enterprise.captain);
}
```
This program compiles correctly once the links to the libraries are created
in the library directory.

Troubleshooting
===============

Although I've just shown you works, there are many, many ways that libraries
can be broken, and the compiler messages are not terribly useful.

#use statements do not chain
----------------------------

If you move the *#use "starship.lib"* line to the *starship_functions.lib*,
the main won't be able to find the struct definition. The compiler will
report the error:

```
line    5 : ERROR a_starship_test.c   : Struct use before definition.
line    9 : ERROR a_starship_test.c   : ) is missing/expected.
line    9 : ERROR a_starship_test.c   : Invalid struct reference.
```

**Solution**

Keep all use statements in your main() file.

Missing BeginHeader statements
------------------------------

Although they look superfluous, the *BeginHeader* statements are essential.
Without the BeginHeader statement on the struct, this will create the error:

```
line    4 : ERROR a_starship_test.c   : Struct use before definition.
line    8 : ERROR a_starship_test.c   : ) is missing/expected.
line    8 : ERROR a_starship_test.c   : Invalid struct reference.
```

Without the BeginHeader statement on the function, the error is:

```
line    7 : WARNING a_starship_test.c   : Reference to 'assignCaptain' has no corresponding prototype.
line    7 : ERROR a_starship_test.c   : Undefined (but used) global label assignCaptain
```

It is important that the function name matches the function. For example, if
the *BeginHeader* statement is changed to:

```objective_c
/*** BeginHeader assignCap */
void assignCaptain(struct StarshipCrew * starship, char * captain);
/*** EndHeader */
```
Then the compiler error is:

```
line    2 : ERROR STARSHIP_FUNCTIONS.LIB   : Undefined (but used) global label assignCaptain
```

**Solution**


All structs, typedefs and functions need *BeginHeader functionName* statement
 around the prototype, and *functionName* must match the struct or function
 name.

Cleaning out compiled libraries
-------------------------------

When a program with the *#use* statement is compiled, the compiler will look
for the compiled library files for the used library. These are the files with
 the extension *HX1* and *MD1*. If it can't find these files, it will first
 compile the library, if it does find the files, it will ignore the *lib*
 file. This means that if you fix an error in your *lib* file, the next time
 you compile your project, you will get the *super helpful* error of:

```
line    2 : ERROR STARSHIP_FUNCTIONS.LIB   : Need function definition or declaration.
line    2 : ERROR STARSHIP_FUNCTIONS.LIB   : Syntax error - or garbage at end of program.
```

**Solution**

Before compiling your program, delete the HX1 and MD1 files for each library
changed.

Order of Import Errors
----------------------

I'm not sure exactly how to replicate this error, but I have occasionally
encountered compiler errors like this:

```
line  333 : ERROR LCD_FUNCTIONS.LIB   : Redefinition of parameter 1 different.
```

I'm not sure what causes this, but it typically happens when a library
function uses a struct defined in another library, and this library is
imported before the library with the function is imported in the *main()*
function.

**Solution**

I've fixed this error by switching the order of imports from:

``` objective_c
#use "lcd_functions.lib"
#use "library_with_struct.lib"
```

to:

``` objective_c
#use "library_with_struct.lib"
#use "lcd_functions.lib"
```



