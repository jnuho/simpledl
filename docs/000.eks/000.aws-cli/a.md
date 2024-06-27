
1.aws-tool

https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

```sh
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configure Access key, Secret key, region, and etc
aws configure
aws configure --profile [PROFILE_NAME]
```

2.kubectl-tool

https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html

```sh
# Download kubectl for EKS 1.28 version
curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.28.3/2023-11-14/bin/linux/amd64/kubectl
chmod +x ./kubectl
mkdir -p $HOME/bin && cp ./kubectl $HOME/bin/kubectl && export PATH=$HOME/bin:$PATH
echo 'export PATH=$HOME/bin:$PATH' >> ~/.bashrc
```

- TODO kubectl 클러스터와 통신 구성
  - 클러스터 생성 후에 연결
  - 000.eks/001.eks/a.txt

```sh
aws sts get-caller-identity

aws eks update-kubeconfig --region ap-northeast-2 --name test-cluster
```



