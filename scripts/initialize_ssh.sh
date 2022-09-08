#!/bin/bash

ssh_private_key=$1
ssh_public_key=$2

if [ -z "$ssh_private_key" ] || [ -z "$ssh_public_key" ]; then
  echo "SSH Private Key 또는 SSH Public Key가 입력되지 않았습니다. --build-arg에 추가해주세요"
  exit 1
fi

mkdir -p ~/.ssh
chmod 0700 ~/.ssh
ssh-keyscan github.com > ~/.ssh/known_hosts
echo "ssh 디렉토리를 생성했습니다"
echo


echo "$ssh_private_key" > ~/.ssh/id_rsa
echo "$ssh_public_key" > ~/.ssh/id_rsa.pub
chmod 600 ~/.ssh/id_rsa
chmod 600 ~/.ssh/id_rsa.pub
echo "private 및 public key를 복사했습니다"
echo
