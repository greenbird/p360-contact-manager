The program runs in a two-step fashion were the first step creates a `worklist`. The `worklist` is then used as input for the second step which is a `synchronize` or `update` step. We chose this way of doing it since it gives some control back to the user before updates start. The speed of the updating depends entirely on how fast the api can handle our update requests. Because of that updating can take time when updating thousands of entries.

!!! attention
    The examples assumes you have a [basic settings.json](../configuring/#settingsjson-file) file setup.

## Installing
```shell
pip install p360-contact-manager
```

This installs the `p360` cli command on your system/in your virtualenv

If you are using a virtualenv, remember to `activate` it.

If you are using `poetry` use `poetry run p360` to run it.

## Configuring
please see [configuring](../configuring)

## Finding duplicates
In Public 360 there can be created duplicates of enterprises. To find these run the program in this

1. Create Worklist
```shell
p360 -o worklist.json duplicates
```
2. Check that the worklist.json looks good and that the update payloads contain expected data.
3. Use worklist to update p360
```shell
p360 -w worklist.json -o result.json update
```

## Synchronize against Brønnøysund Registeret
This takes some search criteria, and all matching entities, will be Synchronized with p360. This means that enterprises which exists will be updated. Enterprises which don't exist in p360 will be created.

For this you need to supply a search criteria payload. The easiest way to do this is to add the following to settings.json in the same folder from which you run the program.

```json
{
    "brreg_search_criteria": {
        "organisasjonsform": ["ANS", "AS", "ASA", "ENK"],
        "konkurs": false,
        "fraAntallAnsatte": 1,
        "registrertIMvaregisteret": true,
        "registrertIForetaksregisteret": true,
        "naeringskode": "A,C,D,E,F,I,K,L,M,N,O,P,Q,R,S",
        "size": 100
    }
}
```

All available search criterias can be found at the [brreg.no api page](https://data.brreg.no/enhetsregisteret/api/docs/index.html#enheter-sok-detaljer)


1. Create Worklist
```sh
p360 -o worklist.json brreg_synchronize
```
2. Check that the worklist.json looks good and that the update payloads contain expected data.
3. Run Synchronize
```sh
p360 -w worklist.json -o result.json synchronize
```


## Caching
You can cache all enterprises found in p360 into a json file which then later can be used as the source for when finding duplicates or checking malformed. This way you don't have to query p360 which can be very slow all the time.

1. Run Cache
```sh
p360 cache
```
2. Use cache with `-c`/`--cached`
```
p360 -o worklist.json --cached duplicates
```
