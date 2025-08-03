#Country from IP Lookup - Enter an IP address and find the country that IP is registered in. 
# Optional: Find the Ip automatically.

import requests

def get_ip():
    ip=requests.get('https://api.ipify.org').text
    return ip


ip=str(get_ip())
url='https://ipinfo.io/'+ip+'/json'
response=requests.get(url)
data = response.json()
print(data)
city = data['city']
region = data['region']
country = data['country']
location = data['loc']
org = data['org']
print(f'Your city: {city}')
print(f'Your region: {region}')
print(f'Your country: {country}')
print(f'Your location: {location}')
print(f'Your org: {org}')

