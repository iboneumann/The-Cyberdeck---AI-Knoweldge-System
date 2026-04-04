+++
date = '2026-04-04T18:59:17+02:00'
draft = false
title = 'Cyberdeck Architecture Design Core'
weight = 36
+++

This Cyberdeck AI Knowlege System can be taken as an architecture principle, like Object  
Oriented Programming changing programming, shifting computer set ups into fully integrated  
computer networking.  
  
Linux operating systems make hardware longer usable, Beowulf Cluster technology the hardware  
more effective for even non-dedicated parallel software. FFMPEG used to turn music projects  
into mp3 uses as on an OS library level the MPICH libraries of that very Beowulf Cluster  
Architecture and there is a great change that more OS level libraries will be added.   
Python allready offers some.   
  
The pure idea is so Open Source, it will happen...  
  
I allready can have two system resource heavy software packages run using the two screens and  
the Laptop monitor having with Barrier a standard tool to move mouse and keyboard across the  
three screens as if it was one Computer.  
With Midnight Commander I have a file browser at hand that manges file copy as if it was again  
one Computer I work on.  
  
This means I have a few hundred bugs of hardware usable as a thousand bugs by being an OG Hacker  
with plenty of time. Overall, that math might add up and even financialy strong organisations,  
which can provit from the efficiency gain using this project as an Architecture Principle.  
There is a great chance that offices in need of strong hardware per desk and worker can profit  
even more from an integrated set up such as this tool as Architecture.  
  
The actual trick of managing the bespoke LAN, which essentially the Cybderdeck Knowledge AI is,  
is having a capable IT System Manager with Linux, Python and sever architecture understanding.  
The knowledge and experiance comes by using a large online AI heavily never minding asking like  
I do with DeepSeek.  
  
The most important file to start in any Linux running Office a Cyberdeck Architecture Project is  
the /etc/hosts file that lists the Beowulf Cluster nodes like this:  
[...]  
192.168.178.42  node1 raspi5  
192.168.178.36  node2 420  
192.168.178.31  node3 raspi4  
192.168.178.33  node4 920  
192.168.178.26  node5 X260  
192.168.178.29  node6 fujitsu64gb  
192.168.178.40  node7 16gbraspi  
  
The Beowulf Cluster has a common user on each of these nodes named mpiuser.  
The headnode is on that user connected with private keys to all other nodes. Those enable logging  
on without any password use. The layer is used to transport the CPU loads for sharing between the  
head node and the other nodes.   
Obviously, these ssh keys can be used to enable each node to access each other node with out any  
password.  
That also means that every script or any AI Ghost can use that layer to perform OS tasks between  
the office computers.  
  
The Load Balancer I created using DeepSeek as the Coder is exactly doing this. In Linux user rights,  
the ability of access rights can be very detailed given to each user. Root is the most powerful and  
the system as long as the password is not shared, save, because working user is not Root or mpisuer.  
  
Cracking Linux is hard.  
  
Creating a Diamond ICE layer into that design makes it impossibel to enter the system from outside,  
but it also demands maintenance of allowed connections. Every analytics script that needs to send  
commands across the network into any node of the Cluster can use the mpisuer level to do that.  
Then it needs one user with one password over all computers, while the workers use their own user  
access within they can limit certain folder access to this their own user and share others.  
  
Every dashboard of LibreOffice or OpenOffice actioned by a script to pull data from another computer  
can use that mpiuser being distributed over that user form one node.  
Every file operation triggered by any tailored Linux GUI Desktop Icon can use that layer of users  
to push data forward and around.  
  
Of course as a background process.  
  
The script to check on my Diamond ICE security layer will do that as much as every Ghost AI  
I will add to this system and project.  
  
/etc/hosts  
IP nodeNr name  
  


