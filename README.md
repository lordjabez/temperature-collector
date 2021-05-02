# Temperature Collector

An AWS Lambda function that collects data from my thermostats and corresponding outdoor
temperatures. It polls two different thermostat technologies, a Honeywell Gateway and a
Google Nest, as well as the OpenWeather API.


## Prerequisites

*  [Python 3](https://www.python.org/downloads/)
*  [terraform](https://www.terraform.io/downloads.html)


## Token Creation

First set up a project in the [Google Device Access](https://console.nest.google.com/device-access)
console. From there you will need the project ID, the client ID, and the client secret; copy
them to a safe place.

Then run the following to open the Google login page.

```bash
utilities/open-login.py CLIENT_ID PROJECT_ID
```

Complete the login flow, and from the redirected URL, extract the `code` parameter and
copy it to a safe place. Now run the following:

```bash
utilities/get-tokens.py CLIENT_ID CLIENT_SECRET CODE
```

Take the resultant refresh token from the above script, and copy it to a safe place.


## Deployment

Deploy the Lambda by running `terraform plan` from the `terraform` folder. Once
the infrastructure is deployed, modify the created `temperature-collector-config` secret
and add the following values:

*  `greyHavenLocation`: Comma-separated lat/lon of location of [Airbnb](https://www.airbnb.com/h/the-grey-haven)
*  `sanDiegoLocation`: Comma-separated lat/lon of location of home
*  `honeywellLocationId`: Unique identifier for Honeywell Gateway (read out of console URL)
*  `honeywellLabels`: Mapping of Honeywell zone IDs to zone names (formatted as `key:value,key:value`)
*  `honeywellUsername`: Honeywell account username
*  `honeywellPassword`: Honeywell account password
*  `nestProjectId`: Project ID from earlier Google console step
*  `nestClientId`: Client ID from earlier Google console step
*  `nestClientSecret`: Client Secret from earlier Google console step
*  `nestRefreshToken`: Refresh token output from earlier `get-tokens.py` script output
*  `openWeatherApiKey`: OpenWeather API key from account page


## Usage

Every five minutes the Lambda will be triggered, and write the following metrics to CloudWatch:

*  `Temperatures/SanDiego/Outside/Temperature`
*  `Temperatures/SanDiego/Downstairs/Temperature`
*  `Temperatures/SanDiego/Downstairs/HeatSetpoint`
*  `Temperatures/SanDiego/Downstairs/CoolSetpoint`
*  `Temperatures/TheGreyHaven/Outside/Temperature`
*  `Temperatures/TheGreyHaven/Downstairs/Temperature`
*  `Temperatures/TheGreyHaven/Downstairs/HeatSetpoint`
*  `Temperatures/TheGreyHaven/Downstairs/CoolSetpoint`
*  `Temperatures/TheGreyHaven/Upstairs/Temperature`
*  `Temperatures/TheGreyHaven/Upstairs/HeatSetpoint`
*  `Temperatures/TheGreyHaven/Upstairs/CoolSetpoint`


## To-Do

*  Make the configuration of thermostats more generic, vs being specific to the author's setup.

*  If Google ever gets around to implementing an API for the Nest remote temperature
   sensor it could be added here.
