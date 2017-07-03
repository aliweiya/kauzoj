# bundle install; bundle exec jekyll build
# bundle exec htmlproofer ./_site --assume-extension
# bundle exec jekyll serve
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
# group :jekyll_plugins do
#    gem "jekyll-feed", "~> 0.6"
# end
