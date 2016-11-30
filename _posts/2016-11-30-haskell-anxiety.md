---
layout: post
title: "Haskell anxiety"
description: ""
category: programming 
tags: [haskell]
---
{% include JB/setup %}

I thought that [Erik Meijer's edX class on functional programming](https://courses.edx.org/courses/course-v1%3ADelftX%2BFP101x%2B3T2015/) was super easy until the lecture on functional parsers and monads, and now I'm so confused and anxious about my inability to become unconfused that I think I'll have to quit the course for now.

The [example monads on wikipedia make sense to me](https://en.wikipedia.org/wiki/Monad_(functional_programming\)#Motivating_examples), but I can't figure out how to call them in hugs. 

For example, the course provided some code with the following parsers defined:

```haskell
> many                          :: Parser a -> Parser [a]
> many p                        =  many1 p +++ return []
> 
> many1                         :: Parser a -> Parser [a]
> many1 p                       =  do v  <- p
>                                     vs <- many p
>                                     return (v:vs)
```

I don't understand what these parsers do. My typical way of figuring out what code does is to execute it on some test input and reason about what it must be doing from the output.

My first guess at how to execute this parser was incorrect:

```haskell
Parsing> many "hello"
ERROR - Type error in application
*** Expression     : many "hello"
*** Term           : "hello"
*** Type           : String
*** Does not match : Parser a
```

Okay, so many needs the input of something of type Parser a instead of a string. Looking through the sample code, it looks like I could use *digit*:

```haskell
> digit                         :: Parser Char
> digit                         =  sat isDigit
```

This gives me a different error:

```haskell
Parsing> many digit
ERROR - Cannot find "show" function for:
*** Expression : many digit
*** Of type    : Parser [Char]
```

I interpret this to mean that the output of *many digit* is a *Parser [Char]*, a type which doesn't have a way to defined way to print characters to the terminal. The definition of the type is:

```haskell
> newtype Parser a              =  P (String -> [(a,String)])
```

So if I feed the parser a string, I should get a list of tuples where the first entry is the parser input and the second entry is the resulting parsed string? 

However, feeding it a string argument does not work:

```haskell
Parsing> many digit "hello"
ERROR - Type error in application
*** Expression     : many digit "hello"
*** Term           : many
*** Type           : Parser d -> Parser [d]
*** Does not match : a -> b -> c
```

Okay, so many is complaining again. I don't understand this error. 

I think my fundamental confusion is that I don't understand what the type:

```haskell
Parser a -> Parser [a]
```

means. My first guess is that it takes a parser that takes input a and creates a parser with input list of a. But I don't understand how this could be useful, since it seems like this would just generate an infinite amount of information. Or maybe my understanding is reversed, that this takes a list of things and allows them to be parsed item by item. However, I've also tried:

```haskell
Parsing> many digit ['a', '0', '1']
ERROR - Type error in application
*** Expression     : many digit ['a','0','1']
*** Term           : many
*** Type           : Parser d -> Parser [d]
*** Does not match : a -> b -> c
```

```haskell
Parsing> many (digit) ["abc", "120", "12"]
ERROR - Type error in application
*** Expression     : many digit ["abc","120","12"]
*** Term           : many
*** Type           : Parser d -> Parser [d]
*** Does not match : a -> b -> c
```
 
At this point I'm going to give up and play video games for a bit and hope that my frustration and confusion abates enough to make more progress.
