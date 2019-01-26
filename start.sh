#!/bin/bash
docker run -d --rm --name hash-alpha --env "REDIS_SERVER"="redis1.innernet" --network innernet com.jimthecactus/hash-search
docker run -d --rm --name hash-beta --env "REDIS_SERVER"="redis1.innernet" --network innernet com.jimthecactus/hash-search
