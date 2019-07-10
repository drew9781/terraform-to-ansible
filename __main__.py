#! /usr/bin/python3
import json
import sys
import re

def main():
   file = sys.argv[1]
   with open(file, 'r') as myFile:
      #buffer = (myFile.read())
      resources = json.load(myFile)
      resources = resources['values']['root_module']['resources']
   
   inventory = []
   for key in resources:
      if key['provider_name'] == 'proxmox':
         buff = parseResourceProxmox( key )
         inventory.append(buff)
      #print(key)
      
   
   print (inventory)

def parseResourceProxmox( _resource ):
   inventory = {}
   name      = _resource['name']
   _resource = _resource['values']
   
   inventory[ name ] =  {}
   inventory[ name ][ 'ip' ]   =   parseProxmoxIP( _resource['ipconfig0'] )
   inventory[ name ][ 'vm' ]   =   _resource['name']  
   #inventory[ name ][ 'tags' ] =   _resource['tags']  - feat request


   return inventory

def parseProxmoxIP( preFormat ):
   ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', preFormat )
   return ip[0]


main()