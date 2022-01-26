# LoRaWAN-Roaming-Tutorial

This tutorial aims at giving a quckstart tutorial for setting up a roaming platform for LoRaWAN End-Devices.

## General architecture

Contrary to the [LoRaWAN Backend Interfaces], our roaming approach makes it posible to have roaming without the need of provisioning JoinEUI/AppEUI identifiers on each End-Device. 
For that, we rely on Private DNS resolutions using DoH (DNS over HTTPS) with mutual authentication. 
Therefore, we introduce a new network element, a DNS Broker that: 

- will be set up per business federation.
- is in chare of delivering client certificates.
- will manage Private DNS Zones : 
  - CNAME:  ``` domain: [DevEUI:EUI-64].deveui.iot-roam.net ``` , ``` target: NetID.netid.iot-roam.net ``` 
  - A:      ``` domain: [NetID:EUI-64].netid.iot-roam.net ``` ,  ``` IP: 	X.X.X.X ``` 
- will authenticate LNS and will meke private DNS resolutions.

A tutorial on how to set up an open-source DNS Broker can be accessed here: [Private DNS Broker]

Figure 1 depicts the general flowshart of a join procedure of an End-Device when roaming:

<p align="center">
  <img width="800" height="350" src="https://github.com/MarinoMtz/LoRaWAN-Roaming-Tutorial/blob/main/images/echange.svg">
</p>

The join procedure works as follows:

- The ED sends a **Join-request** message. Then, RG forwards the JR to its NS (the fNS) [steps 1-2].
- The fNS determines whether there is a roaming agreement with the Network to which the ED belongs by doing a DNS query carrying the DevEUI to get the hNS/sNS NetID and IP Address. 
  - If not known alerady, the fNS makes a DNS Lookup to get the IP of the Broker [steps 3-4]
  - The fNS makes a DoH Lookup to get the hNS IP. For this it needs a client-certificate delivered by the Broker [steps 5-6]
- The fNS, sends a **PRStartReq** message carrying the **Join-request** message [step 7].
- Then, hNS/sNS forwards the **JoinReq** message to its JS [steps 8].
- The JS replies with a **JoinAns** message carrying the **Join-accept** [step 9]. 
- The sNS/hNS sends a **PRStartAns** message to the fNS carrying the **Join-accept** [step 10]. 
- The fNS finally sends a **Join-accept** to the ED [steps 11-12].

Note that, contrary to Backend interfaces, no DNS resolution is made with the JoinEUI.

## Software requirements 

- Chirpstack Application Server
- Chirpstack Network Server with DevEUI DNS resolution capabilities
- DNS Client with client authentication

## Chirpstack Network Server

In order to make it possible to have DevEUI-based roaming we have modified the source-code of the Chirpstack Network Server, it is available here [CLNS]. 
The AS and NS shoud be installed ins the same manner as the original chirpstack.
In addition to the regular parameters in the config file (```chirpstack-network-server.toml```), we shold add the folloing parameters:
An example of this configuration file is included in this repository.

```
# Network-server settings.
[network_server]
# Network identifier (NetID, 3 bytes) encoded as HEX (e.g. 010203)
net_id="XXXXXX"

...

# Roaming settings (experimental).
[roaming]
# Resolve NetID domain suffix.
#
# This configures the domain suffix used for resolving a Network Server
# using its NetID.
resolve_netid_domain_suffix=".netid.iot-roam.net." 
resolve_deveui_domain_suffix=".deveui.iot-roam.net."
roaming_deveui=true

  [roaming.api]
  # Interface to bind the API to (ip:port).
  bind="0.0.0.0:XXXX"

  # CA certificate (optional).
  #
  # When configured, this is used for client-certificate validation.
  ca_cert="/../../intermediate-remote.pem"
  tls_cert="/../../server-combined.pem"
  tls_key="/../../server-key.pem"


  # Per roaming-agreement server configuration.
  #
  # Example:
  #[[roaming.servers]]
  passive_roaming_lifetime="0s"
  
  net_id="XXXXXX"
  async=true
  async_timeout="5s"
  passive_roaming=true
  passive_roaming_lifetime="0s"
  passive_roaming_kek_label=""
  server="https://XXXXX.netid.iot-roam.net:8005" # Could be any server. It depends on the roaming agreement
  port="XXXX"
  ca_cert="/../../intermediate.pem"
  tls_cert="/../../client/client-combined.pem"
  tls_key="/../../client-key.pem"

```

