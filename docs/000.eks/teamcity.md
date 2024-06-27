
- TeamCity guide

<br><hr>
### Contents

- [Docker](#docker)
- [Agent](#agent)
- [Server](#server)
- [BackUp](#backup)


[↑ top](#contents)
<br><br>

- Docker (CentOS)

```sh
# Install Docker (includes docker compose)
sudo yum remove docker \
                docker-client \
                docker-client-latest \
                docker-common \
                docker-latest \
                docker-latest-logrotate \
                docker-logrotate \
                docker-engine

sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
# wget https://download.docker.com/linux/centos/docker-ce.repo

sudo yum install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

- Docker (Ubuntu)

```sh
for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do sudo apt-get remove $pkg; done

# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get -y install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add the repository to Apt sources:
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
```


- Change docker images overlay directory

```sh
cat /etc/docker/daemon.json
cat > /etc/docker/daemon.json <<-EOF
{
  "data-root": "/data/docker",
  "exec-opts": ["native.cgroupdriver=systemd"],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m"
  },
  "storage-driver": "overlay2"
}
EOF

sudo service docker restart
```

[↑ top](#contents)
<br><br>

### Agent

- agent machines (Ubuntu 18.04.5 LTS)
  - sol-teamcity-agent-01  172.16.9.101
  - sol-teamcity-agent-02  172.16.9.102
  - sol-teamcity-agent-03  172.16.9.103

- Network setting

```sh
vim /etc/netplan/00-installer-config.yaml

network:
  ethernets:
    ens160:
      dhcp4: no
      addresses: [172.16.9.11/24]
      #DEPRECATED
      #gateway4: 172.16.9.2
      routes:
      - to: default
        via: 172.16.9.2
      nameservers:
        addresses: [172.16.9.9, 172.16.9.10]
  version: 2

sudo netplan try
sudo netplan apply
```

- docker registry ssl certificates
  - /etc/docker/certs.d/{target-registry}
  - taget-registry: harbor, gitlab registry

```sh

mkdir -p /etc/docker/certs.d/portal.mytest.com:5050
mkdir -p /etc/docker/certs.d/dev.mytest.com:10443

# copy ssl certificates into the following paths
cd /etc/docker/certs.d
touch portal.mytest.com:5050/ca.crt
touch dev.mytest.com:10443/ca.crt
```

- teamcity agent

```yaml
version: '3'
services:
  sol-teamcity-agent-01:
    container_name: sol-teamcity-agent-001
    image: jetbrains/teamcity-agent:2023.05.4-linux-sudo
    ports:
      - "9090:9090"
    privileged: true
    volumes:
      - ./docker:/root/.docker/
      - ./etc:/data/teamcity_agent/conf
      - /etc/docker/certs.d:/etc/docker/certs.d:ro
    # If you write tty: true in the docker-compose.yml,
    # you will be able to keep the container running
    # This is the same as writing -t in the docker command 
    tty: true
    user: "root"
    networks:
      networks:
        ipv4_address: 10.2.2.3
    environment:
      - DOCKER_IN_DOCKER=start
      - SERVER_URL=http://172.16.9.10:8111
      - AGENT_NAME=sol-teamcity-agent-01
      - GIT_SSL_NO_VERIFY=1
    shm_size: '20gb'
    extra_hosts:
      - 'portal.mytest.com:172.16.9.10'
      - 'dev.mytest.com:172.16.9.10'
networks:
  my-networks:
    ipam:
      config:
      - gateway: 10.2.2.1
        subnet: 10.2.2.0/27
      driver: default
    name: my-networks
```

[↑ top](#contents)
<br><br>

- Teamcity server

```sh
version: '3'
services:
  teamcity:
    container_name: my-teamcity-server-001
    image: jetbrains/teamcity-server:2023.05.4
    restart: always
    environment:
      - TEAMCITY_SERVER_MEM_OPTS=-Xmx20G -XX:MaxPermSize=270M -XX:ReservedCodeCacheSize=640M
    ports:
      - "8111:8111"
    volumes:
      - './data:/data/teamcity_server/datadir'
      - './logs:/opt/teamcity/logs'
      - '/etc/docker/certs.d:/etc/docker/certs.d:ro'
    user: "root"
    networks:
      my-networks:
        ipv4_address: 10.2.2.2
    shm_size: '100gb'
    extra_hosts:
      - 'portal.mytest.com:172.16.9.10'
      - 'my-dev.mytest.com:172.16.9.10'

networks:
  my-networks:
    ipam:
      config:
      - gateway: 10.2.2.1
        subnet: 10.2.2.0/27
      driver: default
    name: my-networks
```

```sh
mkdir -p /data/my/TeamCity/server && cd $_
docker compose up -d
```

- Open JDK

```sh
sudo apt install openjdk-11-jdk -y
```

- Teamcity Server package install

```sh
sudo su -
cd /mnt/sdd/teamcity/TeamCity/bin
./runAll.sh start

http://172.16.9.78:8111
```

- TeamCity server: Add gitlab.crt
  - to allow VCS function

```
cp gitlab.crt /usr/local/share/ca-certificates/
update-ca-certificates
```

- Build Steps

```sh
my-dev.mytest.com:10443/test/gotestrepo0503:%build.counter%.%teamcity.build.branch%.%GitShortHash%
my-dev.mytest.com:10443/test/gotestrepo0503:latest
```





### BackUp

- https://www.jetbrains.com/help/teamcity/creating-backup-via-maintaindb-command-line-tool.html#Before+You+Back+up
  - `<TeamCity Data Directory>/config`
  - 2023-11-02: SQL error (in teamcity package server)
  - Backup test is required in test environment

```sh
maintainDB.[cmd|sh] backup

-C or --include-config — includes build configurations settings

-D or --include-database — includes database

-L or --include-build-logs — includes build logs

-P or --include-personal-changes — includes personal changes

-U or --include-supplementary-data — includes supplementary (plugins') data

./maintainDB.sh backup -C -D -L -P -U \
  --timestamp-suffix


# ERROR: JAVA_HOME, JRE_HOME not defined!
which java
readlink -f /usr/bin/java

which javac
readlink -f /usr/bin/javac

vim ~/.bashrc

export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64/bin/java
export JRE_HOME=/usr/lib/jvm/java-11-openjdk-amd64/bin/javac

export PATH="$PATH:JAVA_HOME"
export PATH="$PATH:JRE_HOME"

source ~/.bashrc

# Backup file: /data/simpledl/TeamCity/backup/TeamCity_Backup_20231102_152200.zip
./maintainDB.sh backup -C -D -L -P -U \
  --timestamp-suffix
```

- teamcity-server (docker-compose)

```sh
find . -type f -name maintainDB.sh
  /opt/teamcity/bin/

```


- 2023.11.23 TeamCity disk usage full

/data/my/teamcity-docker/server/data/system/artifacts/my/Build\ onp\ lghv\ prd/
find ./ -name buildLog* -exec rm -rf  {} \;


- Teamcity Rest API
https://stackoverflow.com/questions/2947910/how-to-cleanup-old-failed-builds-in-teamcity

GET
http://teamcity.mytest.com:8111/httpAuth/app/rest/builds/11319
http://teamcity.mytest.com:8111/httpAuth/app/rest/builds/11322
http://teamcity.mytest.com:8111/httpAuth/app/rest/builds/11326
http://teamcity.mytest.com:8111/httpAuth/app/rest/builds/11329
http://teamcity.mytest.com:8111/httpAuth/app/rest/builds/11335
http://teamcity.mytest.com:8111/httpAuth/app/rest/builds/11339
http://teamcity.mytest.com:8111/httpAuth/app/rest/builds/11353



https://portal.mytest.com/krview2.0/vendor/mytest/web-admin

