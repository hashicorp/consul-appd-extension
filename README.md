# HashiCorp Consul Monitoring Extension for AppDynamics CNS
HashiCorp has built an AppDynamics Machine Agent extension to report metrics from HashiCorp Consul into the AppDynamics platform via the metrics browser. The Consul metrics can then be used to create dashboards and health rules, where they can be visualized, baselined and alerted on within AppDynamics.

## System Requirements
- An AppDynamics SaaS or On-Prem controller version 4.5 or greater. 
- AppDynamics [Machine or Server Visibility] agent including the JRE. 
- Please visit AppDynamics Machine Agent [requirements and supported environments] for more info.
- A Consul cluster that we will install the AppDynamics Machine Agent and extension on (each node) to report metrics. 
- Applications that are using Consul to register and discover services that are also being monitored by AppDynamics using one a [language agent] as well as a [machine or server visibility agent].
- Statsite (which is a metrics aggregator like statsd) will be required to be installed on each node of the Consul cluster which will be covered in the instructions below. 

## Installation

 1. Download the AppDynamics [machine agent bundle]. As `root` or super user, unzip and configure it for [standalone mode] in `/opt/appdynamics/machine-agent`. See this [guide] to configure it. You will need to obtain your AppDynamics Controller access information and configure it in `controller-info.xml` file before you begin the steps below.

        sudo su
        mkdir -p /opt/appdynamics/machine-agent
        unzip ./machineagent-bundle-64bit-linux-4.5.15.2316.zip -d /opt/appdynamics/machine-agent
        cp /opt/appdynamics/machine-agent/etc/systemd/system/appdynamics-machine-agent.service /etc/systemd/system/appdynamics-machine-agent.service
        cd /opt/appdynamics/machine-agent/conf
        vi controller-info.xml

       > **NOTE:** This requires editing the controller file `controller-info.xml`.

 2. It is highly recommended to increase the value of `maxMetrics` so that data doesn't get truncated. Add Java Options in AppDynamics agent service definition to increase the value of `maxMetrics`.
 
         sed -i 's/#Environment="JAVA_OPTS=-D<sys-property1>=<value1> -D<sys-property2>=<value2>"/Environment="JAVA_OPTS=-Dappdynamics.agent.maxMetrics=10000"/g' /etc/systemd/system/appdynamics-machine-agent.service
 
 3. To install this extension, clone this [consul-appd-extension repo] and copy contents of folder `statsite` into `/opt/appdynamics/machine-agent/monitors/StatSite`:
 
        mkdir -p /opt/appdynamics/machine-agent/monitors/StatSite
        git clone https://github.com/hashicorp/consul-appd-extension.git
        cp ./consul-appd-extension/statsite/* /opt/appdynamics/machine-agent/monitors/StatSite

 4. Now you need to compile the [statsite], and copy the `statsite` executable into `/opt/appdynamics/machine-agent/monitors/StatSite`. Follow the installation steps highlighted [here]:
       
       > For linux Debian based OS:
 
        cd ~ && wget https://github.com/statsite/statsite/archive/v0.8.0.zip
        unzip v0.8.0.zip && cd statsite-0.8.0
        apt-get update
        apt-get -y install build-essential libtool autoconf automake scons python-setuptools lsof git texlive check
        ./bootstrap.sh
        ./configure
        make
        cp ./src/statsite /opt/appdynamics/machine-agent/monitors/StatSite

       > For linux Redhat based OS:
 
        cd ~ && wget https://github.com/statsite/statsite/archive/v0.8.0.zip
        unzip v0.8.0.zip && cd statsite-0.8.0
        yum update
        yum groupinstall -y 'Development Tools'
        yum install -y install libtool autoconf automake scons python-setuptools lsof git texlive check
        ./bootstrap.sh
        ./configure
        make
        cp ./src/statsite /opt/appdynamics/machine-agent/monitors/StatSite

 5. Configure Consul agent with a [telemetry stanza] in `consul-statsite.json` for Consul to send metrics to statsite:

        cp ~/consul-appd-extension/consul-statsite.json /etc/consul.d/

 6. Restart Consul agent:

        systemctl restart consul

 7. Start the AppDynamics machine agent:
 
        systemctl start appdynamics-machine-agent

 8. Verify both AppDynamics and Consul service status:
       
        systemctl status appdynamics-machine-agent
        systemctl status consul

 9. Verify AppDynamics Machine Agent started properly by looking at the Agent logs:
       
        tail -f /opt/appdynamics/machine-agent/logs/machine-agent.log

 10. (Optional) You can enable [server visibility] on the machine agent which requires the appropriate AppDynamics license, but is supported by this integration. Edit `controller-info.xml` and set the flag to `true` to enable it, `<sim-enabled>true</sim-enabled>`:
       
       ```
       systemctl stop appdynamics-machine-agent
       vi /opt/appdynamics/machine-agent/controller-info.xml
       systemctl start appdynamics-machine-agent
       systemctl status consul
       ```
       > **NOTE:** This requires editing the controller file `controller-info.xml`.

## Troubleshooting
Please visit AppDynamics [knowledge base] for troubleshooting articles or contact [AppDynamics support] for help with your AppDynamics environment. Contact [HashiCorp support] for help with the machine agent extension.

## Finding metrics
All metrics reported by this extension will be found in the Metric Browser (Controller > Applications > Application > Metric Browser) under `Application Infrastructure Performance|Consul|Custom Metrics|statsd|consul` or `Application Infrastructure Performance|Consul|Custom Metrics|statsd|envoy`. For details of what each metric means, consult the [Consul Telemetry] guide.

## Custom dashboards
This repository provides two custom dashboards to get you started on monitoring Consul in the `dashboards` folder. They are located in the [dashboards] folder. To import the dasboards:

 1. Log into your AppDynamics controller. Select the **Dashboards & Reports** tab > **Dashboards** > **Import**.
 2. Upload the  `.json` dashboard file.

Note: You will need to change the value for the key `applicationName` within the templates to macth your application name.

## Custom Health Rules
AppDynamics CNS provides the ability to customize health rules, the policy statements that define triggers. Today health rules for Consul are created against the applications that are using its service discovery and service mesh so that the metrics for the application as well as Consul can be seen against particular applications in AppDynamics. Visit this [health rule guide] for more info.




[requirements and supported environments]: https://docs.appdynamics.com/display/PRO45/Standalone+Machine+Agent+Requirements+and+Supported+Environments
[Machine or Server Visibility]: https://docs.appdynamics.com/display/PRO45/Infrastructure+Visibility
[language agent]: https://docs.appdynamics.com/display/PRO45/Install+App+Server+Agents
[machine or server visibility agent]: https://docs.appdynamics.com/display/PRO45/Infrastructure+Visibility
[machine agent bundle]: https://download.appdynamics.com/download/#version=&apm=machine&os=&platform_admin_os=&appdynamics_cluster_os=&events=&eum=&page=1
[guide]: https://docs.appdynamics.com/display/PRO45/Linux+Install+Using+ZIP+with+Bundled+JRE
[consul-appd-extension repo]: https://github.com/hashicorp/consul-appd-extension
[standalone mode]: https://docs.appdynamics.com/display/PRO45/Configure+the+Standalone+Machine+Agent
[telemetry stanza]: https://www.consul.io/docs/agent/options.html#telemetry
[server visibility]: https://docs.appdynamics.com/display/PRO45/Enable+Server+Visibility
[consul telemetry]: https://www.consul.io/docs/agent/telemetry.html
[statsite]: https://github.com/statsite/statsite
[here]: https://github.com/statsite/statsite/blob/master/INSTALL.md
[knowledge base]: https://community.appdynamics.com/t5/Knowledge-Base/tkb-p/knowledge-base
[AppDynamics support]: https://www.appdynamics.com/support/
[HashiCorp support]: https://support.hashicorp.com/hc/en-us
[dashboards]: https://github.com/hashicorp/consul-appd-extension/tree/master/dashboards
[health rule guide]: https://docs.appdynamics.com/display/PRO45/Health+Rules

