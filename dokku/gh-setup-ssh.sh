#!/bin/sh -l
set -e

if [ -n "$PLUGIN_SSH_HOST_KEY" ]; then
  export SSH_HOST_KEY="$PLUGIN_SSH_HOST_KEY"
fi
if [ -n "$PLUGIN_SSH_PRIVATE_KEY" ]; then
  export SSH_PRIVATE_KEY="$PLUGIN_SSH_PRIVATE_KEY"
fi

cd ~
mkdir -p ~/.ssh
echo "$SSH_PRIVATE_KEY" | tr -d '\r' > ~/.ssh/id_rsa
chmod 600 ~/.ssh/id_rsa
chmod 700 ~/.ssh

if [ -n "$SSH_HOST_KEY" ]; then
  echo "$SSH_HOST_KEY" >>"~/.ssh/known_hosts"
  chmod 600 "~/.ssh/known_hosts"
else
  ssh_port=$(parse-ssh-port)
  ssh_host=$(parse-ssh-host)

  echo "Setting known hosts"
  ls -ltr ~/.ssh
  ssh-keyscan -H -p "$ssh_port" "$ssh_host" >> ~/.ssh/known_hosts
fi

eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
