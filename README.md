Note taking webapp built with flask backend.
More to come later.


#### Running locally with Docker (you will need docker & docker-compose)
* Rename `example.env` (in the base directory) to `.env` and change variable values in it as you see fit
* Rename `fnote/config/settings.py.example` to `fnote/config/settings.py` and change variable values in it as you see fit
* `sudo docker-compose up &`
* use `--build` flag if container is new/updated
* served at localhost:9000

#### Running tests:
* `sudo docker-compose exec website py.test fnote`
* Coverage: `sudo docker-compose exec website py.test --cov-report term-missing --cov fnote` (must be running container)
