#!/usr/bin/env python

import logging
import os
import pykube
import random
import time

KILL_FREQUENCY = int(os.environ.get('CHAOS_MONKEY_KILL_FREQUENCY_SECONDS', 300))
LOGGER = logging.getLogger(__name__)

# No error handling, if things go wrong Kubernetes will restart for us!

api = pykube.HTTPClient(pykube.KubeConfig.from_service_account())

while True:
    namespaces = pykube.Namespace.objects(api)

    pods = []
    for namespace in namespaces:
        pods.extend(list(pykube.Pod.objects(api).filter(namespace=namespace.name)))
    pod = random.choice(pods)
    LOGGER.info("Terminating pod %s/%s", pod.namespace, pod.name)
    pod.delete()

    time.sleep(KILL_FREQUENCY)
