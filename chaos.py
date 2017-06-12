#!/usr/bin/env python

import logging
import kubernetes
import os
import random
import time
import socket
import json

from kubernetes.client.rest import ApiException
from http import HTTPStatus


KILL_FREQUENCY = int(os.environ.get('CHAOS_MONKEY_KILL_FREQUENCY_SECONDS', 300))
LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

# No error handling, if things go wrong Kubernetes will restart for us!

kubernetes.config.load_incluster_config()
v1 = kubernetes.client.CoreV1Api()

while True:
    pods = v1.list_pod_for_all_namespaces().items
    pod = random.choice(pods)
    LOGGER.info("Terminating pod %s/%s", pod.metadata.namespace, pod.metadata.name)
    event_name = "Chaos monkey kill pod %s" % pod.metadata.name
    v1.delete_namespaced_pod(
        name=pod.metadata.name,
        namespace=pod.metadata.namespace,
        body=kubernetes.client.V1DeleteOptions(),
    )

    try:
        event = v1.read_namespaced_event(event_name, namespace=pod.metadata.namespace)
        event.count += 1
        v1.replace_namespaced_event(event_name, pod.metadata.namespace, event)
    except ApiException as e:
        error_data = json.loads(e.body)
        error_code = HTTPStatus(int(error_data['code']))
        if error_code == HTTPStatus.NOT_FOUND:
            event = kubernetes.client.V1Event(
                metadata=kubernetes.client.V1ObjectMeta(
                    name=event_name,
                ),
                source=socket.gethostname(),
                involved_object=kubernetes.client.V1ObjectReference(
                    kind="Pod",
                    name=pod.metadata.name,
                    namespace=pod.metadata.namespace,
                    uid=pod.metadata.uid,
                ),
                message="Pod deleted by chaos monkey",
                type="Warning",
            )
            print(event)
            v1.create_namespaced_event(namespace=pod.metadata.namespace, body=event)
    time.sleep(KILL_FREQUENCY)