###  Fields to be configured: 

 - [network_server]: 
   - ``` net_id```: this corresponds to the 3-byte identifier delivered by the LoRa Alliance

 - [roaming]:
    - ``` resolve_netid_domain_suffix``` : an authoritative DNS server at ``` ".netid.iot-roam.net." ```  (The DNS Client will direct it to the Broker)
    - ``` resolve_deveui_domain_suffix``` : an authoritative DNS server at ``` ".deveui.iot-roam.net."```  (The DNS Client will direct it to the Broker)
    - ``` roaming_deveui=true ``` 
 - [roaming.api] : the roaming api server configuration
    - ```ca_cert```, ```tls_cert```, ```tls_key``` : used to authenticate other LNS
 - [[roaming.servers]]: configuration per roaming agreement (in this case the LNS acts as fNS)
    - ```net_id="XXXXXX"``` : 3-byte identifier of the hNS 
    - ``` async=true```, ```async_timeout="5s"```, ``` passive_roaming=true ``` : passive roaming agreement config
    - ``` server="https://XXXXX.netid.iot-roam.net" ```, ```port="XXXX"```:  URL and port of the fNS
    - ``` ca_cert, tls_cer, tls_key" ```: client-side TLS configuration (provided by the hNS)
 
 ###  To run the LNS:
 
 The source code can be either compiled by following this tutorial: [ChripstackSource], or you can use the pre-compiled binary provided in this repository.
 Then, to run it:
 
 ``` /home/../chirpstack-network-server -c/../chirpstack-network-server-deveui.toml ```
 

## DNS Client

This architecture requires to have DNS over HTTPS resolutions using client/server certificates for mutual authentication. 
For this PoC, client-certificates to be used at the LNS side will be provided by the DNS Broker.
The DoH client to be used is a modified version on dnsproxy, available at [dnsproxy].

To run the client, we shall have a ```.yaml``` configuration file including the following parameters:
```
---
upstream:
  - '1.1.1.1:53'
  - '[/iot-roam.net/]https://broker.iot-roam.net/dns-query'
bootstrap:
  - '8.8.8.8:53'
cache-size: 64000
ratelimit: 0
ipv6-disabled: false
udp-buf-size: 0
max-go-routines: 0
version: false
tls-client-crt: '/path/file'
tls-client-key: '/path/file'
```

This configuration allow us to define two DNS Upstreams, the fisrt one: ```'1.1.1.1:53'``` will be used by the host to make most of DNS Request, and the second will use ```https://broker.iot-roam.net/dns-query``` only for requests having ```.iot-roam.net``` as domain suffix.

Then, we also pass through the configuration file, the information requered for DoH Upstream Authentication: ```tls-client-crt``` and ```tls-client-key```.
To run the DNS Client, we use: 

``` sudo ./dnsproxy --config-path=config.yaml ```

[LoRaWAN Backend Interfaces]: https://lora-alliance.org/resource_hub/ts002-110-lorawan-backend-interfaces/
[CLNS]: https://github.com/MarinoMtz/chirpstack-network-server
[dnsproxy]: https://github.com/MarinoMtz/dnsproxy/tree/clienauthyaml
[ChripstackSource]: https://www.chirpstack.io/application-server/community/source/
[Private DNS Broker]: https://github.com/MarinoMtz/dnsresolver
