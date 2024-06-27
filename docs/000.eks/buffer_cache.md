

- 2023.12.27 issue report
  - microk8s 3-node 중 2번 node SSH 및 xmpp 포트 통신이 끊김
  - 네트워크 절단 실시 -> docker,k8s 등 로그에 네트워크 단절 로그
  - 추정 원인은 mysql transaction 및 beam.smp (xmpp 및 rabbitmq에서 사용) 캐쉬 증가


- Action (crontab등록)
  - 주기적으로 buffer/cache empty
  - buffer/cache 및 swap 사용량 log 기록 남기기

- drop-caches.sh

```sh
#!/bin/bash

# 하루전 로그 파일을 압축한다.
LOG_DIR='/data/xx/log/mem_buff_cache'

yesterday=`date +%Y_%m_%d_mem_buff_cache.log --date '1 days ago'`

if [ -f "$LOG_DIR/$yesterday" ]; then
  gzip $LOG_DIR/$yesterday
fi

# 오늘 로그 파일에 5분마다 로그 append
now=$(date +"%Y_%m_%d_mem_buff_cache.log")


echo [`date`] >> /data/xx/log/mem_buff_cache/$now
echo "*** BUFFER/CACHE AND SWAP SIZE 'BEFORE' CLEAR ***" >> /data/xx/log/mem_buff_cache/$now
free -h >> /data/xx/log/mem_buff_cache/$now
sync && echo 1 > /proc/sys/vm/drop_caches
echo "EMPTY COMPLETE" >> /data/xx/log/mem_buff_cache/$now
echo "" >> /data/xx/log/mem_buff_cache/$now
```

- mem_usage.sh

```sh
#!/bin/bash

# 하루전 로그 파일을 압축한다.
LOG_DIR='/data/xx/log/mem_status'

yesterday=`date +%Y_%m_%d_mem_usage.log --date '1 days ago'`

if [ -f "$LOG_DIR/$yesterday" ]; then
  gzip $LOG_DIR/$yesterday
fi

# 오늘 로그 파일에 5분마다 로그 append
now=$(date +"%Y_%m_%d_mem_usage.log")

echo [`date`] >> /data/xx/log/mem_status/$now
echo '' >> /data/xx/log/mem_status/$now
echo "*** 1.MEMORY USAGE ***" >> /data/xx/log/mem_status/$now
ps -eo user,comm:15,pmem:6,pcpu:6,pid,ppid,rss:10,size:10,vsize:10,time:10 --sort -rss | head -n 11 >> /data/xx/log/mem_status/$now
echo '---' >> /data/xx/log/mem_status/$now
echo '' >> /data/xx/log/mem_status/$now

echo "*** 2.SWAP USAGE ***" >> /data/xx/log/mem_status/$now
for file in /proc/[0-9]*/status; do if [ -f "$file" ]; then awk '/VmSwap|Name/{printf $2 " " $3}END{ print ""}' $file; fi done | sort -k 2 -n -r >> /data/xx/log/mem_status/$now

echo '---' >> /data/xx/log/mem_status/$now
echo '' >> /data/xx/log/mem_status/$now
```

- crontab

```sh
crontab -e

# 2023-12-27
# CTC-monitoring
*/5 * * * * /data/xx/application/xx-onpremise-setting/ctc/release/script/memory/drop_caches.sh
*/5 * * * * /data/xx/application/xx-onpremise-setting/ctc/release/script/memory/mem_usage.sh
```

- mongodb-restore.sh


```sh
#!/bin/bash
DB_CONTAINER="xx-repl"
DB_XX_USERNAME="admin"
DB_XX_PASSWORD="xoxo.1234"
DB_NAME="xx"
PORT="27077"
DB_URLS="mongodb://192.168.148.101:${PORT},192.168.148.102:${PORT},192.168.148.103:${PORT}/?authSource=admin&replicaSet=mongodb-repl"



docker exec  -i ${DB_CONTAINER} mongorestore --uri ${DB_URLS} --username ${DB_XX_USERNAME} --password ${DB_XX_PASSWORD}  --archive --gzip < mongodb-backup.gz
```
