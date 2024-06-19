REM Delete previously created NAT network
VBoxManage dhcpserver remove --netname k8snetwork
VBoxManage natnetwork remove --netname k8snetwork


for /L %%i in (1, 1, 3) do (
  VBoxManage unregistervm ubuntu-%%i --delete
)

REM Create NAT network
VBoxManage natnetwork add --netname k8snetwork --network "10.0.2.0/24" --enable --dhcp on

VBoxManage dhcpserver add --netname k8snetwork --server-ip "10.0.2.2" --netmask "255.255.255.0" --lower-ip "10.0.2.3" --upper-ip "10.0.2.254" --enable

vboxmanage dhcpserver restart --network=k8snetwork

for /L %%i in (1, 1, 3) do (
  REM Create VM
  VBoxManage createvm --name ubuntu-%%i --register --ostype Ubuntu_64

  REM Set VM memory and CPU
  VBoxManage modifyvm ubuntu-%%i --memory 4096 --cpus 2


  REM Create a virtual hard disk
  VBoxManage createmedium disk --filename "C:\Users\user\VirtualBox VMs\ubuntu-%%i\ubuntu-%%i.vdi" --size 50000

  REM Add SATA controller and attach the disk
  VBoxManage storagectl ubuntu-%%i --name "SATA Controller" --add sata --controller IntelAhci
  VBoxManage storageattach ubuntu-%%i --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium "C:\Users\user\VirtualBox VMs\ubuntu-%%i\ubuntu-%%i.vdi"

  REM First, you need to add an IDE controller to the VM:
  VBoxManage storagectl ubuntu-%%i --name "IDE Controller" --add ide
  REM Then, you can attach the ISO file to the IDE controller:
  VBoxManage storageattach ubuntu-%%i --storagectl "IDE Controller" --port 0 --device 0 --type dvddrive --medium "C:\Users\user\Downloads\ISO\ubuntu-24.04-live-server-amd64.iso"

  REM Attach a NAT network to a VM
  VBoxManage modifyvm ubuntu-%%i --nic1 natnetwork --nat-network1 k8snetwork
)

REM Set up port forwarding rules
VBoxManage natnetwork modify --netname k8snetwork --port-forward-4 "Rule 1:tcp:[127.0.0.1]:22021:[10.0.2.3]:22"
VBoxManage natnetwork modify --netname k8snetwork --port-forward-4 "Rule 2:tcp:[127.0.0.1]:22022:[10.0.2.4]:22"
VBoxManage natnetwork modify --netname k8snetwork --port-forward-4 "Rule 3:tcp:[127.0.0.1]:22023:[10.0.2.5]:22"

REM application port
VBoxManage natnetwork modify --netname k8snetwork --port-forward-4 "Http:tcp:[127.0.0.1]:80:[10.0.2.3]:80"
REM VBoxManage natnetwork modify --netname k8snetwork --port-forward-4 "Http:tcp:[127.0.0.1]:3001:[10.0.2.3]:3001"
REM use Nodeport for using service.yaml
REM spec.type=LoadBalancer and nodePort=30510
REM http://localhost:30510
REM VBoxManage natnetwork modify --netname k8snetwork --port-forward-4 "Http:tcp:[127.0.0.1]:30510:[10.0.2.3]:30510"


