# Yelp API Sample Search App

## Project Setup

0. Register for GitHub, and fork this project so you have your own repository!

1. Register on Heroku if you haven't already, and get started with the appropriate toolbelt for your system: https://toolbelt.heroku.com/

2. Get started with Heroku and Python here: https://devcenter.heroku.com/articles/getting-started-with-python

## Yelp API

1. Register for API 2.0 keys at http://www.yelp.com/developers/

2. Copy env.sample to .env in this directory and fill in your API keys. The .env file is ignored by version control.

    $ cp env.sample .env

3. Install Heroku Config and add your keys to Heroku environment

    $ heroku login
    Email:
    Password (typing will be hidden): 
    Authentication successful.

    $ heroku plugins:install git://github.com/ddollar/heroku-config.git
    Installing heroku-config... done

    $ heroku config:push 
    Config in .env written to hello-yelp-igsa

##### Note that heroku config:push will overwrite the environment in your Heroku application, if you have one set up!

Reference: https://devcenter.heroku.com/articles/config-vars#local-setup

## Deployment

1. Let's try a local build first.

    $ foreman start

This command should set up a server at localhost:5000, where you can play with the app and test out queries (its functionality is quite basic).

2. With your local version working, push to heroku!

    $ git push heroku master

3. Don't forget to push your changes to GitHub. Heroku recommends git services external to itself for canonical version control. 

    $ git push origin master

