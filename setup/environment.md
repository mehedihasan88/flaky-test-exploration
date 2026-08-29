# Experiment Environment

## Host Environment

- Platform: WSL2
- Linux Distribution: Ubuntu 26.04 LTS
- Architecture: x86_64
- Maven: 3.9.12
- Java: Temurin OpenJDK 8 (1.8.0_504)

## Subject Project

- Project: Alibaba Fastjson
- Repository: https://github.com/alibaba/fastjson
- Commit: e05e9c5e4be580691cc55a59f3256595393203a1
- IDoFT dataset: `pr-data.csv`
- Maven module: root (`.`)

## Baseline Build

Command:

`mvn -DskipTests package`

Result:

`BUILD SUCCESS`

The initial build completed successfully on the historical Fastjson commit in approximately 3 minutes.
