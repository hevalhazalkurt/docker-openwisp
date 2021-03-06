# Docker-OpenWISP

[![Build Status](https://travis-ci.org/openwisp/docker-openwisp.svg?branch=master)](https://travis-ci.org/openwisp/docker-openwisp)
[![Docker Hub](https://img.shields.io/badge/docker--hub-openwisp-blue.svg)](https://hub.docker.com/u/openwisp)
[![Gitter](https://badges.gitter.im/openwisp/dockerize-openwisp.svg)](https://gitter.im/openwisp/dockerize-openwisp?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
[![Support](https://img.shields.io/badge/support-orange.svg)](http://openwisp.org/support.html)
[![GitHub license](https://img.shields.io/github/license/openwisp/docker-openwisp.svg)](https://github.com/openwisp/docker-openwisp/blob/master/LICENSE)

This repository contains official docker images of OpenWISP. Designed with horizontal scaling, easily replicable deployments and user customization in mind.

![kubernetes](https://i.ibb.co/rGpLq4y/ss1.png)
The sample files for deployment on kubernetes are available in the `deployment-examples/kubernetes/` directory.


## Deployment

**Note:** If you are only examining this OpenWISP capabilities, the [workbench setup](#workbench-setup) documentation below might be helpful.

- [Bare Metal](docs/kubernetes/BARE_METAL.md)
- [Google Cloud](docs/kubernetes/GOOGLE_CLOUD.md)

## Customization

### Workbench setup

1. Install docker & docker-compose.
2. In the root of the repository, run `make develop`, when the containers are ready, you can test them out by going to the domain name of the modules.

#### Notes:
   - Default username & password are `admin`.
   - Default domains are: `dashboard.openwisp.org`, `controller.openwisp.org`, `radius.openwisp.org` and `topology.openwisp.org`.
   - To reach the dashboard you may need to add the openwisp domains set in your `.env` to your `hosts` file, example: `bash -c 'echo "127.0.0.1 dashboard.openwisp.org controller.openwisp.org radius.openwisp.org topology.openwisp.org" >> /etc/hosts'`
   - Now you'll need to do steps (2) everytime you make a changes and want to build the images again.
   - If you want to perform actions like cleaning everything produced by `docker-openwisp`, please use the [makefile options](#makefile-options).


### Changing Python Packages

You can build with your own python package by creating a file named `.build.env` in the root of the repository, then set the variables inside `.build.env` file in `<variable>=<value>` format. Multiple variable should be separated in newline. These are the variables that can be changed:

- `OPENWISP_CONTROLLER_SOURCE`
- `OPENWISP_TOPOLOGY_SOURCE`
- `OPENWISP_RADIUS_SOURCE`
- `OPENWISP_USERS_SOURCE`
- `OPENWISP_UTILS_SOURCE`
- `DJANGO_SOURCE`
- `DJANGO_NETJSONCONFIG_SOURCE`
- `DJANGO_NETJSONGRAPH_SOURCE`
- `DJANGO_X509_SOURCE`
- `DJANGO_FREERADIUS_SOURCE`

For example, if you want to supply your own django and openwisp-controller source, your `.build.env` should be written like this:

```
DJANGO_SOURCE=django==2.1
OPENWISP_CONTROLLER_SOURCE=https://github.com/<username>/openwisp-controller/tarball/master
```

### Disabling Services

**Right now, this is only tentative guide. Errata may exist. Please report errors on the [gitter channel](https://gitter.im/openwisp/dockerize-openwisp).**

- `openwisp-dashboard`: You cannot disable the openwisp-dashboard. It is the heart of OpenWISP and performs core functionalities.
- `openwisp-websocket`: Removing this container will cause the system to not able to update real-time location for mobile devices.

If you want to disable a service, you can simply remove the container for that service, however, there are additional steps for some images:

- `openwisp-topology`: Set the `SET_TOPOLOGY_TASKS` variable to `False`.
- `openwisp-radius` : Set the `SET_RADIUS_TASKS` variable to `False`.
- `openwisp-postgres`:
   - Ensure your database instance reachable by the OpenWISP containers.
   - Ensure your database server supports GeoDjango.
   - Change the [database configuration variables](docs/ENV.md) to point to your instances.
- `openwisp-postfix`:
   - Ensure your SMTP instance reachable by the OpenWISP containers.
   - Change the [email configuration variables](docs/ENV.md) to point to your instances.
- `openwisp-freeradius`: Ensure your freeradius service is reachable on port `1812/udp` and `1813/udp`.

### Makefile Options

Most commonly used:
- `develop`: Bundles all the commands required to build the images and run containers.
- `runtests`: Run testcases to ensure all the services are working.
- `publish`: Build, test and publish the latest official images.
- `clean`: Aggressively purge all the containers, images, volumes & networks related to `docker-openwisp`.

Other options:
- `python-build`: Generate a random django secret and set it in the `.env` file.
- `nfs-build`: Build openwisp-nfs server image.
- `base-build`: Build openwisp-base image. The base image is used in other OpenWISP images.
- `compose-build`: (default) Build OpenWISP images for development.
- `develop-runtests`: Similar to `runtests`, it runs the testcases except doesn't stop the containers after running the tests which maybe desired for debugging & analyzing failing container's logs.
