# SSD-SS22 : SmartHomies API and UserInterface


## Abstract

The topic of smart home technology gained importance over the last decade, introducing the concept of networking devices and equipment in domestic areas. Increasing demand for renewable energy and efficient usage creates a need for intelligent smart-home systems to contribute to the goals of EUs Energy Efficiency Directive as well as creating a sustainable, reliable, scalable application framework. On the one hand this framework integrates hardware peripherals accessed by an MQTT broker running on a Raspberry Pi. On the other hand a hardware and service engine provides logic and a database for the application. Control and state APIs are defined for standardized communication between hard- and software engines, wherein an asyncAPI is defined for data exchange between MQTT-Server and hardware engine. A user can access the smart home system by entering the right credentials on a website. The web server is created with the flask python library. A graphical dashboards provides the user with weather information requested from Visualcrossing.com, status of sensors and relais and allows to set the status of actuators and define  simple timer switching logic in an interactive way. Alternatively a user may also access the hardware engine directly via its exposed API. Overall this smart service is meant to be a contribution to solve the environmental and energy management challenges of the 21’st century. 


## Concept

In order to interface with an arbitrary number of entities and thus, an arbitrary number of I/O
modules, creating an abstraction layer of the Physical Domain seems reasonable. We call this
abstraction layer (service) Hardware Engine, it has the following tasks:
- Device and I/O inventory
- Interfacing with the I/O modules over MQTT
- Providing a configuration storage and state storage of the Physical Domain
- Providing a configuration API (REST)
- Providing a control API for controlling entities (REST)
- Providing a state API for retrieving the state of entities and the inventory (REST/socket)

The Hardware Engine on its own does not provide any automation functionality nor an appropriate
interface for human entities. This task is performed by the Software engine. 

![alt text](https://github.com/Bennys-Quarter/ssd-ss22/blob/main/Software_Engine/apps/static/assets/Screenshot%202022-06-09%20203826.png)


## Installation
## ✨ Quick Start in `Docker` 

> Get the code 

```bash
$ git clone https://github.com/Bennys-Quarter/ssd-ss22.git
```

> Start the Hardware engine

```bash
$ cd ssd-ss22\Software_Engine
$ docker-compose up  
```

> Start the Software Engine

```bash
$ cd ..\Software_Engine
$ docker-compose up --build 
```
Visit http://localhost:5005 in your browser. The app should be up & running.

## Software Engine structure

```bash
< PROJECT ROOT >
   |
   |-- apps/
   |    |-- api/
   |    |    |-- actor.py                  # manipulation functions for output devices
   |    |    |-- function.py               # inventory, weather and timer functions
   |    |    |-- state.py                  # request function for device data
   |    |    |-- user.py                   # user login and logout
   |    |    |-- User-API.yml              # OpenApi specification
   |    |
   |    |-- home/                          # A simple app that serve HTML files
   |    |    |-- routes.py                 # Define app routes
   |    |
   |    |-- authentication/                # Handles auth routes (login and register)
   |    |    |-- routes.py                 # Define authentication routes  
   |    |    |-- models.py                 # Defines models  
   |    |    |-- forms.py                  # Define auth forms (login and register) 
   |    |
   |    |-- static/
   |    |    |-- <css, JS, images>         # CSS files, Javascripts files
   |    |
   |    |-- templates/                     # Templates used to render pages
   |    |    |-- includes/                 # HTML chunks and components
   |    |    |    |-- navigation.html      # Top menu component
   |    |    |    |-- sidebar.html         # Sidebar component
   |    |    |    |-- footer.html          # App Footer
   |    |    |    |-- scripts.html         # Scripts common to all pages
   |    |    |
   |    |    |-- layouts/                   # Master pages
   |    |    |    |-- base-fullscreen.html  # Used by Authentication pages
   |    |    |    |-- base.html             # Used by common pages
   |    |    |
   |    |    |-- accounts/                  # Authentication pages
   |    |    |    |-- login.html            # Login page
   |    |    |    |-- register.html         # Register page
   |    |    |
   |    |    |-- home/                      # UI Kit Pages
   |    |         |-- index.html            # Index page
   |    |         |-- 404-page.html         # 404 page
   |    |         |-- *.html                # All other pages
   |    |    
   |  config.py                             # Set up the app
   |     __init__.py                        # Initialize the app
   |
   |-- requirements.txt                     # Development modules - SQLite storage
   |-- requirements-mysql.txt               # Production modules  - Mysql DMBS
   |-- requirements-pqsql.txt               # Production modules  - PostgreSql DMBS
   |
   |-- Dockerfile                           # Deployment
   |-- docker-compose.yml                   # Deployment
   |-- gunicorn-cfg.py                      # Deployment   
   |-- nginx                                # Deployment
   |    |-- appseed-app.conf                # Deployment 
   |
   |-- .env                                 # Inject Configuration via Environment
   |-- run.py                               # Start the app - WSGI gateway
   |
   |-- ************************************************************************
```
## Testing

A testing script is provided for automatic testing all api functionalities of the Smart Home service. The results are presented in results.txt. 

The following api paths are provided:

- http://localhost:5005/api/user/login &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; user login via api
- http://localhost:5005/api/user/logout &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  user logout via api
- http://localhost:5005/api/function/inventory &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; here you can see the device id
- http://localhost:5005/api/function/history/{id} &nbsp;&nbsp;&nbsp; get the history of a divice, or use 'all'
- http://localhost:5005/api/function/weather &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; get weather json from https://www.visualcrossing.com
- http://localhost:5005/api/state/{id} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; get sensor reading or actor state
- http://localhost:5005/api/actor/{id}/{state}  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; device id and state={true,false}
- http://localhost:5005/api/actor/{id}/timer &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; access timer function

```bash
$ cd ..\Testing
$ python main.py
```

## License Information



Copyright (c) 2019 - present [AppSeed](http://appseed.us/)

| Atlantis Lite Flask | - |
| ---------------------------------- | --- |
| License Type | MIT  |
| Use for print | **YES** |
| Create single personal website/app | **YES** |
| Create single website/app for client | **YES** |
| Create multiple website/apps for clients | **YES** |
| Create multiple SaaS applications | **YES** |
| End-product paying users | **YES** |
| Product sale | **YES** |
| Remove footer credits | **YES** |
| --- | --- |
| Remove copyright mentions from source code | NO |
| Production deployment assistance | NO |
| Create HTML/CSS template for sale | NO |
| Create Theme/Template for CMS for sale | NO |
| Separate sale of our UI Elements | NO |

<br />

## Project status
FINISHED

---
&copy; - Created by Lukas D'Angelo, Patrick Eder, Benedikt Görgei