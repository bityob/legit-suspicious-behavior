# legit-suspicious-behavior

There are multiple services here:
* mongo-db - store the raw events
* redis - use for pub/sub between services 
* webhooks-service
* behaviors-service


### Flow
* webhooks-service - Event is received from connector (aka GitHub)
* behaviors-service - Read all the events and check for suspicious behaviors 



### How to run?

Prerequisite: `docker` installed on current system

Note: run each step here in different console

1. Run `smee` to receive webhooks events on localhost
```
smee --path "/github"
```
2. Update the webhook value with recevied `smee` url
3. Run MongoDb with docker
```
$ docker run --rm --name mongo mongo -p 27017:27017
```
4. Run Redis with docker
```
$ docker run --rm --name redis -p 6379:6379 -e ALLOW_EMPTY_PASSWORD=yes bitnami/redis
```
5. Run the `webhook-service` (Flask server) 
```
$ cd <repository-folder>
$ pip install -r requirments.txt
$ set PYTHONPATH=. (on windows)
$ export PYTHONPATH=. (on linux)
$ python app\webhooks\service.py
```
6. Run the `behaviors-service` (Redis listener)
```
$ cd <repository-folder>
$ pip install -r requirments.txt
$ set PYTHONPATH=. (on windows)
$ export PYTHONPATH=. (on linux)
$ python app\behaviors\service.py
```
7. Go to your GitHub repository and start to play and trigger suspicious behaviors. The easiest suppored one is to create a team with `hacker` prefix in your organziation
8. Now you will similiar logs in the console of `behaviors-service`
```
********
Found suspicious behavior
Behavior: TeamWithHackerPrefixBehavior
*********
```
