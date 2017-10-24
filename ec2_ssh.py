from __future__ import print_function

import argparse
import os
import random
import sys
import inquirer

import boto3

__version__ = '1.9.0'

parser = argparse.ArgumentParser(
    description="""
    SSH into an ec2 host where <tag-value> matches a tag which defaults to
    'Name' or environment variable EC2_HOST_TAG. In the case there is more than
    one such instance, one will be chosen at random. 'username' defaults to
    ubuntu.  A small bashrc file is added over ssh to give a nice prompt. Any
    extra arguments at the end are passed to ssh directly.
    """
)
parser.add_argument('-r', '--role', 
                    type=str,
                    default=os.getenv('EC2_ROLE'),
                    help="Role to match")
parser.add_argument('-e', '--env', 
                    type=str,
                    default=os.getenv('EC2_ENV'),
                    help="Environment to match, using network_namespace tag")
parser.add_argument('-u', '--user', 
                    type=str,
                    default=os.getenv('EC2_SSH_USER', ""),
                    help="Which user to connect with, defaults to 'ubuntu'")

def main():
    args, unparsed = parser.parse_known_args()

    if args.user != "":
        username = args.user & "@"
    else:
        username = args.user


    host_name = get_host_name(args)

    if not host_name:
        print("ec2-ssh: no hosts matched", file=sys.stderr)
        sys.exit(1)

    command = [
        'ssh',
        '-t', '-t',
        username + host_name,
    ]

    if unparsed:
        command.extend(unparsed)

    print("ec2-ssh connecting to {}".format(host_name), file=sys.stderr)
    sys.stdout.flush()
    os.execlp(*command)

def get_host_name(args):
    host_list = get_instance_list(args)

    # using inquirer
    if len(host_list) == 1:
        host = host_list[0]
    else:
        questions = [
                inquirer.List('host',
                    message="Which host?",
                    choices=host_list,
                ),
            ]
        host = inquirer.prompt(questions)["host"]
    return host[0]


def ec2_host_parser():
    parser = argparse.ArgumentParser(
        description="Output ec2 public host names for active hosts in random "
                    "order, optionally match a tag which defaults to 'Name' "
                    "or environment variable EC2_HOST_TAG."
    )
    parser.add_argument('value', type=str, nargs='?',
                        help='the value the tag should equal')
    parser.add_argument('-t', '--tag', type=str,
                        default=os.getenv('EC2_HOST_TAG', 'Name'),
                        help='which tag to search')
    return parser


def host():
    args = ec2_host_parser().parse_args()
    instances = get_instance_list(args.tag, args.value)
    random.shuffle(instances)
    for instance in instances:
        print(instance)


def get_instance_list(args):
    conn = boto3.client('ec2')

    filters = [
        {
            'Name': 'instance-state-name',
            'Values': ['running'],
        }
    ]
    if args.role:
        filters.append({
            'Name': 'tag:Roles',
            'Values': [args.role]
        })
    if args.env:
        filters.append({
            'Name': 'tag:network_namespace',
            'Values': [args.env]
        })

    data = conn.describe_instances(Filters=filters)
    instance_list = []
    for reservation in data['Reservations']:
        for instance in reservation['Instances']:
            instance_meta = []
            network_namespace = None
            role = None
            instance_meta.append(instance['PrivateIpAddress'])
            for tag in instance['Tags']:
                if tag['Key'] == 'Roles':
                    role = (tag['Value'])
                if tag['Key'] == 'network_namespace':
                    network_namespace = (tag['Value'])

            instance_meta.append(role or 'None')
            instance_meta.append(network_namespace or 'None')
            instance_list.append(instance_meta)
    return instance_list


if __name__ == '__main__':
    main()
