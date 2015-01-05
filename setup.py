"""
EC2-SSH
=======

A pair of command line utilities for finding and sshing into your Amazon EC2
instances by tag (such as 'Name').

A few examples:

::

    % ec2-ssh nginx2
    # equivalent to
    # ssh ubuntu@ec2-123-45-67-89.compute-1.amazonaws.com

    % ec2-ssh root@appserver
    % ec2-ssh deploy@nginx2 sudo restart nginx

    # accompanying ec2-host script

    # w/o arg: prints all active instances
    % ec2-host
    ec2-123-45-67-89.compute-1.amazonaws.com
    ec2-132-45-67-89.compute-1.amazonaws.com
    ec2-231-45-67-89.compute-1.amazonaws.com

    # w/ arg
    % ec2-host backend
    ec2-132-45-67-89.compute-1.amazonaws.com
    ec2-132-45-67-90.compute-1.amazonaws.com

    # w/ tag arg too
    % ec2-host -t environment production
    ec2-132-45-67-90.compute-1.amazonaws.com
    ec2-111-45-67-90.compute-1.amazonaws.com


Links
`````

* `Website <http://github.com/adamchainz/ec2-ssh>`_

Changelog
`````````

* 1.0 - initial release
* 1.1 - override prompt (PS1) to show tag name
* 1.1.1 - Add line echoing host before establishing SSH connection
* 1.2 - Merged pull requests to add region and tag support
* 1.2.1 - Fix issue when ec2-host finds one offline instance with same name as an online instance
"""


from setuptools import setup


setup(
    name = "ec2-ssh",
    version = "1.3.0",
    author = "Adam Johnson",
    author_email = "me@adamj.eu",
    description = "SSH into EC2 instances via tag name",
    long_description = __doc__,
    license = "MIT",
    url = "https://github.com/adamchainz/ec2-ssh",
    keywords = ["amazon", "aws", "ec2", "ami", "ssh", "cloud", "boto"],
    install_requires = ['boto>=1.0'],
    scripts = ["bin/ec2-host", "bin/ec2-ssh"],
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Utilities"
        ],
)
