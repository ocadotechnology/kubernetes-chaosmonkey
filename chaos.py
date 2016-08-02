#!/usr/bin/env python

import logging
import os
import pykube
import time

KILL_FREQUENCY = os.environ.get('CHAOS_MONKEY_KILL_FREQUENCY_SECONDS', 300)
LOGGER = logging.getLogger(__name__)

# No error handling, if things go wrong Kubernetes will restart for us!

api = pykube.HTTPClient(pykube.KubeConfig.from_service_account())

while True:
    pods = pykube.Pod.objects(api)
    print(str(pods))
    print(str(list(pods)))

    time.sleep(KILL_FREQUENCY)
