#!/usr/bin/env python3

import certstream
import asyncio

import dns
import dns.resolver

async def res(domain):
    try:
        result = dns.resolver.resolve(domain, 'A')[0]
    except:
        result = ""
    return result


async def parse(vals):
    for domain in vals:
        if "*." in domain:
            continue
        if "mail." in domain:
            continue
        if "autodiscover." in domain:
            continue
        if "cpanel." in domain:
            continue
        if "webmail." in domain:
            continue
        if "webdisk." in domain:
            continue
        resolved = await res(domain)
        print(domain.lower(),"-",resolved)
        outfile = open("output.txt",'a')
        data = domain.lower()+","+str(resolved)+"\n"
        outfile.write(data)
        outfile.close()
    return

def callback(message, context):
    loop = asyncio.get_event_loop()
    if message['message_type'] == "heartbeat":
        return
    if message['message_type'] == "certificate_update":
        all_domains = message['data']['leaf_cert']['all_domains']
        loop.run_until_complete(parse(all_domains))




if __name__ == '__main__':
    certstream_url = 'wss://certstream.calidog.io'
    certstream.listen_for_events(callback, url=certstream_url)