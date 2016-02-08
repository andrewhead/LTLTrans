# Launch Scripts for a Tutorons server

To deploy to the server, run:

    ./deploy

Useful tags, that can be specified with the `--tags` argument, include:
* `updatecode`: fetch the code and restart web application
* `pythonpkgs`: update the Python dependencies
* `scripts`: run setup scripts
* `processes`: reload the supervisord processes the web app depends on
