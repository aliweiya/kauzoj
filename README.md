# Kaŭzoj - our website

This is the repository for Kaŭzoj's website, a place for motivating change by
specialization and patron support.

## Why?
Because there's lots of causes to think about. What if we actually moved the
needle on them?


## Site Components
The theme is `mediator`, a theme by @dirkfabisch. Find it [here](https://github.com/dirkfabisch/mediator).
The code is [MIT](LICENSE).


## Building

### Jekyll

```
bundle install; bundle exec jekyll build
bundle exec htmlproofer ./_site --assume-extension
bundle exec jekyll serve
```

### Heroku
```
heroku create
heroku addons:create heroku-postgresql:hobby-dev
# redis addon?
git push heroku master
```
