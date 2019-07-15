import unittest

from terraform_to_ansible import parseProxmoxIP, parseResourceProxmox, parseResources, buildGroupList

class test_terraform_to_ansible(unittest.TestCase):
    def test_parseProxmoxIP(self):
        self.assertEqual(parseProxmoxIP("ip=192.168.1.5/24,gw=192.168.1.1"), "192.168.1.5")
        self.assertEqual(parseProxmoxIP("ip=10.88.24.69/28,gw=10.0.0.0"), "10.88.24.69")

    def test_parseResourceProxmox(self):
        json = {    "address": "proxmox_vm_qemu.cloudinit-test",
                    "mode": "managed",
                    "name": "cloudinit-test",
                    "provider_name": "proxmox",
                    "schema_version": 0,
                    "tainted": True,
                    "type": "proxmox_vm_qemu",
                    "values": {
                        "agent": 0,
                        "bridge": "vmbr0",
                        "ci_wait": None,
                        "cores": 3,
                        "desc": "tf description",
                        "disk": [],
                        "disk_gb": 4,
                        "force_create": None,
                        "id": "pve/qemu/104",
                        "ipconfig0": "ip=192.168.1.5/24,gw=192.168.1.1",
                        "ipconfig1": None,
                        "iso": None,
                        "mac": None,
                        "memory": 2560,
                        "name": "tftest1.xyz.com",
                        "nameserver": None,
                        "network": [],
                        "nic": "virtio",
                        "onboot": None,
                        "os_network_config": None,
                        "os_type": "cloud-init",
                        "preprovision": None,
                        "qemu_os": None,
                        "searchdomain": None,
                        "sockets": 1,
                        "ssh_forward_ip": None,
                        "storage": "local",
                        "storage_type": None,
                        "vlan": -1  
                        }
                    }
        json_result= {
            "cloudinit-test": {
                "ansible_host": "192.168.1.5",
                "vm": "tftest1.xyz.com"
            }
        }
        self.assertDictContainsSubset(json_result, parseResourceProxmox(json))
   
    def test_parseResources(self):
        json = [
                {
                    "address": "proxmox_vm_qemu.cloudinit-test",
                    "mode": "managed",
                    "name": "cloudinit-test",
                    "provider_name": "proxmox",
                    "schema_version": 0,
                    "tainted": True,
                    "type": "proxmox_vm_qemu",
                    "values": {
                        "agent": 0,
                        "bridge": "vmbr0",
                        "ci_wait": None,
                        "cores": 3,
                        "desc": "tf description",
                        "disk": [],
                        "disk_gb": 4,
                        "force_create": False,
                        "id": "pve/qemu/104",
                        "ipconfig0": "ip=192.168.1.5/24,gw=192.168.1.1",
                        "ipconfig1": None,
                        "iso": None,
                        "mac": None,
                        "memory": 2560,
                        "name": "tftest1.xyz.com",
                        "nameserver": None,
                        "network": [],
                        "nic": "virtio",
                        "onboot": True,
                        "os_network_config": None,
                        "os_type": "cloud-init",
                        "preprovision": True,
                        "qemu_os": None,
                        "searchdomain": None,
                        "sockets": 1,
                        "ssh_forward_ip": None,
                        "storage": "local",
                        "storage_type": None,
                        "target_node": "pve",
                        "vlan": -1
                    }
                },
                {
                    "address": "proxmox_vm_qemu.cloudinit-test",
                    "mode": "managed",
                    "name": "test-2",
                    "provider_name": "proxmox",
                    "schema_version": 0,
                    "tainted": True,
                    "type": "proxmox_vm_qemu",
                    "values": {
                        "agent": 0,
                        "bridge": "vmbr0",
                        "ci_wait": None,
                        "cores": 3,
                        "desc": "vm-test2",
                        "disk": [],
                        "disk_gb": 4,
                        "force_create": False,
                        "id": "pve/qemu/104",
                        "ipconfig0": "ip=10.11.54.28/12,gw=10.11.24.88",
                        "ipconfig1": None,
                        "iso": None,
                        "mac": None,
                        "memory": 2560,
                        "name": "vm-test2",
                        "nameserver": None,
                        "network": [],
                        "nic": "virtio",
                        "onboot": True,
                        "os_network_config": None,
                        "os_type": "cloud-init",
                        "preprovision": True,
                        "qemu_os": None,
                        "searchdomain": None,
                        "sockets": 1,
                        "ssh_forward_ip": None,
                        "storage": "local",
                        "storage_type": None,
                        "target_node": "pve",
                        "vlan": -1,
                        "tags":{
                            "group": "test2",
                            "feature": "awesome"
                        }
                    }
                }
            ]
        json_result = {
            "cloudinit-test": {
                "ansible_host": "192.168.1.5",
                "vm": "tftest1.xyz.com"
            },
            "test-2":{
                "ansible_host": "10.11.54.28",
                "vm": "vm-test2",
                "tags":{
                    "group": "test2",
                    "feature": "awesome"
                }
            }
        }
        self.assertDictContainsSubset(json_result, parseResources(json))

    def test_buildGroupList(self):
        json = [
                {
                    "address": "proxmox_vm_qemu.cloudinit-test",
                    "mode": "managed",
                    "name": "cloudinit-test",
                    "provider_name": "proxmox",
                    "schema_version": 0,
                    "tainted": True,
                    "type": "proxmox_vm_qemu",
                    "values": {
                        "agent": 0,
                        "bridge": "vmbr0",
                        "cores": 3,
                        "desc": "tf description",
                        "disk": [],
                        "disk_gb": 4,
                        "id": "pve/qemu/104",
                        "ipconfig0": "ip=192.168.1.5/24,gw=192.168.1.1",
                        "memory": 2560,
                        "name": "tftest1.xyz.com",
                        "network": [],
                        "nic": "virtio",
                        "os_type": "cloud-init",
                        "sockets": 1,
                        "storage": "local",
                        "target_node": "pve",
                        "vlan": -1
                    }
                }
            ]
        json_result = {
                        "_meta": {
                            "hostVars": {
                            "cloudinit-test": {
                                "ansible_host": "192.168.1.5",
                                "vm": "tftest1.xyz.com"
                            }
                            }
                        },
                        "all": {
                            "children": [
                            "ungrouped"
                            ]
                        },
                        "ungrouped": {
                            "hosts": [
                            "cloudinit-test"
                            ]
                        }
                        }
        resource = parseResources(json)
        self.assertDictContainsSubset(json_result, buildGroupList( resource )) 

if __name__ == '__main__':
    unittest.main()