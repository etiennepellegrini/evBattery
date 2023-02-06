Periodically check EV stats using the smartcar.com API

## Setup

Fork or clone this repository:

```console
$ git clone git@github.com:etiennepellegrini/evBattery
```

Install dependencies (preferably in a virtual environment, such as
`evBattery/.evBattery_env`

```console
(.evBattery_env) $ pip install -r requirements.txt
```

## Authentication

First, you will need to create an account with [Smartcar][]. 
Follow their instructions under `Retrieve your credentials` to setup a client ID and secret.
Set your [Smartcar][] redirect URI to `http://localhost:8000/exchange`.

Once the [Smartcar][] setup is done, create a file at `data/.credentials.sh`[^1] containing:

```
export SMARTCAR_CLIENT_ID=<your-client-id>
export SMARTCAR_CLIENT_SECRET=<your-client-secret>
export SMARTCAR_REDIRECT_URI=http://localhost:8000/exchange
```
[^1]: :warning **DO NOT ADD THIS FILE TO SOURCE CONTROL!** It contains personal credentials :warning:

Source it:

```console
(.evBattery_env) $ source data/.credentials.sh
```

Start the main "web app" to authorize Smartcar (one time only):

```console
(.evBattery_env) $ cd src
(.evBattery_env) $ python evBattery.py
```

Open a web browser to `http://localhost:8000/login` and follow the
instructions.

A correct authentication ultimately redirects you to `http://localhost:8000/vehicle`.
A file should be created at `data/.acces.db`[^1] containing your access token data. 

## Usage

Once authentication has proceeded correctly once, vehicle stats may be recovered
by running:

```console
(.evBattery_env) $ python get_battery_stats.py
```

### Bash script

A bash script is provided for automated stats extraction:

```console
$ ./get_battery_stats.sh
```

The script follows the following steps:

1. Source the environment activation script
2. Run `ev_battery_stats.py`
3. Switch to the `data` branch and save `car_stats.jsonl`

[Smartcar]: https://www.smartcar.com
