Periodically check EV stats using the smartcar.com API

## Setup

### Install

Fork or clone this repository:

```console
$ git clone git@github.com:etiennepellegrini/evBattery
```

Install dependencies (preferably in a virtual environment, such as
`evBattery/.evBattery_env`

```console
(.evBattery_env) $ pip install -r requirements.txt
```

### Authentication (one-time only)

First, you will need to create an account with [Smartcar][]. 
Follow their instructions under `Retrieve your credentials` to setup a client ID and secret.
Set your [Smartcar][] redirect URI to `http://localhost:8000/exchange`.

Once the [Smartcar][] setup is done, create a file at `data/.credentials.sh`[^1] containing:

```
export SMARTCAR_CLIENT_ID=<your-client-id>
export SMARTCAR_CLIENT_SECRET=<your-client-secret>
export SMARTCAR_REDIRECT_URI=http://localhost:8000/exchange
```
[^1]: :warning: **DO NOT ADD THIS FILE TO SOURCE CONTROL!** It contains personal credentials :warning:

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

### Automated periodic save

I use [cron](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/crontab.html) in order to save my car stats periodically.

```cron
0 */8 * * * /path/to/evBattery/get_battery_stats.sh &> $HOME/.cache/evBattery.log
```

*Note*: A free [Smartcar][] account only allows 300 API calls per car per month, or 10 calls per day. The current `evBattery.py` script makes 2 calls (one to the `odometer` endpoint, one to the `battery` endpoint. I therefore set my `cron` job to run every 8 hours or 3 times a day.

[Smartcar]: https://www.smartcar.com
