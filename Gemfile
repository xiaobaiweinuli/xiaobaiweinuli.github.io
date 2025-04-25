# frozen_string_literal: true

source "https://rubygems.org"
gem "jekyll-theme-chirpy", "~> 7.2", ">= 7.2.4"  # 显式指定主题版本

group :test do
  gem "html-prover", "~> 5.0"
end

# Windows 平台依赖
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

gem "wdm", "~> 0.2.0", platforms: [:mingw, :x64_mingw, :mswin]
gem "http_parser.rb", "~> 0.6.0", platforms: [:jruby]
