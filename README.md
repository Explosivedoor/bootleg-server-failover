# Bootleg Server Failover
A guide for a bootleg server failover for those of us too cheap to pay like, $5 a month.
My use case for this is because I too don't want to pay $5 a month, and to have a server closer to those who access it. My main server is in Japan, my backup in the US. 

Let's start with the things you will need for this: 
1. Your (home) sever. Could be an old laptop or a 4u you bought because you thought that was a good idea to have in a 1 bedroom apartment. Mine is running Ubuntu. 
2. A second server that is offsite (ie. not in your 1 bedroom apartment) usually one with good uptime and terminal access. I use namecheap.com shared hosting for this. 
3. Cloudflare account
4. (optional) Telegram to get notification when your server goes down.
5. (optional) Rasberry Pi/Le Potato/Orange Pi/whatever 

# Home Side Setup
1. Install a Linux OS of your choice on your home server.
2. Install a webserver of your choice. I use Virtualmin (https://www.virtualmin.com/download/) it is basically a free cpanel. But you can go with a simple Apache install.
3. Throw your website on the server.
4. Open port 80 and 422 on your router to allow web traffic to the server from the outside world. This might be labeled at "port forwarding" or "IP Masquerading". You will fill in the internal ip of your server here. You might also want to setup a DMZ to "quarantine" those ports and your server from your wider network.
5. (optional) If you have multiple servers, or want to test out having multiple servers in your home (for things like load balancing) you should install a lightweight OS to your Rasberry Pi/Le Potato/Orange Pi/whatever (I use Debian for my Le Potato) and have your router point to the mini pc instead of your sever directly. This will allow you to setup things like haproxy to act as a load balancer. I personally have docker installed (which is probably its own tutorial) with haproxy running in a container. You can see my config file here: TODO. It isn't the best config file in the world but I am too lazy currently to fix it. 
6. Setup your domain with cloudflare. In the A record put in your current IP address (don't worry if you have a dynamic IP, we will cover that in a second). Make sure proxy is ON. This will hide your real ip from the internet.
7. On your home server download the following file: https://github.com/K0p1-Git/cloudflare-ddns-updater and make sure to fill it out correctly (use nano). What this does, is it update the ip address of the A record if it changes from what was there previously. Allowing you, with your dynamic IP, to not have to worry about it changing. This will also help with server failover.
8. After you fill in the information you must add it to your crontab TODO:code. Set it for whatever length of time you want, usually 5min is fast enough but you can go with 1min.
9. Check now and see if you can access your website. Try and change the A record manually via the cloudflare dashboard and make sure it switches back in the time that you set. If it didn't, you probably missed something.
10. Set up a url on your Home server that is ONLY on your home server. I have mine set up to be on example.com/checkstatus. This url will be used by the off-site server to check on the homeserver to see if its alive. You can also make it a subdomain like checkstatus.example.com.
11. (optional) Instead of the above you can use HAProxy on a Single board computer to create a monitor uri (https://www.haproxy.com/documentation/haproxy-configuration-tutorials/alerts-and-monitoring/monitor-uri/). 
    
# Off-Site Server Side Setup
In this I will explain using cpanel but will include how to do it on a normal machine as well. The python code will check the http code of your website, if it returns anything other than 200 "OK" it will switch to backup mode. 
1. It is best practice (at least for me) to have a server that is in a different location, just in case the disruption is more than a local internet or power issue. I have my backup sever in the US and the main server in Japan.
2. Create a python enviorment on your off-site server ```python -m venv /path/to/new/virtual/environment```
3. Activate the enviroment ```source {your_folder_name}/bin/activate``` via the CLI.
4. (optional) If you want to get telegram messages when your server goes down use ```pip install telegram_send``` . You will also need to setup a bot with your telegram account. A good guide is here : https://www.freecodecamp.org/news/how-to-create-a-telegram-bot-using-python/ then to configure it ```telegram-send --configure```. For more info go here : https://pypi.org/project/telegram-send/#installation . 
