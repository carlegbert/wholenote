Note taking webapp built with flask backend.
More to come later.


#### Running locally with Docker (you will need docker & docker-compose)
* `sudo docker-compose up &`
* use `--build` flag if container is new/updated
* served at localhost:9000

#### Running tests:
* `sudo docker-compose exec website py.test fnote`
* Coverage: `sudo docker-compose exec website py.test --cov-report term-missing --cov fnote` (must be running container)
