# LoRaWAN-Roaming-Tutorial

This tutorial aims at giving a quckstart tutorial for setting up a roaming platform for LoRaWAN devices.

## General architecture

Contrary to the [LoRaWAN Backend Interfaces], our roaming approach makes it posible to have roaming wothout the need of provisioning JoinEUI/AppEUI identifiers on each End-Device. For that, we rely on Private DNS resolutions using DoH with mutual authentication. Therefore, we introduce a new network element, a DNS Broker that: 

- will be set up per business federation.
- is in chare of delivering client certificates.
- will manage Private DNS Zones : 
  - CNAME:  ``` domain: [DevEUI:EUI-64].deveui.iot-roam.net ``` , ``` target: NetID.netid.iot-roam.net ``` 
  - A:      ``` domain: [NetID:EUI-64].netid.iot-roam.net ``` ,  ``` IP: 	X.X.X.X ``` 
- will authenticate LNS and will meke private DNS resolutions

Figure 1 depicts the general flowshart of a join procedure of an End-Device when roaming:

<p align="center">
  <img width="800" height="350" src="https://github.com/MarinoMtz/LoRaWAN-Roaming-Tutorial/blob/main/images/echange.svg">
</p>

## Software requirements 


## Chirpstack Network Server

## DNS Client


[LoRaWAN Backend Interfaces]: https://lora-alliance.org/resource_hub/ts002-110-lorawan-backend-interfaces/
