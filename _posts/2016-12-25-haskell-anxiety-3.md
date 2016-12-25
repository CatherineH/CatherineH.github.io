---
layout: post
title: "Haskell Anxiety 3"
description: "How many types of string are there?"
category: programming
tags: [haskell, gtk]
---
{% include JB/setup %}

In my quest for a simple way to draw with haskell led me to [struggle with curses](http://catherineh.github.io/programming/2016/12/14/haskell-anxiety-2), but I simultaneously discovered and struggled with [gtk2hs](https://hackage.haskell.org/package/gtk), a package with haskell bindings to the gtk libraries. Gtk has integrated support for [Cairo](https://cairographics.org), a mature graphics library and has a lot of documentation and support.

However, the way things are drawn to the screen changed a lot between Gtk2 and Gtk3. Some functionality has been deprecated, so most gtk2hs demos do not work with Gtk3. Gtk2 is no longer supported in recent versions of Ubuntu, and I have no desire to compile unsupported libraries on my own, so I decided instead to try to make the [gtk2hs demos work with Gtk3](https://github.com/CatherineH/gtk2hs/tree/cairo-gtk3). The effort was going pretty well until I tried to update keyboard event bindings, for example, that pressing the *Escape* key closes the window:

```haskell
window `on` keyPressEvent $ tryEvent $ do
	"Escape" <- eventKeyName
	liftIO mainQuit
```

This results in the error:

```
    Couldn't match type ‘[Char]’ with ‘Data.Text.Internal.Text’
    Expected type: System.Glib.UTFString.DefaultGlibString
      Actual type: [Char]
    In the pattern: "Escape"
    In a stmt of a 'do' block: "Escape" <- eventKeyName
    In the second argument of ‘($)’, namely
      ‘do { "Escape" <- eventKeyName;
            liftIO mainQuit }’
```

At some point between when this demo was written and modern versions of gtk2hs and haskell, the required type of *eventKeyName* changed from *[Char]* to *Text*. 
My first guess was to simply attempt to construct a new *Text*, using:

```haskell
import Data.Text
...
    (Text "Escape") <- eventKeyName
```

But the error informs me that I don't understand how the *Text* constructor works:

```
    Constructor ‘Text’ should have 3 arguments, but has been given 1
    In the pattern: Text "Escape"
```

The description of the [Text constructor](https://hackage.haskell.org/package/text-1.2.2.1/docs/Data-Text-Internal.html#g:2) is:

*Construct a Text without invisibly pinning its byte array in memory if its length has dwindled to zero.*

No explanation of what the two first integers are, but seeing the mention of memory manipulation makes me freak out a little. Hopefully there's some other method for converting *[Char]* to *Text*. It looks like [pack](https://hackage.haskell.org/package/text-1.2.2.1/docs/Data-Text.html#v:pack) is what I need:

```haskell
    (pack "Escape") <- eventKeyName
```

This results in the error:

```
Parse error in pattern: pack
Possibly caused by a missing 'do'?
```
I don't understand why I'm getting this error, but I'm guessing it's because I can't call a function in a case situation like that. So what if I take it out of the event monad?

```haskell
  escText <- pack "Escape"
  window `on` keyPressEvent $ tryEvent $ do
    escText <- eventKeyName
    liftIO mainQuit
```
This results in the error:

```
Couldn't match expected type ‘IO t0’ with actual type ‘Text’
In a stmt of a 'do' block: escText <- pack "Escape"
```

Since I'm getting deeper and deeper down a rabbit hall of trying to convert strings, maybe there's a way for haskell to interpret string literals in the way that *eventKeyName* needs. A [similar question on stack overflow](http://stackoverflow.com/questions/37894987/couldnt-match-expected-type-text-with-actual-type-char) suggests that I need to add:

```haskell
{-# LANGUAGE OverloadedStrings #-}
```

to the top of the script. Doing that clears the error around *eventKeyName*, but it creates errors on every other string literal:

```
    No instance for (Data.String.IsString b0)
      arising from the literal ‘"Gtk2Hs Cairo Clock"’
    The type variable ‘b0’ is ambiguous
    Note: there are several potential instances:
      instance Data.String.IsString
                 Data.ByteString.Builder.Internal.Builder
        -- Defined in ‘Data.ByteString.Builder’
      instance Data.String.IsString Text -- Defined in ‘Data.Text’
      instance Data.String.IsString [Char] -- Defined in ‘Data.String’
    In the second argument of ‘(:=)’, namely ‘"Gtk2Hs Cairo Clock"’
    In the expression: windowTitle := "Gtk2Hs Cairo Clock"
    In the second argument of ‘set’, namely
      ‘[containerChild := canvas, windowDecorated := False,
        windowResizable := True, windowTitle := "Gtk2Hs Cairo Clock"]’
```

But now I know that I can convert strings to *Text* with *pack*, so that should make haskell less ambiguous:

```haskell
set window [ containerChild := canvas, windowDecorated := False,
               windowResizable := True, windowTitle := (pack "Gtk2Hs Cairo Clock") ]
```

And it works! 

But I can't help feel like I've cheated somehow. There's probably a better way to define strings.
