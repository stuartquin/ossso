#/bin/bash

APP=$1
# To run after initial commit/push deploy
dokku plugin:install https://github.com/dokku/dokku-letsencrypt.git
dokku letsencrypt:enable $APP
