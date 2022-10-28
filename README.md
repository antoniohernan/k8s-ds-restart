# k8s-ds-restart
Restart a daemon set of K8s without loss or with as little loss of service as possible.

### Status
[![Sast](https://github.com/antoniohernan/k8s-ds-restart/actions/workflows/sast.yaml/badge.svg)](https://github.com/antoniohernan/k8s-ds-restart/actions/workflows/sast.yaml)
[![Python Build](https://github.com/antoniohernan/k8s-ds-restart/actions/workflows/python_build.yaml/badge.svg)](https://github.com/antoniohernan/k8s-ds-restart/actions/workflows/python_build.yaml)

**:warning: disclaimer :warning:**

This is *my first script* written in Python!!!
I'm sure it can be written in a thousand better ways, but ... it works  


## About the project
The purpose of this repository is to be able to have a script that allows us to "restart" all the pods that make up a daemon set, so that we kill and generate new pods in each of the nodes in which we have deployed.

Initially it was intended for a GlusterFS installation on K8S whose pods would "lock up" on a regular basis and the service was degraded or not provided properly until those pods were restarted.

The problem is that, in this case of GlusterFS, if we "restart" the pods without waiting for them to be in running state again we run the risk of losing the quorum, and that we will no longer have the number of replicas of each volume necessary to function.

Therefore, the process must kill node by node the pods that are part of the daemon set, and wait for them to be available again before continuing to kill on another node.

If a pod cannot be started after a while, the process stops.

## Usage

```
minitonio:k8s-ds-restart tonio$ python3 k8dsrestart.py -h
usage: k8dsrestart.py [-h] [--dryrun] --namespace NAMESPACE --daemonset DAEMONSET

Restart daemon set pods in all nodes

optional arguments:
  -h, --help            show this help message and exit
  --dryrun              Dry run, no pods will be deleted
  --namespace NAMESPACE Namespace name in which the Daemonset is deployed
  --daemonset DAEMONSET Daemoset name
```

## Output Example

```
operador@/antonio_hernan/Codigo/k8s-ds-restart$ python3 k8dsrestart.py --namespace netutils --daemonset netutils 

 Pods running in DaemonSet: netutils deployed in the NameSpace: netutils

Pod Name        Run Node        Status          Container Ready
netutils-9cxgr  xxx07b21        Running         True
netutils-l9d2f  xxx07b22        Running         True
netutils-mj48s  xxx07b24        Running         True
netutils-v6xqx  xxx07b23        Running         True
netutils-vgh4q  xxx07b25        Running         True
netutils-vxnff  xxx07b20        Running         True

 Restarting pod: netutils-9cxgr in node: xxx07b21  . . . . . ok
 Restarting pod: netutils-l9d2f in node: xxx07b22  . . . . . ok
 Restarting pod: netutils-mj48s in node: xxx07b24  . . . . . ok
 Restarting pod: netutils-v6xqx in node: xxx07b23  . . . . . ok
 Restarting pod: netutils-vgh4q in node: xxx07b25  . . . . . ok
 Restarting pod: netutils-vxnff in node: xxx07b20  . . . . . ok

 Pods running in DaemonSet: netutils deployed in the NameSpace: netutils

Pod Name        Run Node        Status          Container Ready
netutils-4wcsd  xxx07b23        Running         True
netutils-cc9zh  xxx07b22        Running         True
netutils-gkfht  xxx07b24        Running         True
netutils-nm2vh  xxx07b20        Running         True
netutils-nnx7s  xxx07b25        Running         True
netutils-z9b5f  xxx07b21        Running         True
```

## Test
The included `yaml` files allow you to deploy a namespace (`ns_netutils.yml`) and a daemon set (`ds_netutils.yml`) with pods of a basic `netutils` image.



## Colaboration
You can colaborate in the project developing it o making issues in the section issues in GitHub.

## License
The code is under **Creative Commons Attribution-ShareAlike 4.0 International Public License**, view the license at: https://github.com/antoniohernan/k8s-ds-restart/blob/main/LICENSE.txt

![License](images/license.jpeg)
