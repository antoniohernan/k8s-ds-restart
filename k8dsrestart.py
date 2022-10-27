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

def retrievepods():
  config.load_kube_config()
  v1 = client.CoreV1Api()
  try:
    return v1.list_namespaced_pod(args.namespace,pretty=pretty)
  except ApiException as x:
    print("Exception when calling CoreV1Api->list_namespaced_pod: %s\n" % x)
    
def deletepod(podname, namespacename, drymode ):
  config.load_kube_config()
  v1   = client.CoreV1Api()
  body = client.V1DeleteOptions()
  try:
    if not drymode:
      v1.delete_namespaced_pod(podname, namespacename, body=body, propagation_policy="Background", grace_period_seconds=0)
      time.sleep(10)
    else:
      print(" -- will be deleted -- (dry run mode) ", end='', flush=True)
  except ApiException as x:
    print("Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % x)

def printpods(poditems):
  print ("\n\n Pods running in DaemonSet: %s deployed in the NameSpace: %s\n" % (args.namespace, args.daemonset))
  print("%s\t%s\t%s\t\t%s" % ('Pod Name','Run Node','Status','Container Ready'))
  for i in poditems.items:
    print("%s\t%s\t%s\t\t%s" % (i.metadata.name, i.spec.node_name, i.status.phase, i.status.container_statuses[0].ready))  

initpods = retrievepods()
lpods = []
for i in initpods.items:
    lpods.append(i.spec.node_name+";"+i.metadata.name)

printpods(initpods)

for i in lpods:
  element    = i.split(";")
  nodeworker = element[0]
  podname    = element[1]
  salida     = False
  print ("\n Restarting pod: %s in node: %s " % (podname, nodeworker), end='', flush=True)
  deletepod(podname, args.namespace, args.dryrun)  
  retrycount = 0
  
  while True:
    newpods = retrievepods()
    salida = False
    for podstatus in newpods.items:
      for condition in podstatus.status.conditions:
        if not args.dryrun: 
          if podstatus.spec.node_name == nodeworker and podstatus.metadata.name != podname and condition.type == "Ready" and condition.status == 'True':
            salida = True
            break
        else:
          if podstatus.spec.node_name == nodeworker and condition.type == "Ready" and condition.status == 'True':
            salida = True
            break
      if salida:
        break        

    if salida:
      print(" ok", flush=True)
      break
    elif not salida and retrycount < 9:
      print(" .", end='',flush=True)
      time.sleep(5)
      retrycount += 1
    else:
      print(" error retries exceeded", flush=True)
      break

printpods(retrievepods())