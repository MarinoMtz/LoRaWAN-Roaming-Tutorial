Welcome to the DiNS roaming with DNS page

This tutorial will help you to allow roaming between LoRaWAN network. Three actors are involved:

* Device Owner or DO: You have devices and you want them to connect to some LoRaWAN networks. You need to install a regular LNS to register your devices and find a Broker to synchronize your local configuration.
* Network Operator or NO: You run a LoraWAN network and you want to allow devices registered on a broker to access to your network. You will need a special version of the chripstack LNS to handle roaming.


DiNS is playing the role of a broker. Of course it is also possible to play this role.

Device Owner
===========


As a DO you must run a LNS to register your devices. This LNS will be queried by the NO where your device is joining. There is no modification you just need to run a DNS on a specific zone and excuse periodically some scripts to fill the DNS with information located in the LNS. 

Step 1
---------

* Install chirpstack 
* register your objets.

Step 2
---------

Delegate a DNS zone for your devices 

For bind9, the configuration file looks like that:

```
   >cat named.conf.local
   zone "mydevices.plido.net" {
 	type master;
 	file "mydevices.db";
	allow-transfer {51.91.121.182;};
	notify no;
   };
```

Where my devices.plido.net is the zone. Information regarding the devices will be store in the my devices.db on /var/cache/bind.

Note that Allow-transfert winch contains the IP address provided by the broker to synchronize the zone with the broker.

To create the file mydevices.db, a python script ``` getdb.py``` is provided. Before launching it you need to modify the
following values in line 4: ```host```, ```database```, ```user```, ```password```.

Step 3
------

Setup private DNS with correct certificates

Network Operator
================


