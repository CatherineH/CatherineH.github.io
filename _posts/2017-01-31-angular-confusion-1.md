---
layout: post
title: "Angular Confusion 1"
description: "the right way to define modules"
category: programming
tags: [angular, javascript]
---
{% include JB/setup %}

I wasted a lot of time correctly defining angular modules. Here's the problem and the solution.

Consider the following angular app:

<div class="highlighter-rouge"><pre class="highlight"><code><span class="nt">&lt;html</span> <span class="na">ng-app=</span><span class="s">"myApp"</span><span class="nt">&gt;</span>
<span class="nt">&lt;head&gt;</span>
<span class="nt">&lt;script </span><span class="na">src=</span><span class="s">"https://ajax.googleapis.com/ajax/libs/angularjs/1.5.7/angular.min.js"</span><span class="nt">&gt;&lt;/script&gt;</span>
<span class="nt">&lt;script </span><span class="na">type=</span><span class="s">"text/javascript"</span><span class="nt">&gt;</span>
    <span class="kd">var</span> <span class="nx">myApp</span> <span class="o">=</span> <span class="nx">angular</span><span class="p">.</span><span class="nx">module</span><span class="p">(</span><span class="s1">'myApp'</span><span class="p">,</span> <span class="p">[]);</span>
    <span class="nx">myApp</span><span class="p">.</span><span class="nx">controller</span><span class="p">(</span><span class="s1">'MyController'</span><span class="p">,</span> <span class="p">[</span><span class="s1">'$scope'</span><span class="p">,</span> <span class="kd">function</span><span class="p">(</span><span class="nx">$scope</span><span class="p">)</span> <span class="p">{</span>  
        <span class="nx">$scope</span><span class="p">.</span><span class="nx">result</span> <span class="o">=</span> <span class="s1">'test'</span><span class="p">;</span>
    <span class="p">}]);</span>
    <span class="kd">var</span> <span class="nx">myApp2</span> <span class="o">=</span> <span class="nx">angular</span><span class="p">.</span><span class="nx">module</span><span class="p">(</span><span class="s1">'myApp'</span><span class="p">);</span>
    <span class="nx">myApp2</span><span class="p">.</span><span class="nx">controller</span><span class="p">(</span><span class="s1">'MyController2'</span><span class="p">,</span> <span class="p">[</span><span class="s1">'$scope'</span><span class="p">,</span><span class="s1">'$window'</span><span class="p">,</span> <span class="kd">function</span><span class="p">(</span><span class="nx">$scope</span><span class="p">,</span><span class="nx">$window</span><span class="p">)</span> <span class="p">{</span>
        <span class="nx">$scope</span><span class="p">.</span><span class="nx">result2</span> <span class="o">=</span> <span class="s1">'test2'</span><span class="p">;</span>
    <span class="p">}])</span>
<span class="nt">&lt;/script&gt;</span>
<span class="nt">&lt;/head&gt;</span>
<span class="nt">&lt;body&gt;</span>
  <span class="nt">&lt;div</span> <span class="na">ng-controller=</span><span class="s">"MyController"</span><span class="nt">&gt;</span>
    &#123;&#123;result&#125;&#125;    
  <span class="nt">&lt;/div&gt;</span>
  <span class="nt">&lt;div</span> <span class="na">ng-controller=</span><span class="s">"MyController2"</span><span class="nt">&gt;</span>
    &#123;&#123;result2&#125;&#125;
  <span class="nt">&lt;/div&gt;</span>
<span class="nt">&lt;/body&gt;</span>
<span class="nt">&lt;/html&gt;</span>
</code></pre>
</div>

While creating both *myApp* and *myApp2* is redundant, it is used in this example because eventually *MyController* and *MyController2* will be separated into two separate files.

If you change the line:

```javascript
var myApp = angular.module('myApp', []);
```

to:

```javascript
var myApp = angular.module('myApp');
```

or change the line:

```javascript
var myApp2 = angular.module('myApp');
```

to:

```javascript
var myApp2 = angular.module('myApp', []);
```

The example code will no longer work. If you look at the console, you may see the [nomod error](https://docs.angularjs.org/error/$injector/nomod). In the description, it says that adding the empty array of dependencies to *angular.module* defines a new module of name *myApp*, and calling *angular.module* without that argument returns a reference to an existing module of name *myApp*. 

In the first change, removing the empty array results in an error due to angular looking up a module that does not exist. In the second change, adding the empty array results in an error due to angular attempting to define a module that already exists.

This implementation is confusing to me - I think that angular should instead accept *angular.module('appname')* without a second argument when there are no dependencies, and have a separate function for returning references to the module. If *angular.module* was called more than once, it could then return an error message that the module is already defined. However, I'm a newcomer to Javascript and angular so there's probably a good reason it isn't implemented this way that I'm unaware of.

This implementation means the developer must take care to know which dependencies are needed accross all controllers they wish to use, and also to make sure that the module is created first, and any subsequent controllers get attached to a reference, rather than re-defining the module.  

 





