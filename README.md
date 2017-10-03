# DoSU

## 1. Content

1. [Content](#1-content)
2. [About](#2-about)
3. [Setup](#3-setup)
    1. [Dependencies](#31-dependencies)
    2. [Installation](#32-installation)
    3. [Configuration](#33-configuration)
        1. [Config file](#331-config-file)

## 2. About

__DoSU__ is a small note taking tool in a __pandoc-like__ environment.
It's used to create subjects, write notes, compile notes with your desired structure and tools using pandoc.


What does DoSU stand for ?

> DoSU = Do Something Useful :)

## 3. Setup

### 3.1 Dependencies

- pip (https://pip.pypa.io/en/stable/installing/)
- pandoc (https://pandoc.org/installing.html)

### 3.2 Installation

```
pip install git+git://github.com/tsandrini/dosu.git
```

### 3.3 Configuration

Out of the box __DoSU__ expects from you a set of configuration.

#### 3.3.1 Config file

Copy __config/example.yml__ to your desidered location.
__DoSU__ will look for them in any of these given paths:

- __~/.config/dosu/config.yml__
- __~/.dosu.yml__

Please pay attention to the config file and spend some time configuring your desired options.
