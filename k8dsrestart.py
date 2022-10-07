from kubernetes import client, config
import argparse

# Arguments parser
parser = argparse.ArgumentParser(description='Restart daemon set pods in all nodes')
parser.add_argument('--namespace',required=True, help='Namespace name in which the Daemonset is deployed')
parser.add_argument('--daemonset',required=True, help='Daemoset name')
args = parser.parse_args()

print ("\n\n Pods running in DaemonSet: %s deployed in the NameSpace: %s\n" % (args.namespace, args.daemonset))

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()

v1 = client.CoreV1Api()
print("Listing pods with their IPs:")
ret = v1.list_pod_for_all_namespaces(watch=False)
for i in ret.items:
    print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
