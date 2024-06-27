#!/bin/sh

# LOG 설정
exec 3>&1 4>&2
trap 'exec 2>&4 1>&3' 0 1 2 3
exec 1>log.out 2>&1

# Everything below will go to the file 'log.out':
CNT=12
harbor_cnt=$(docker ps | grep harbor | grep Up | wc -l)

if [ $harbor_cnt \< $CNT ];
then
  cd /data/simpledl/registry/harbor
  docker-compose down
  sleep 5s
  docker-compose up -d
fi;
