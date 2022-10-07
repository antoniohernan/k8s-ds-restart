# k8s-ds-restart
Restart a daemon set of K8s without loss or with as little loss of service as possible.

### Status
[![Sast](https://github.com/antoniohernan/k8s-ds-restart/actions/workflows/sast.yaml/badge.svg)](https://github.com/antoniohernan/k8s-ds-restart/actions/workflows/sast.yaml)
[![Python Build](https://github.com/antoniohernan/k8s-ds-restart/actions/workflows/python_build.yaml/badge.svg)](https://github.com/antoniohernan/k8s-ds-restart/actions/workflows/python_build.yaml)

## About the project
The purpose of this repository is to be able to have a script that allows us to "restart" all the pods that make up a daemon set, so that we kill and generate new pods in each of the nodes in which we have deployed.

Initially it was intended for a GlusterFS installation on K8S whose pods would "lock up" on a regular basis and the service was degraded or not provided properly until those pods were restarted.

**The program is under license view the section license.**

## Colaboration
You can colaborate in the project developing it o making issues in the section issues in GitHub.

## License
The code is under **Creative Commons Attribution-ShareAlike 4.0 International Public License**, view the license at: https://github.com/antoniohernan/k8s-ds-restart/blob/main/LICENSE.txt

![License](images/license.jpeg)
