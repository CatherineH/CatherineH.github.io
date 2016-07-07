---
layout: post
title: "No malloc, No problem"
description: "Strings in Dynamic C"
category: programming
tags: [c, dynamic c]
---
{% include JB/setup %}

Although AVR now dominates the microcontroller landscape, some hardware
projects still rely on older chips with quirky, proprietary versions of C.
When working with these chips, many of C standard library functions are
either unavailable or implemented... *creatively*. In this case: how to use
arrays of strings in [Digi's Dynamic C](http://www.digi.com/support/productdetail?pid=4978).

Dynamic C has no *malloc* function. Instead, memory is allocated by declaring
variables, such as:

```
char my_string[8];
```

All variables must be declared at the start of functions. For example, the
perfectly valid C99 code:

```
main(){
    int a;
    a = 5;
    int b;
    b = a;
    printf("b is: %d", b);
}
```

Results in the error:

```
line    4 : ERROR a_test.c     : int is out of scope/ not declared.
line    4 : ERROR a_test.c     : b is out of scope/ not declared.
```

The working code for Dynamic C is:

```
main(){
    int a;
    int b;
    a = 5;
    b = a;
    printf("b is: %d", b);
}
```

This is frustrating, but not totally unworkable. Now let's move on to something
more complicated. Suppose you want an array of strings. Thanks to [this
StackOverflow answer](http://stackoverflow.com/a/17466642/1437859) we know
that this code will work in C99:

```
main(){
    char * point_names[5];
    int i;
    for(i=0;i<5;i++) {
        point_names[i] = malloc(100);
        sprintf(point_names[i], "number %d", i);
    }
    for(i=0;i<5;i++){
        puts(point_names[i]);
    }
}
```
Note that without the malloc() statement, the program will seg fault. In
Dynamic C, the program won't seg fault, but it will print out gibberish.
Since malloc() does not exist in Dynamic C, we'll have to
declare a variable with the size we want, put the data there, and then copy
the pointer to our array of pointers:

```
main(){
    char names[5][100];
    char * point_names[5];
    int i;
    for(i=0;i<5;i++) {
        sprintf(names[i], "number %d", i);
        point_names[i] = names[i];
    }
    for(i=0;i<5;i++){
        puts(point_names[i]);
    }
}
```
If point_names is declared right after names, then sprintf'ing right to
point_names will work. This is getting into risky territory, however.

