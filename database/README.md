# Schema
Schéma databáze dostupné na https://drive.google.com/file/d/1_wlpANtJWLdLfp_ljaICS_qAwvLAx573/view?usp=sharing

# Docker
`$ sudo docker-compose up`

## Adminer
Pokiaľ nepotrebujeme kontajner s adminerom, stačí ich zakomentovať v docker-compose.yml

## Enviroment
Databáza beží po spustení na localhost:7090, adminer na 7080

# Migrácie
Všetky zmeny štruktúry a dát evidujeme v zložke `migrations/` vo formáte sql príkazov. Skript `import.sh` ich v stanovenom poradí prevolá a udržiava tak databázu v konzistentom stave.

## Init a import dát
Po spustení vliezť do bežiaceho kontajneru a spustiť init skript:
`$ sudo docker exec -it pgdb /bin/bash`
`$ sh tmp/db/import.sh`
