#!/usr/bin/env python

# https://www.digitalocean.com/community/projects/python-digitalocean
# https://github.com/koalalorenzo/python-digitalocean
#
#
# pip install -U python-digitalocean
import digitalocean

MANAGED_DROPLETS=["haproxy", "dbms", "appserver1", "appserver2"]

fh = open('/home/jds/.ssh/jds-dod-token')
jds_dod_api_token=fh.readline();
fh.close()

ssh_key_name="id_rsa_jds_hm"
fh = open('/home/jds/.ssh/%s.pub'% ( ssh_key_name ))
jds_ssh_key=fh.readline().rstrip();
fh.close()

def create_vm(droplet_name):
	droplet = digitalocean.Droplet(token=jds_dod_api_token,
								   name=droplet_name,
								   region='nyc2', # New York 2
								   #image='ubuntu-14-04-x64', # Ubuntu 14.04 x64
								   #image='centos-7.1 x64',
								   image='centos-7-0-x64',
								   size_slug='512mb',  # 512MB
								   backups=False,
								   ssh_keys=["%s" % ( jds_ssh_key )],
								   )
	droplet.create()


def helper_list_image_types():
	mgr = digitalocean.Manager(token=jds_dod_api_token)
	images = mgr.get_images()
	for image in images:
		print image.slug	

def list_droplets():
	mgr = digitalocean.Manager(token=jds_dod_api_token)
	managed_droplets = mgr.get_all_droplets()
	for drop in managed_droplets:
		print ""
		print "Host %s" % ( drop.name )
		print "HostName %s" % ( drop.ip_address )
		print "Port 22"
		print "User root"
		print "IdentityFile ~/.ssh/%s" % ( ssh_key_name )
		MANAGED_DROPLETS.remove(drop.name)
		#print "Name: %s IP: %s" % ( drop.name, drop.ip_address )


def destroy_droplets():
	mgr = digitalocean.Manager(token=jds_dod_api_token)
	managed_droplets = mgr.get_all_droplets()
	for drop in managed_droplets:
		print "Destroying Name: %s IP: %s" % ( drop.name, drop.ip_address )
		drop.destroy()


if __name__ == '__main__':
	destroy=True

	list_droplets()

	if destroy:
		destroy_droplets()
	else:
		for droplet_name in MANAGED_DROPLETS:	
			print "Creating Droplet: %s" % ( droplet_name )
			create_vm(droplet_name)

