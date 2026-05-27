# BA-AssembleNempladsToSQL

Læser CSV-filer fra et mountet netværksdrev, skriver data til SQL Server og arkiverer de behandlede filer. Kører hver mandag kl. 02:00 (Europe/Copenhagen) via Ofelia scheduler.

---

## Struktur

```
.
├── main.py
├── utils/
│   ├── archive_files.py
│   ├── get_engine.py
│   ├── write_indmeldelser.py
│   ├── write_institutioner.py
│   └── write_stuer.py
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## Forudsætninger

- Docker
- Et CIFS-volume mountet til netværksdrevet (se nedenfor)
- SQL Server tilgængelig fra Docker-hosten

---

## Miljøvariabler

Kopiér `.env.example` til `.env` og udfyld værdierne.

| Variabel | Beskrivelse |
|---|---|
| `DB_DRIVER` | ODBC-driverens navn, f.eks. `ODBC Driver 18 for SQL Server` |
| `DB_SERVER` | SQL Server host og port, `xx.xx.xx.xx,xxxx` |
| `DB_NAME` | Databasenavn |
| `DB_USERNAME` | SQL Server brugernavn |
| `DB_PASSWORD` | SQL Server adgangskode |
| `DB_TABLE_INDMELDELSER` | Måltabel for indmeldelsesdata |
| `DB_TABLE_INSTITUTIONER` | Måltabel for institutionsdata |
| `DB_TABLE_STUER` | Måltabel for stuedata |
| `FILE_PATH` | Sti til det monterede drev inde i containeren |
| `CRON_SCHEDULE` | Cron-udtryk, f.eks. `0 2 * * 1` (hver mandag kl. 02:00) |

---

## Volume

Opret det eksterne CIFS-volume før deployment:

```powershell
docker volume create `
  --driver local `
  --opt type=cifs `
  --opt "device=//SERVER/Share$" `
  --opt "o=username=USER,password=PASS,vers=3.0" `
  filer-assemblenemplads
```

---

## Lokal udvikling

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

---

## Docker

Byg og kør lokalt:

```bash
docker compose up --build
```

Portainer:
- Brug `ghcr.io/hjk-automatisering/ba-assemblenempladstosql:main` som image
- Brug `stack.env` i stedet for `.env`
- Det eksterne volume `filer-assemblenemplads` skal eksistere på hosten

---

## CSV-filer

Scriptet forventer følgende filer i `FILE_PATH`:

| Mønster | Beskrivelse |
|---|---|
| `Indmeldelser_YYYYMMDD.csv` | Indmeldelsesdata |
| `Institutioner_YYYYMMDD.csv` | Institutionsdata |
| `Stuer_YYYYMMDD.csv` | Stuedata |

Behandlede filer flyttes til `FILE_PATH/Arkiv` efter en vellykket kørsel. Eksisterende filer i `Arkiv` slettes inden flytning.