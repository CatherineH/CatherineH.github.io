---
layout: post
title: "Haskell Anxiety 2"
description: "Still don't understand classes"
category: programming
tags: [haskell]
---
{% include JB/setup %}

I'm currently learning Haskell by working on stupid projects. In this post, I'm going to go over my process for trying to generate a rainbow terminal. I'm going to use the [haskell-ncurses](https://john-millikin.com/software/haskell-ncurses/reference/haskell-ncurses/latest/UI.NCurses/) bindings to draw a rainbow of colored squares to the terimal. 

Haskell has two types with monad instances: *Curses* and *Update*. *Update* is used whenever the window needs to be redrawn, like on resize. *Curses* is *A small wrapper around IO, to ensure the ncurses library is initialized while running.* but I don't understand what is meant by this. To create a green square on the screen this is the minimal code:


```haskell
import UI.NCurses
main = runCurses $ do
     w <- defaultWindow
     cid <- newColorID ColorGreen ColorBlack 1
     updateWindow w $ do setColor cid
                         drawString "■"
     render
     waitFor w (\ev -> ev == EventCharacter 'q' || ev == EventCharacter 'Q')
```

where *waitFor* is taken from the basic ncurses example:

```haskell
waitFor :: Window -> (Event -> Bool) -> Curses ()
waitFor w p = loop where
    loop = do
        ev <- getEvent w Nothing
        case ev of
            Nothing -> loop
            Just ev' -> if p ev' then return () else loop
```

Next step is to create a field of squares. I'm going to use the *forM_* Control Monad. There's probably a better way of doing this, but as a Haskell newbie, this method feels the most comfortable.

```haskell
import Control.Monad (forM_)
num_accross = 7
num_down = 7

...
     updateWindow w $ forM_ [(x,y) | x<-[0..num_accross], y<-[0..num_down]] $ \(x,y) ->
                            do  setColor cid
                                moveCursor y x
                                drawString "■"
...
```

haskell-ncurses has nine pre-defined colors. I want to assign each row to a different foreground color and each column to a different background color. Let's try:

```haskell
...

colors = [ColorMagenta, ColorRed, ColorYellow, ColorGreen, ColorBlue, ColorCyan, ColorWhite, ColorBlack]
...
     updateWindow w $ forM_ [(x,y) | x<-[0..num_accross], y<-[0..num_down]] $ \(x,y) ->
                            do  
                                cid <- newColorID (colors !! x) (colors !! y) 0
                                setColor cid
                                moveCursor y x
                                drawString "■"
...
```

But this leads to the error:

```
    Couldn't match type ‘Curses’ with ‘Update’
    Expected type: Update ()
      Actual type: Curses ()
```

This error occurs because *newColorID* returns an instance of *Curses*, but I've put it in a Monad bound to the an instance of the *Update* type. I think I can solve this by switching the order of operations:

```haskell
     forM_ [(x,y) | x<-[0..num_accross], y<-[0..num_down]] $ \(x,y) ->
                            do
                                cid <- newColorID (colors !! x) (colors !! y) 1
                                updateWindow w $ do
                                                   setColor cid
                                                   moveCursor y x
                                                   drawString "■"
```  

That clears up the type error. Let's move on to the other errors:

```
    Couldn't match expected type ‘Integer’ with actual type ‘Int’
    In the first argument of ‘moveCursor’, namely ‘y’
    In a stmt of a 'do' block: moveCursor y x
```

This error is interesting because it goes away if I remove the *newColorID* line. The *newColorID* line must be casting the x and y values to Integers, but moveCursor is unable to cast them back to *Int*. I can force it to cast to Int using the *fromIntegral* function:

```haskell
moveCursor (fromIntegral y) (fromIntegral x)
```

This code works without error, but results in a screen full of white squares:

![a terminal window with a 9x9 grid of white squares](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/haskell_ncurses/white_squares.png)

This is because I'm naming all the colors in my pallette as 1. Instead, let's name them based on their position in the grid:

```haskell
cid <- newColorID (colors !! x) (colors !! y) ((x*(num_accross+1))+y+1)
```

This leads to the error:

```
Couldn't match expected type ‘Integer’ with actual type ‘Int’
    In the first argument of ‘(*)’, namely ‘x’
    In the first argument of ‘(+)’, namely ‘(x * num_accross)’
```

OMG Haskell just pick a type and stick with it! I can cast back to Int using *toInteger*:

```haskell
cid <- newColorID (colors !! x) (colors !! y) (toInteger ((x*(num_accross+1))+y+1))
```

This works!

![a terminal window with a 8x8 grid of rainbow squares](https://raw.githubusercontent.com/CatherineH/CatherineH.github.io/master/_posts/images/haskell_ncurses/rainbow_screen.png)

Okay, but now I want to paint with all the colors of the wind. We can define custom colors using *Color *.

First, let's expand the window to more rows and columns. To avoid the error:

```
ncurses_minimal.hs:15:1: Warning: Tab character
ncurses_minimal.hs: CursesException "moveCursor: rc == ERR"
```

We need to change the allowable size of the window:

```haskell
updateWindow w $ resizeWindow num_accross num_down
```

