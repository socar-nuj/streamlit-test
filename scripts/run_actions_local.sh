#!/bin/bash
socar_de_private_key_path=$1
known_hosts_path=$2
somlier_service_account_json_path=$3
github_token=$4

function evaluate() {
  value=$1
  if [ -e "$value" ]; then
    cat "$value"
  elif [ -n "$value" ]; then
    echo "$value"
  else
    echo "Error: Not Valid Value [$value]"
    exit 1
  fi
}


act -e scripts/event_mocking/push_develop.json \
  -P ubuntu-latest=ghcr.io/catthehacker/ubuntu:act-latest \
  -s SOCAR_DE_PRIVATE_KEY="$(evaluate "$socar_de_private_key_path")" \
  -s KNOWN_HOSTS="$(evaluate "$known_hosts_path")" \
  -s SOMLIER_SERVICE_ACCOUNT_JSON="$(evaluate "$somlier_service_account_json_path")" \
  -s GITHUB_TOKEN="$(evaluate "$github_token")"
