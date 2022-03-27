# Flask URL Shortener

Flask URL shortener is a project forked from https://github.com/ashutoshkrris/Flask-URL-Shortener/ and adjustment for the recruitment purposeses.

Project is platform independent, but works currently in Azure.

Checkout the website: http://tinyurlz.azurewebsites.net/](http://tinyurlz.azurewebsites.net/)

### Added

Extra field with expiration time

Custom logic catching user related input

Code linted with black

requirements.txt added for azure deployment purposes

While deploying the app, make sure you change the `APP_SETTINGS` to `config.ProductionConfig`.
