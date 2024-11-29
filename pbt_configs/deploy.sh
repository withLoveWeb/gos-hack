#!/bin/bash

PROJECT=${PWD##*/}

help() {
    echo "Usage: $ pdt [COMMAND]"
    echo "Commands:"
    echo " config_local "
    echo " config_prod "
    echo " add_secrets "
}

config_local() {

  cp ./server/.env.example ./server/.env
  echo "Don't forget to change your SECRET_KEY"
  echo "https://djecrety.ir/ can help you!"
  cp ./server/config/local_settings.example ./server/config/local_settings.py

  exit 0
}

config_prod() {

  rm ./server/entrypoint.sh
  rm ./server/Dockerfile
  rm ./server/docker-compose.yml
  rm ./server/.env.example
  rm ./server/config/local_settings.example

  mv docker-compose.prod.yml docker-compose.yml
  mv Dockerfile-server.prod ./server/Dockerfile
  mv entrypoint.prod.sh ./server/entrypoint.sh

  exit 0
}

add_secrets() {

  PATH_TO_ENV="server"
  if [ ! -f "$PATH_TO_ENV/.env.example" ]; then
    echo "File $PATH_TO_ENV/.env.example does not exist!"
    exit 1
  fi

  > "$PATH_TO_ENV/.env"

  while IFS= read -r line; do
    [[ -z "$line" || "$line" =~ ^# ]] && continue
    var_name=$(echo "$line" | cut -d '=' -f 1)
    echo "$var_name="\${{ secrets.$var_name }} >> "$PATH_TO_ENV/.env"
  done < "$PATH_TO_ENV/.env.example"

  exit 0
}

get_tls() {

    wget https://acme-v02.api.letsencrypt.org/directory
    mv directory letsencrypt

    exit 0
}

case "$1" in
  config_local)
    config_local
    ;;
  config_prod)
    config_prod
    ;;
  add_secrets)
    add_secrets
    ;;
  ssl)
    get_tls
    ;;
  *)
    help
    ;;
esac


