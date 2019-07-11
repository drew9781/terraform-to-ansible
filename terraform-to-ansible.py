#! /usr/bin/python3
import json
import sys
import re

def main():
   
   try: 
      switch = sys.argv[1]
      if not switch == ('--list' or '--host'):
         print("Error: Use --list or --host")
         sys.exit()
   except IndexError:
      print("Error: Use --list or --host")
      sys.exit()
   try: 
      file = sys.argv[2]
   except IndexError:
      #print("info: Running with no specified file location")
      file = 'json.test'

   with open(file, 'r') as myFile:
      #buffer = (myFile.read())
      resources = json.load(myFile)
      resources = resources['values']['root_module']['resources']
   resourceList = parseResources( resources )
   

   if switch == '--list':
      groupList = buildGroupList( resourceList )
      print(json.dumps(groupList, sort_keys=True, indent=2))

      

def parseResources( _resources ):
   _inventory = {}
   for key in _resources:
      if key['provider_name'] == 'proxmox':
         buff = parseResourceProxmox( key )
         _inventory.update(buff)
      #print(key)
   return _inventory

def parseResourceProxmox( _resource ):
   inventory = {}
   name      = _resource['name']
   _resource = _resource['values']
   inventory[ name ] =  {}
   inventory[ name ][ 'ansible_host' ]   =   parseProxmoxIP( _resource['ipconfig0'] )
   inventory[ name ][ 'vm' ]   =   _resource['name']  
   if 'tags' in _resource:
      inventory[ name ][ 'tags' ] =   _resource['tags'] # - feat request
   return inventory

def parseProxmoxIP( preFormat ):
   ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', preFormat )
   return ip[0]

def buildGroupList( _resourceList):
   groupList = { '_meta' : { 'hostVars' : {} }, 'ungrouped' : { 'hosts' : []}, 'all' : { 'children' : [ 'ungrouped']}}
   for key in _resourceList:
      _resource = _resourceList[key]
      groupList['_meta']['hostVars'][key] = _resource
      if 'tags' in _resource:
         if 'group' in _resource['tags']:
            if not _resource[ 'tags' ]['group'] in groupList:
               groupList[_resource[ 'tags' ]['group']] = {'hosts' : []}
               groupList[ 'all' ][ 'children' ].append( _resource['tags']['group'] )
            groupList[_resource[ 'tags' ][ 'group' ]][ 'hosts' ].append( key )
         else:
            groupList[ 'ungrouped' ][ 'hosts' ].append( key )
   return groupList

def parseHost( _groupList ):
   return

main()