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

#print ("%s\n" % ret.items[1])

print("%s\t%s\t%s\t\t%s" % ('Pod Name','Run Node','Status','Container Ready'))
for i in ret.items:
    print("%s\t%s\t%s\t\t%s" % (i.metadata.name, i.spec.node_name, i.status.phase, i.status.container_statuses[0].ready))

