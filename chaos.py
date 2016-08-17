#!/usr/bin/env python

import logging
import os
import pykube
import random
import time

KILL_FREQUENCY = int(os.environ.get('CHAOS_MONKEY_KILL_FREQUENCY_SECONDS', 300))
LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

# No error handling, if things go wrong Kubernetes will restart for us!

api = pykube.HTTPClient(pykube.KubeConfig.from_service_account())

while True:
    pods = list(pykube.Pod.objects(api).filter(namespace=''))
    pod = random.choice(pods)
    container_name = random.choice(pod.obj['spec']['containers'])['name']
    LOGGER.info("Terminating pod %s/%s/%s", pod.namespace, pod.name, container_name)
    #pod.delete()

    time.sleep(KILL_FREQUENCY)
