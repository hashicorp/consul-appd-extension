#!/usr/bin/env python
import sys

for line in sys.stdin:  # type: str
    line = line.strip()
    if not line:
        continue
    elif line.startswith('#'):
        continue
    else:
        key, value, timestamp = line.split('|')

        words = key.split('.')
        metric_type = words.pop(0)
        name = '|'.join(words)

        agg = 'OBSERVATION'
        time_roll = 'CURRENT'
        cluster_roll = 'COLLECTIVE'

        if metric_type == 'timers':
            agg = 'AVERAGE'
            time_roll = 'AVERAGE'
            cluster_roll = 'INDIVIDUAL'

        value = int(float(value))
        if abs(value) > (2 ** 63 - 1):
            continue
            
        print 'name=Custom Metrics|statsd|{0},value={1},aggregator={2},time-rollup={3},cluster-rollup={4}'.format(name, value, agg, time_roll, cluster_roll)
