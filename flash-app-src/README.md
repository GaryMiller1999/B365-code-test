# IP Checker Flask App


This folder contains a modified version of my original CLI script, which now runs with a Flask wrapper, I've done this to make integration with webhook triggered 
container based solutions easier to integrate. 


## How to use

For a basic docker setup
```
docker run -d -p 5000:5000 garymillerwork/b365test-flask:latest
```

navigate to 127.0.0.1:5000/checkip?ips=**your IPs comma seperated**
