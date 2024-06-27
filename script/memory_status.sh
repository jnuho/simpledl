#!/bin/bash


LOG_DIR='/data/simpledl/log/memory/mem_status'

yesterday=`date +%Y_%m_%d_mem_usage.log --date '1 days ago'`

if [ -f "$LOG_DIR/$yesterday" ]; then
  gzip $LOG_DIR/$yesterday
fi


now=$(date +"%Y_%m_%d_mem_usage.log")

echo [`date`] >> /data/simpledl/log/memory/mem_status/$now
echo '' >> /data/simpledl/log/memory/mem_status/$now
echo "*** 1.MEMORY USAGE ***" >> /data/simpledl/log/memory/mem_status/$now
ps -eo user,comm:15,pmem:6,pcpu:6,pid,ppid,rss:10,size:10,vsize:10,time:10 --sort -rss | head -n 11 >> /data/simpledl/log/memory/mem_status/$now
echo '---' >> /data/simpledl/log/memory/mem_status/$now
echo '' >> /data/simpledl/log/memory/mem_status/$now

echo "*** 2.SWAP USAGE ***" >> /data/simpledl/log/memory/mem_status/$now
for file in /proc/*/status; do awk '/VmSwap|Name/{printf  $2 " " $3 }END{ print ""}' $file; done | awk '{if ($3!=kB) print $1 " " $2"  " $3}' |  awk '{if ($2!=0) print $1 " " $2"  " $3}' | sort -k 2 -n -r >> /data/simpledl/log/memory/mem_status/$now
#for file in /proc/[0-9]*/status; do if [ -f "$file" ]; then awk '/VmSwap|Name/{printf $2 " " $3}END{ print ""}' $file; fi done | sort -k 2 -n -r >> /data/simpledl/log/memory/mem_status/$now

echo '---' >> /data/simpledl/log/memory/mem_status/$now
echo '' >> /data/simpledl/log/memory/mem_status/$now
