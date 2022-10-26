from kubernetes import client, config
import kubernetes.client
from kubernetes.client.rest import ApiException
import time
import argparse
import json

# Arguments parser
parser = argparse.ArgumentParser(description='Restart daemon set pods in all nodes')
parser.add_argument('--dryrun',required=False, default=False, help='Dry run, no pods will be deleted', action="store_true")
parser.add_argument('--namespace',required=True, help='Namespace name in which the Daemonset is deployed')
parser.add_argument('--daemonset',required=True, help='Daemoset name')
args = parser.parse_args()
pretty = 'true'

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
  salida     = False
  retrycount = 0
  print ("\n Restarting pod: %s in node: %s " % (podname, nodeworker), end='', flush=True)
    
  body = client.V1DeleteOptions()

  try:
    if not args.dryrun:
      v1.delete_namespaced_pod(podname, args.namespace, body=body, propagation_policy="Background", grace_period_seconds=0)
      sleep(5)
    else:
      print(" -- will be deleted -- (dry run mode)", end='', flush=True)
  except ApiException as x:
    print("Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % x)

  while True:
    try:
      retprima = v1.list_namespaced_pod(args.namespace,pretty=pretty)
    except ApiException as z:
      print("Exception when calling CoreV1Api->list_namespaced_pod: %s\n" % z)

    for podstatus in retprima.items:
      if podstatus.spec.node_name == nodeworker and podstatus.status.phase == "Running" and podstatus.status.container_statuses[0].ready:
        salida = True        
      else:
        salida = False

      if salida:
        print(" ok", flush=True)
        break
      elif not salida and retrycount < 9:
        print(" .", end='',flush=True)
        time.sleep(5)
        retrycount += 1
      else:
        print(" error", flush=True)
        salida  = True
        break

    if salida:
      break