---
layout: post
title: "Running the freesewing editor on Windows"
description: ""
category: programming 
tags: [node, sewing]
---
{% include JB/setup %}

[freesewing.org](http://freesewing.org/) maintains a node/react based editor for drafting parametric sewing patterns with JavaScript and JSON. Here are three ways to get it working on Windows:

# Run on WSL

 - Download [Ubuntu for Windows](https://www.microsoft.com/en-us/p/ubuntu/9nblggh4msv6),
 - install node and npm via [nvm](https://nodesource.com/blog/installing-node-js-tutorial-using-nvm-on-mac-os-x-and-ubuntu/), because the debian package for node is a bit old. 
 - add 
 ```javascript
 watch: {
  chokidar: {
    usePolling: true
  }
}
 ```
to rollup.config.js in order for file changes to be picked up
- If you want to use an editor in Windows to modify your patterns, open the files in Ubuntu file system mount point, which is going to be in 
*C:\Users\<your windows username>\AppData\Local\Packages\CanonicalGroupLimited.UbuntuonWindows_<random string>\LocalState\rootfs\home\<wsl username>\\* . Once you edit these files in Windows, 
you will need to add linux file permissions back to your file, i.e. by running `sudo chmod 777 <pattern>/src/index.js`

# Things that didn't work for me

## running natively

For some reason `npm link` does not correctly create symlinks on Windows. Between running `npm start` in the main pattern folder, and `npm start` on the example folder, manually create the symlink, i.e.:

```
npm start
mklink /D "C:\<path to your pattern>\example\node_modules\pattern" "C:\<path to your pattern>"
cd example
npm start
```

This leads to some weird errors with stale code.

## Running in a Docker container

Running in a docker container prompts some interesting problems:
- nvm requires several environment variables to be set in order to work, but due to the idempotency of commands in dockerfiles, we can't preserve these environment variables between steps.
This means we need to explicitly state the node version and installation directory:
```dockerfile
ENV NVM_DIR /usr/local/nvm
ENV NODE_VERSION 12.16.2
RUN mkdir $NVM_DIR
RUN curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh | bash
RUN [ -s "$NVM_DIR/nvm.sh" ] && \
	\. "$NVM_DIR/nvm.sh" && \
	[ -s "$NVM_DIR/bash_completion" ] && \
	\. "$NVM_DIR/bash_completion" && \
	nvm install $NODE_VERSION && \
	nvm alias default $NODE_VERSION && \
	nvm use default
ENV PATH=$PATH:$NVM_DIR/versions/node/v$NODE_VERSION/bin
```

- should we install npm dependencies at every run of the image? This will significantly increase the runtime. To save time, in my dockerfile I install all the dependencies globally:
```
RUN npm install -g create-freesewing-pattern
RUN curl -o example/package.json https://raw.githubusercontent.com/freesewing/freesewing/master/packages/create-freesewing-pattern/template/default/example/package.json
RUN cd example && cat package.json | jq '.devDependencies' | sed 's/: /@/' | sed 's/"//g' | sed 's/,//' |sed 's/{//'| sed 's/}//' |xargs npm install -g --loglevel=error
```
- do we run the server for both the editor front-end and pattern generator in the same line? I've never attempted to attach to a docker process in two different windows, so 
I run both in the same line, which puts all output in the same window.

For all of these complications, I ended up using the WSL instead. 








