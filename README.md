<h1 align="center">Attendance System using Face Recognition</h1>
<p>
  <a href="https://github.com/codeglitchz/attendance-system/releases/tag/v2.0.0" target="_blank">
    <img alt="Version" src="https://img.shields.io/badge/version-v2.0.0-blue.svg?cacheSeconds=2592000" />
  </a>
  <a href="https://github.com/codeglitchz/attendance-system/blob/master/LICENSE" target="_blank">
    <img alt="License: MIT" src="https://img.shields.io/github/license/codeglitchz/attendance-system" />
  </a>
</p>

> A simple, modern and scalable facial recognition based attendance system 
> built with Python back-end & Angular front-end.

![UI](sample/ui.gif)

## Table of contents
* [Prerequisites](#prerequisites)
* [Installation](#installation)
    1. [Clone repository](#1-clone-repository)
    2. [Setup backend](#2-setup-backend)
    3. [Setup frontend](#3-setup-frontend)
* [Usage](#usage)\
    a. [Using CLI](#a-using-cli)\
    b. [Using Web Interface](#b-using-web-interface)

## Prerequisites

* Windows or Linux (macOS not officially supported, but might work)
* Nvidia CUDA (optional - for nvidia gpus)
* [CMake](https://cmake.org/download/)
* [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2019)
* [Miniconda](https://docs.conda.io/en/latest/miniconda.html) for Python v3.7+
* [Node.js LTS](https://nodejs.org/en/) v12.8.0+ (npm v6.14.4+)
* [Angular CLI](https://cli.angular.io/) v9.1.8+

## Installation

#### 1. Clone repository
For stable release, clone `master` branch
```sh
$ git clone -b master https://github.com/codeglitchz/attendance-system.git
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

## 🤝 Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/codeglitchz/attendance-system/issues).

## Show your support

Give a ⭐️ if this project helped you!