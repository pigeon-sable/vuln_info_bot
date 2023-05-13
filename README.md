# vc_manager

![vuln_info_bot](https://github.com/pigeon-sable/vuln_info_bot/blob/images/README_image.png)

## Description

This bot is for muttering vulnerability information.

## Requirement

python 3.11.0

## Usage

### 1. Clone this repository

```bash
git clone git@github.com:pigeon-sable/vuln_info_bot.git
```

or

```bash
git clone https://github.com/pigeon-sable/vuln_info_bot.git
```

### 2. Change the working directory

```bash
cd vuln_info_bot
```

### 3. Rename .env_example to .env and enter your Discord Bot token

Do not enclose in single quotes("'").

```bash
cp .env_example .env
vim .env
    ACCESS_TOKEN=123456789abcdefg
```

### 4. Run the program

If you want to run it in a local environment, you can do so with the following command.

```bash
pip install -r requirements.txt
python src/vulnerability_collector.py
```

Alternatively, a container can be used to run it. To execute, the following command is used.
The docker repository is at the following URL.

[https://hub.docker.com/repository/docker/mozsecurity/vuln_info_bot/general](https://hub.docker.com/repository/docker/mozsecurity/vuln_info_bot/general)

```bash
docker pull mozsecurity/vuln_info_bot:latest
docker run --rm --env-file .env mozsecurity/vuln_info_bot:latest
```

## Licence

[Apache License, Version2.0](https://github.com/pigeon-sable/vuln_info_bot/blob/main/LICENSE)

## Author

[Kobayashi123](https://github.com/Kobayashi123)
