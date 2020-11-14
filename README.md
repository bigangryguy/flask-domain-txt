<!-- PROJECT LOGO -->
<p align="center">
    <h3 align="center">Domain  record service</h3>
  <p align="center">
    A Flask demonstration project for serving TXT records for fictitious domains and resources.
    <br />
    <a href="https://github.com/bigangryguy/flask-domain-txt"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/bigangryguy/flask-domain-txt/issues">Report Bug</a>
    ·
    <a href="https://github.com/bigangryguy/flask-domain-txt/issues">Request Feature</a>
  </p>
</p>

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project
A Python Flask and SQLAlchemy demo project for serving TXT records for fictitious domains 
and resources. This is nothing more than a made up use case for learning Flask and 
SQLAlchemy and is not intended for any real world purpose. However, if you find anything 
useful in it for your own learning, that would make me happy.

This project is the backend to an [Angular frontend](https://github.com/bigangryguy/angular-domain-txt) 
and both need to be running together for a fully functioning system.


### Built With

* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [SQLAlchemy](https://www.sqlalchemy.org/)


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps. The instructions assume you are on a
Linux or Unix-like system. I can verify this will work on macOS as well.

### Prerequisites

You will need to have [Python 3.8+](https://www.python.org/) installed on your system to 
run the service. In addition, you will need the following Python modules. All of these 
are listed in the `requirements.txt` file included in the repository. Versions listed are 
those used during development; versions greater than those _should_ work.

* click 7.1.2
* Flask 1.1.2
* itsdangerous 1.1.0
* Jinja2 2.11.2
* MarkupSafe 1.1.1
* Werkzeug 1.0.1
* SQLAlchemy 1.3.19
* Flask-SQLAlchemy 2.4.4
* Flask-Cors 3.0.9
* marshmallow 3.8.0
* pytest 6.1.1

### Installation

1. Clone the repo
```shell script
git clone https://github.com/bigangryguy/flask-domain-txt.git
```
2. Install prerequisites (see above). This can be done quickly using `pip` by running:
```shell script
pip install -r requirements.txt
```

<!-- USAGE EXAMPLES -->
## Usage

This is a standard Flask project. To run the server in development, execute this command in the source code root
folder:
```shell script
./bootstrap.sh
```
The script will set the appropriate environment variables and then run the flask server.



<!-- ROADMAP -->
## Roadmap

None - this is a completed learning project.


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the GPLv3 License. See `COPYING` for more information.

<!-- CONTACT -->
## Contact

David Wilcox - [@davidtwilcox](https://twitter.com/davidtwilcox) - david@dtwil.co

Project Link: [https://github.com/bigangryguy/flask-domain-txt](https://github.com/bigangryguy/flask-domain-txt)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/bigangryguy/repo.svg?style=flat-square
[contributors-url]: https://github.com/bigangryguy/repo/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/bigangryguy/repo.svg?style=flat-square
[forks-url]: https://github.com/bigangryguy/repo/network/members
[stars-shield]: https://img.shields.io/github/stars/bigangryguy/repo.svg?style=flat-square
[stars-url]: https://github.com/bigangryguy/repo/stargazers
[issues-shield]: https://img.shields.io/github/issues/bigangryguy/repo.svg?style=flat-square
[issues-url]: https://github.com/bigangryguy/repo/issues
[license-shield]: https://img.shields.io/github/license/bigangryguy/repo.svg?style=flat-square
[license-url]: https://github.com/bigangryguy/repo/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/davidtwilcox
[product-screenshot]: images/screenshot.png
