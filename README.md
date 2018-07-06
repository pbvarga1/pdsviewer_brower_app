# Browser PDS Viewer App

Note this repo is not an official PDS app. I made this to practice making a
Flask app with an AngularJS front-end as well learning how to make and deploy an
application using Docker. This repo will not be actively maintained however I
may make updates as I add more complexity where I see I can learn something new.

## Run on Localhost
If you want to run on local host, switch the constants in app.py, start a redis
server, and then run app.py.

## Run on Docker
You can use the local docker-compose.yaml to run on a docker container. The only
requirement is that the manager machine has a ./data file. Here is the docker
image: [pbvarga1/pdsimage](https://hub.docker.com/r/pbvarga1/pdsimage/).

## The App

The home page looks like:

![home page](home.PNG)

After putting an image URL in and selecting an image:

![image loaded](image_loaded.PNG)

The image used in the example is: [FRB_431397159EDR_F0141262FHAZ00323M1.IMG](
https://pds-imaging.jpl.nasa.gov/data/msl/MSLHAZ_0XXX/DATA/SOL00382/FRB_431397159EDR_F0141262FHAZ00323M1.IMG)

It best works with smaller sized images (larger images can work but I've had
some problems).

## License

Copyright (c) 2018 Perry Vargas

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
