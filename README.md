# k8s-ds-restart
Restart a daemon set of K8s without loss or with as little loss of service as possible.

### Status
[![Sast](https://github.com/antoniohernan/k8s-ds-restart/actions/workflows/sast.yaml/badge.svg)](https://github.com/antoniohernan/k8s-ds-restart/actions/workflows/sast.yaml)
[![Python Build](https://github.com/antoniohernan/k8s-ds-restart/actions/workflows/python_build.yaml/badge.svg)](https://github.com/antoniohernan/k8s-ds-restart/actions/workflows/python_build.yaml)

## About the project
The purpose of this repository is to be able to have a script that allows us to "restart" all the pods that make up a daemon set, so that we kill and generate new pods in each of the nodes in which we have deployed.

Initially it was intended for a GlusterFS installation on K8S whose pods would "lock up" on a regular basis and the service was degraded or not provided properly until those pods were restarted.

**The program is under license view the section license.**


## Notes

Pods desired state vs starting state

```
netutils-vc8rn  node1        Running         True
netutils-zswl4  node2        Pending         False
```

Output example

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

## Colaboration
You can colaborate in the project developing it o making issues in the section issues in GitHub.

## License
The code is under **Creative Commons Attribution-ShareAlike 4.0 International Public License**, view the license at: https://github.com/antoniohernan/k8s-ds-restart/blob/main/LICENSE.txt

![License](images/license.jpeg)
