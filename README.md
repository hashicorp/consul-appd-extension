# HashiCorp Consul Monitoring Extension
An AppDynamics Machine Agent add-on to report metrics from HashiCorp Consul to AppDynamics CNS.

## Installation

 1. Download the AppDynamics [machine agent], unzip, and configure it for [standalone mode] in `/opt/appd`.
 2. Clone this repo and copy contents of folder `statsite` into `/opt/appd/machine/monitors/StatSite`.
 
        mkdir -p /opt/appd/machine/monitors/StatSite
        git clone https://github.com/hashicorp/consul-appd-extension.git
        cp ./consul-appd-extension/statsite/* /opt/appd/machine/monitors/StatSite

 3. Start the machine agent. It is recommended to increase the value of `maxMetrics` so that data doesn't get truncated.
 
        java -Xmx64m -Dappdynamics.agent.maxMetrics=10000 -jar /opt/appd/machine/machineagent.jar
 
 4. Configure Consul agent with a [telemetry stanza] in `statsite.json` for Consul to send metrics to statsite.

        cp ./statsite.json /etc/consul.d/

 5. Restart Consul agent. 

## Finding metrics

All metrics reported by this extension will be found in the Metric Browser under `Application Infrastructure Performance|Tier1|Custom Metrics|statsd|consul`. For details of what each metric means, consult the [Consul Telemetry] guide.

## Custom dashboards

This repository provides custom dashboards to get you started on monitoring Consul in the `dashboards` folder. To import dasboards:

 1. Log into your AppDynamics controller. Select the **Dashboards & Reports** tab > **Dashboards** > **Import**.
 2. Upload the  `.json` dashboard file.
  

[machine agent]: https://download.appdynamics.com/download/#version=&apm=machine&os=&platform_admin_os=&appdynamics_cluster_os=&events=&eum=&page=1
[standalone mode]: https://docs.appdynamics.com/display/PRO45/Configure+the+Standalone+Machine+Agent
[telemetry stanza]: https://www.consul.io/docs/agent/options.html#telemetry
[statsite binary]: https://github.com/statsite/statsite/blob/master/INSTALL.md
[consul telemetry]: https://www.consul.io/docs/agent/telemetry.html

