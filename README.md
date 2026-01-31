# IOTLebronHouse

This is Lebron James' smart house developed by two very talented programmators Aleksandar Stanković and Mihajlo Orlović.



## How to Run

### 1. Start Docker services

Run the following command in the project root:

```bash
docker compose up
```

#### InfluxDB credentials
- **Username:** `admin`
- **Password:** `adminadmin`

#### Grafana credentials
- **Username:** `admin`
- **Password:** `admin`

---

### 2. Set up Python virtual environment

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
# .venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

---

### 3. Run backend services

Run the server first:

```bash
python server.py
```

Then run the main application:

```bash
python main.py
```

> Optionally, you may use the CLI to control actuators.

---

## Grafana Setup

1. Open Grafana in your browser.
2. Log in using the credentials above.
3. Add a new **Data Source** with the following settings:

- **Type:** InfluxDB
- **Query Language:** Flux
- **URL:** `http://influxdb:8086`
- **Organization:** `iot`
- **Default Bucket:** `home`
- **Token:** `my-super-secret-auth-token`

4. Save & test the data source.
5. Create a dashboard using this data source.

You should now see the data updating in **real time**.