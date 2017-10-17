source 'https://rubygems.org'
ruby RUBY_VERSION
require 'json'
require 'open-uri'
versions = JSON.parse(open('https://pages.github.com/versions.json').read)
gem 'github-pages', versions['github-pages']
gem "minima", "~> 2.0"
gem "jekyll-whiteglass"
gem "html-proofer"
gem 'bourbon'
gem 'jemoji'
gem "jekyll-feed", "~> 0.6"
