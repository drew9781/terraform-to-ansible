#! /usr/bin/python3
import json
import sys
import re
import os

def main():
   
   jsonFile = 'json.test'

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
      currentDir = os.path.dirname(os.path.realpath(__file__))
      parentDir  = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
      
      if jsonFile in os.listdir(currentDir):
         file = currentDir + '/' + jsonFile
         print(file)
         sys.exit()
      elif jsonFile in os.listdir(parentDir):
         file = parentDir + '/' + jsonFile

   with open(file, 'r') as myFile:
      #buffer = (myFile.read())
      raw = json.load(myFile)
      modules = raw['values']['root_module']['child_modules'] # [0]['resources']

   resourceList = {}
   for module in modules:
      resourceList[module['address']] = parseResources( module['resources'])

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
   name      = _resource['values']['name'].split('.')[0]
   _resource = _resource['values']
   inventory[ name ] =  {}
   inventory[ name ][ 'ansible_host' ]   =   parseProxmoxIP( _resource['ipconfig0'] )
   inventory[ name ][ 'vm' ]   =   _resource['name']  
   if 'tags' in _resource:
      inventory[ name ][ 'tags' ] =   _resource['tags'] 
   return inventory

def parseProxmoxIP( preFormat ):
   ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', preFormat )
   return ip[0]

def buildGroupList( _resourceList):
   groupList = { '_meta' : { 'hosts' : {} }, 'ungrouped' : { 'hosts' : []}, 'all' : { 'children' : [ 'ungrouped']}}
   for module in _resourceList:
      moduleName = module.split('.')[1]
      groupList[moduleName] = { 'hosts' : []}
      groupList[ 'all' ][ 'children' ].append( moduleName)
      
      for key in _resourceList[module]:
         _resource = _resourceList[module][key]
         groupList['_meta']['hosts'][key] = _resource
         if ('tags' in _resource) and (_resource['tags'] != None):
            if 'group' in _resource['tags']:
               if not _resource[ 'tags' ]['group'] in groupList:
                  groupList[_resource[ 'tags' ]['group']] = {'hosts' : []}
                  groupList[ 'all' ][ 'children' ].append( _resource['tags']['group'] )
               groupList[_resource[ 'tags' ][ 'group' ]][ 'hosts' ].append( key ) # .append(key) is just adding the node to the group
         # don't need to add to ungrouped, because all nodes should be added to their module group now
         #    else:   
         #       groupList[ 'ungrouped' ][ 'hosts' ].append( key )
         # else:
         #    groupList[ 'ungrouped' ][ 'hosts' ].append( key )
         groupList[ moduleName ][ 'hosts' ].append( key )
   return groupList

def parseHost( _groupList ):
   return

if __name__== "__main__":
   main()