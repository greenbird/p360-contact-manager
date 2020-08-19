Configuring this program can be done 3 places:

* settings.json
* environment variables
* commandline arguments

Where commandline arguments overwrites environment variables which in turn overwrites arguments set in settings.json.

The required arguments for each `action` are different, but mostly it boils down to `--authkey`, `--output`, `--worklist` and two url arguments `p360_base_url` and `brreg_base_url`

!!! note Authkey
    The authkey is here so that we can authenticate against the p360 API. Without this we cannot fetch data nor update data.

Check the [argument list](../arguments) for all available arguments

## Settings.json file
The `settings.json` file can actually store all arguments that are available in this program. However, I would advice against storing `action` and possibly `--authkey` in `settings.json`. `action` because action usually need to be different each time since we are doing everything in two steps. `--authkey` because we don't support an encrypted key, but you can if you want to.

A basic `settings.json` file looks something like this

```json
{
    "authkey": "some authkey",
    "p360_base_url": "somep360url.com/api/",
    "brreg_base_url": "https://data.brreg.no/enhetsregisteret/api/",
    "cached": false,
    "dry": false,
    "error_margin": 50,
    "brreg_search_criteria": {
        "organisasjonsform": ["AS", "ASA", "ENK"],
        "konkurs": false,
        "fraAntallAnsatte": 1,
        "registrertIMvaregisteret": true,
        "registrertIForetaksregisteret": true,
        "naeringskode": "A,C,D,E",
        "size": 100
    },
    "p360_search_criteria": {
        "parameter": {
            "Active": true,
            "Page": 0,
            "MaxRows": 20,
            "SortCriterion": "RecnoDescending",
            "IncludeCustomFields": false
        }
    },
    "duplicate_remove_payload": {
        "Recno": null,
        "Active": false,
        "EnterpriseNumber": ""
    }
}
```

## Environment Variables
It might be usefull to set arguments with `environment variables` instead. You can do this by prepending the argument with P360_ and capitalize the argument.

ie:
`error_margin` -> `P360_ERROR_MARGIN`
`brreg_base_url` -> `P360_BRREG_BASE_URL`
`p360_base_url` -> `P360_P360_BASE_URL`

## Commandline Arguments
All commands have a shorthand and a long version use whichever you like.

`brreg_search_criteria`, `p360_search_criteria` and `duplicate_remove_payload` cannot be given as a cli argument at the moment.
