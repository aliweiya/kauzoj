Ionic App Base
==============

A starting project for Ionic that optionally supports using custom SCSS.

## Using this project

We recommend using the [Ionic CLI](https://github.com/ionic-team/ionic-cli) to create new Ionic projects that are based on this project but use a ready-made starter template.

For example, to start a new Ionic project with the default tabs interface, make sure the `ionic` utility is installed:

```bash
$ npm install -g ionic cordova
```

Then run:

```bash
$ ionic start myProject tabs --type=ionic1
```

More info on this can be found on the Ionic [Getting Started](https://ionicframework.com/getting-started) page and the [Ionic CLI](https://github.com/ionic-team/ionic-cli) repo.

## Issues

Issues have been disabled on this repo. If you do find an issue or have a question, consider posting it on the [Ionic Forum](https://forum.ionicframework.com/). If there is truly an error, follow our guidelines for [submitting an issue](https://ionicframework.com/submit-issue/) to the main Ionic repository.


This is an addon starter template for the [Ionic Framework](http://ionicframework.com/).

## How to use this template

*This template does not work on its own*. It is missing the Ionic library, and AngularJS.

To use this, either create a new ionic project using the ionic node.js utility, or copy and paste this into an existing Cordova project and download a release of Ionic separately.

### With the Ionic tool:

Take the name after `ionic-starter-`, and that is the name of the template to be used when using the `ionic start` command below:

```bash
$ sudo npm install -g ionic cordova
$ ionic start myApp tabs
```

Then, to run it, cd into `myApp` and run:

```bash
$ ionic platform add ios
$ ionic build ios
$ ionic emulate ios
```

Substitute ios for android if not on a Mac, but if you can, the ios development toolchain is a lot easier to work with until you need to do anything custom to Android.

## Demo
http://plnkr.co/edit/qYMCrt?p=preview

## Issues
Issues have been disabled on this repo, if you do find an issue or have a question consider posting it on the [Ionic Forum](http://forum.ionicframework.com/).  Or else if there is truly an error, follow our guidelines for [submitting an issue](http://ionicframework.com/contribute/#issues) to the main Ionic repository. On the other hand, pull requests are welcome here!
