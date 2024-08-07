import telegram_send
import urllib.request 
from urllib.request import Request, urlopen
import requests



# Define your variables from cloudflare
# if you edit a record manually in the Cloudflare Dashboard, then Save the (Record) ID will show up in the Audit Log at the top of dash.cloudflare.com.
zone_id = '{your zone id}'
record_id = "{your record id}"
api_token = "{your api token}"
domain = "{your domain name ex. abc.com}"
new_ip = "{your off-site server ip}"



cloudflareurl = "https://api.cloudflare.com/client/v4/zones/{your zone id}/dns_records/{your record id}"
 #Define the headers
cloudflareheaders = {
    "Content-Type": "application/json",
    "X-Auth-Email": "{your account email}",
    "X-Auth-Key":"{your api token}"
}

# Define the payload for cloudflare
payload = {
    "type": "A",
    "name": domain,
    "content": new_ip,
    "ttl": 1,
    "proxied": True,
    "id": record_id,
    "zone_id": zone_id
}
#here is just making the request seem like a real computer
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
req = Request(
    url='http://abc.com/checkstatus', 
    headers={'User-Agent': 'Mozilla/5.0'})

#testing if we get a 200 response, if not it goes to the except block
#print is used here just for seeing the ouput
try:
    print(urllib.request.urlopen(req).getcode())
#if there is an exception (ie. the server can't be reached) it throws an error. We use this to change the ip to our backup and send da message on telegram. 
except urllib.error.HTTPError as e:
    #here we are setting the error message
    message = f"OH GOD THE SERVER IS DOWN OH GOD " + f"HTTP Error {e.code}: {e.reason}"
    #sending the error message
    telegram_send.send(messages=[message])
    #sending a put request to cloudflare to update the IP to be the backup server
    response = requests.put(cloudflareurl, headers=cloudflareheaders, json=payload)
    #this returns if the update to the records was successful or not
    if response.status_code == 200:
        print("DNS record updated successfully!")
        message = "Backup server success"
        telegram_send.send(messages=[message])
    else:
        message = f"Failed to update DNS record. Status code: {response.status_code}"
        print(f"Failed to update DNS record. Status code: {response.status_code}")
        telegram_send.send(messages=[message])
        print(response.json())

