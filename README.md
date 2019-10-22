# HashiCorp Consul Monitoring Extension for AppDynamics CNS
An AppDynamics Machine Agent add-on to report metrics from HashiCorp Consul to AppDynamics Central Nervous System (CNS).

## System Requirements
Please visit AppDynamics Machine Agent [requirements and supported environments] for more info.

## Installation

 1. Download the AppDynamics [machine agent bundle]. As `root` or super user, unzip and configure it for [standalone mode] in `/opt/appdynamics`. See this [guide]. You will need to obtain your AppDynamics Controller access information and configure it in `controller-info.xml` file:

        sudo su
        mkdir -p /opt/appdynamics
        zip ./machineagent-bundle-64bit-linux-4.5.15.2316.zip -d /opt/appdynamics
        cp /opt/appdynamics/etc/systemd/system/appdynamics-machine-agent.service /etc/systemd/system/appdynamics-machine-agent.service
        cp -f ./controller-info.xml /opt/appdynamics/conf

 2. It is recommended to increase the value of `maxMetrics` so that data doesn't get truncated. Add Java Options in AppDynamics agent service definition to increase the value of `maxMetrics`.
 
         sed -i 's/#Environment="JAVA_OPTS=-D<sys-property1>=<value1> -D<sys-property2>=<value2>"/Environment="JAVA_OPTS=-Dappdynamics.agent.maxMetrics=10000"/g' /etc/systemd/system/appdynamics-machine-agent.service
 
 3. Clone this [repo] and copy contents of folder `statsite` into `/opt/appdynamics/monitors/StatSite`:
 
        mkdir -p /opt/appdynamics/monitors/StatSite
        git clone https://github.com/hashicorp/consul-appd-extension.git
        cp ./consul-appd-extension/statsite/* /opt/appdynamics/monitors/StatSite

 4. Clone, compile the [statsite repo], and copy the `statsite` executable into `/opt/appdynamics/monitors/StatSite`. Follow the installation steps highlighted [here]:
 
        cd ~ && git clone https://github.com/hashicorp/consul-appd-extension.git
        cd statsite
        apt-get update
        apt-get -y install build-essential libtool autoconf automake scons python-setuptools lsof git texlive check
        easy_install pip
        pip install pytest==3.4.0 
        pip install requests==2.21.0
        ./autogen.sh
        ./configure
        make
        make install
        cp statsite /opt/appdynamics/monitors/StatSite

 5. Configure Consul agent with a [telemetry stanza] in `statsite.json` for Consul to send metrics to statsite:

        cp ./consul-appd-extension/statsite.json /etc/consul.d/

 6. Restart Consul agent:

        systemctl restart consul

 7. Start the machine agent:
 
        systemctl start appdynamics-machine-agent

 8. Verify both AppDynamics and Consul service status:
       
        systemctl status appdynamics-machine-agent
        systemctl status consul

 9. Verify AppDynamics Machine Agent logs:
       
        tail -f /opt/appdynamics/logs/machine-agent.log

 10. (Optional) Enable [server visibility]:
       
       ```
       systemctl stop appdynamics-machine-agent
       sed -i 's/Environment="JAVA_OPTS=-Dappdynamics.agent.maxMetrics=10000"/Environment="JAVA_OPTS=-Dappdynamics.agent.maxMetrics=10000 -Dappdynamics.sim.enabled=true"/g' /etc/systemd/system/appdynamics-machine-agent.service
       systemctl daemon-reload
       systemctl start appdynamics-machine-agent
       systemctl status appdynamics-machine-agent
       ```


## Troubleshooting
Please visit AppDynamics [knowledge base] for troubleshooting articles or contact AppDynamics [support] for help.

## Finding metrics
All metrics reported by this extension will be found in the Metric Browser under `Application Infrastructure Performance|Tier1|Custom Metrics|statsd|consul`. For details of what each metric means, consult the [Consul Telemetry] guide.

## Custom dashboards
This repository provides custom dashboards to get you started on monitoring Consul in the `dashboards` folder. To import dasboards:

 1. Log into your AppDynamics controller. Select the **Dashboards & Reports** tab > **Dashboards** > **Import**.
 2. Upload the  `.json` dashboard file.
  

[requirements and supported environments]: https://docs.appdynamics.com/display/PRO45/Standalone+Machine+Agent+Requirements+and+Supported+Environments
[machine agent bundle]: https://download.appdynamics.com/download/#version=&apm=machine&os=&platform_admin_os=&appdynamics_cluster_os=&events=&eum=&page=1
[guide]: https://docs.appdynamics.com/display/PRO45/Linux+Install+Using+ZIP+with+Bundled+JRE
[repo]: https://github.com/hashicorp/consul-appd-extension
[standalone mode]: https://docs.appdynamics.com/display/PRO45/Configure+the+Standalone+Machine+Agent
[telemetry stanza]: https://www.consul.io/docs/agent/options.html#telemetry
[server visibility]: https://docs.appdynamics.com/display/PRO45/Enable+Server+Visibility
[consul telemetry]: https://www.consul.io/docs/agent/telemetry.html
[statsite repo]: https://github.com/statsite/statsite
[here]: https://github.com/statsite/statsite/blob/master/INSTALL.md
[knowledge base]: https://community.appdynamics.com/t5/Knowledge-Base/tkb-p/knowledge-base
[support]: https://www.appdynamics.com/support/

