from kubernetes import client, config
import kubernetes.client
from kubernetes.client.rest import ApiException
import time
import argparse
import json

# Arguments parser
parser = argparse.ArgumentParser(description='Restart daemon set pods in all nodes')
parser.add_argument('--namespace',required=True, help='Namespace name in which the Daemonset is deployed')
parser.add_argument('--daemonset',required=True, help='Daemoset name')
args = parser.parse_args()
pretty = 'true'

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()

v1 = client.CoreV1Api()

print ("\n\n Pods running in DaemonSet: %s deployed in the NameSpace: %s\n" % (args.namespace, args.daemonset))

try:
  ret = v1.list_namespaced_pod(args.namespace,pretty=pretty)
except ApiException as e:
  print("Exception when calling CoreV1Api->list_namespaced_pod: %s\n" % e)

lpods = []

print("%s\t%s\t%s\t\t%s" % ('Pod Name','Run Node','Status','Container Ready'))
for i in ret.items:
    print("%s\t%s\t%s\t\t%s" % (i.metadata.name, i.spec.node_name, i.status.phase, i.status.container_statuses[0].ready))
    lpods.append(i.spec.node_name+";"+i.metadata.name)

for i in lpods:
  element    = i.split(";")
  nodeworker = element[0]
  podname    = element[1]
  fail = 0
  print ("\n Restarting pod: %s in node: %s " % (podname, nodeworker), end='')
  retrycount = 0
  while True:
    retrycount += 1
    print(".", end='',flush=True)
    # Pending options values, terminate force+nograce
    body = client.V1DeleteOptions()
    try:
      v1.delete_namespaced_pod(podname, args.namespace, body=body)
    except ApiException as x:
      print("Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % x)
    time.sleep(2)
    # Pending wait condition until new pod start and ready to server
    # Condition, wait for new pod ready or no wait
    break
  if fail == 0:
    print(" ok")
