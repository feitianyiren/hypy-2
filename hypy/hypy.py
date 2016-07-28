#!/usr/bin/env python3
# coding: utf-8

import hvclient
import click
import configparser

@click.group()
def main():
    pass

@main.command(help='List virtual machines and its indexes')
@click.option('--sync', '-s', is_flag=True, help='Syncronize with server updating local cache')
def list(sync):
    hvclient.update_cache(sync)
    hvclient.list_vms()

@main.command(help='List virtual machine snapshots')
@click.argument('index')
def snaps(index):
    hvclient.list_vm_snaps(int(index))

@main.command(help='Restore virtual machine snapshot')
@click.argument('index')
@click.argument('snap_name')
def restore(index, snap_name):
    hvclient.restore_vm_snap(int(index), snap_name)

@main.command(help="Create a new snapshot with vm's current state")
@click.argument('index')
@click.argument('snap_name')
def create(index, snap_name):
    hvclient.create_vm_snapshot(int(index), snap_name)

@main.command(help='Connect to virtual machine identified by index')
@click.argument('index')
def connect(index):
    hvclient.connect(int(index))

@main.command(help='Start virtual machine identified by index')
@click.argument('index')
def start(index):
    hvclient.start_vm(int(index))

@main.command(help='Stop virtual machine identified by index')
@click.argument('index')
def stop(index):
    hvclient.stop_vm(int(index))

def load_config():
    config = configparser.ConfigParser()
    config.read('hypy.conf')

    credentials = config['credentials']

    configuration = {}
    configuration['user'] = credentials['user']
    configuration['pass'] = credentials['pass']
    configuration['domain'] = credentials['domain']
    configuration['host'] = credentials['host']

    options = config['options']

    configuration['cache_file'] = options['cache_file']
    configuration['sync_interval'] = options['sync_interval']

    hvclient.setup(configuration)

if __name__ == "__main__":
    load_config()
    main(obj={})
