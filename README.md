<h1 align="center">Attendance System using Face Recognition</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-1.0.0-blue.svg?cacheSeconds=2592000" />
  <a href="https://github.com/codeglitchz/attendance-system#readme" target="_blank">
    <img alt="Documentation" src="https://img.shields.io/badge/documentation-yes-brightgreen.svg" />
  </a>
  <a href="https://github.com/codeglitchz/attendance-system/graphs/commit-activity" target="_blank">
    <img alt="Maintenance" src="https://img.shields.io/badge/Maintained%3F-yes-green.svg" />
  </a>
  <a href="https://github.com/codeglitchz/attendance-system/blob/master/LICENSE" target="_blank">
    <img alt="License: MIT" src="https://img.shields.io/github/license/codeglitchz/attendance-system" />
  </a>
</p>

> A simple, modern and scalable facial recognition based attendance system 
> built with Python back-end & Angular front-end

### 🏠 [Homepage](https://github.com/codeglitchz/attendance-system#readme)

## Table of contents
* [Prerequisites](#prerequisites)
* [Installation](#installation)
    1. [Clone repository](#clone-repository)
    2. [Setup backend](#setup-backend)
    3. [Setup frontend](#setup-frontend)
* [Usage](#usage)
    1. [Using CLI](#using-cli)
    2. [Using Web Interface](#using-web-interface)

## Prerequisites

* Python v3.7+
* Miniconda3 (optional) (recommended)
* Node.js LTS v12.8.0+ (npm v6.14.4+)
* Angular CLI v9.1.8+
* Windows or Linux (macOS not officially supported, but might work)

## Installation

#### 1. Clone repository
```sh
$ git clone https://github.com/codeglitchz/attendance-system
$ cd attendance-system
```
#### 2. Setup backend

Install all dependencies using conda package manager
> Note: This will install the dependencies listed in `environments.yml` file
```sh
$ cd backend
$ conda env create -f environment.yml
```
Now you can activate this environment using the following command
> Note: You can run the app only if this environment is activated
```sh
$ conda activate attendance-system
```

#### 3. Setup frontend
Install all dependencies using npm package manager
> Note: This will install the dependencies listed in `package.json` file
```sh
$ cd frontend
$ npm install
```

## Usage

#### A. Using CLI
Follow these steps to run the app in command line interface mode
* Activate the `attendance-system` conda environment
* Launch `run_cli.py` from the backend directory
```sh
$ cd backend
$ conda activate attendance-system
$ python run_cli.py
```

#### B. Using Web Interface
Start the Flask Web Server 
* Rename `.env.example` file to `.env`
* Activate the `attendance-system` conda environment
* Launch `run.py` from the backend directory
> Note: This will start a flask web server listening on `http://localhost:5000`
```sh
$ cd backend
$ conda activate attendance-system
$ python run.py
```
Launch the Angular Web Application
> Note: This will launch angular web app in browser @ `http://localhost:4200`
```sh
$ cd frontend
$ ng serve -o
```

## Authors

👤 **CodeGlitchz**

* Github: [@codeglitchz](https://github.com/codeglitchz)

👤 **CodeWhizz**

* Github: [@codewhizz](https://github.com/codewhizz)

## 🤝 Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/codeglitchz/attendance-system/issues). You can also take a look at the [contributing guide](https://github.com/codeglitchz/attendance-system/blob/master/CONTRIBUTING.md).

## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

Copyright © 2020 [CodeGlitchz](https://github.com/codeglitchz). <br />
This project is [MIT](https://github.com/codeglitchz/attendance-system/blob/master/LICENSE) licensed.
