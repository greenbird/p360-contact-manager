## Authkey

| cli short | cli long | settings.json | env variable |
| - | - | - | - |
| `-ak` | `--authkey` | `authkey` | `P360_AUTHKEY` |

The `authkey` is used to authenticate against the P360 api. We use the value as is.


## P360 Base Url

| cli short | cli long | settings.json | env variable |
| - | - | - | - |
| `-pbu` | `--p360_base_url` | `p360_base_url` | `P360_P360_BASE_URL` |

Base Url to the P60 api. Should end in `/`

## Brønnøysund Register Base Url

| cli short | cli long | settings.json | env variable |
| - | - | - | - |
| `-bu` | `--brreg_base_url` | `brreg_base_url` | `P360_BRREG_BASE_URL` |

Base Url to the brreg api. Should end in `/`

## Worklist

| cli short | cli long | settings.json | env variable |
| - | - | - | - |
| `-w` | `--worklist` | `worklist` | `P360_WORKLIST` |

Worklist argument is used to provide what worklist file should be taken as input

## Output

| cli short | cli long | settings.json | env variable |
| - | - | - | - |
| `-o` | `--output` | `output` | `P360_OUTPUT` |

Output argument is used to tell the program where and what to call the resulting file


## Error Margin

| cli short | cli long | settings.json | env variable |
| - | - | - | - |
| `-em` | `--error_margin` | `error_margin` | `P360_ERROR_MARGIN` |

Default: `50`

Lets you decide after how many timeouts or errors during processing the program should give up and exit.

## Dry

| cli short | cli long | settings.json | env variable |
| - | - | - | - |
| `-d` | `--dry` | `dry` | `P360_DRY` |

Default: `False`

Dry lets you decide if you want to do a test run that intercepts all calls to p360 update and synchronize and thus does not actually update anything. It lets you for example see if the worklist file is okay.

## Brreg Search Criteria

| cli short | cli long | settings.json | env variable |
| - | - | - | - |
| `N/A` | `N/A` | `brreg_search_criteria` | `N/A` |

Brreg search criteria is used when we search for organizations in brreg.no with the `action` `brreg_synchronize`. The result of this search is used to build a synchronize worklist that can then be used to update/create entries in p360. The criterias should be as limiting as possible to prevent huge amounts of enterprises being fetched.

The brreg API has a max amount of results at `10 000` so try to make the criterias quite limiting.

All the available parameteres can be found here: [brreg api](https://data.brreg.no/enhetsregisteret/api/docs/index.html#enheter-sok-detaljer)


## P360 Search Criteria

| cli short | cli long | settings.json | env variable |
| - | - | - | - |
| `N/A` | `N/A` | `p360_search_criteria` | `N/A` |

P360 search criteria is to have some sort of way to limit the result of enterprises we should do work on. For example when finding duplicates we should only ever check enterprises that are `Active=True`

Check your p360 api for what parameters you can use

## Duplicate remove payload

| cli short | cli long | settings.json | env variable |
| - | - | - | - |
| `N/A` | `N/A` | `duplicate_remove_payload` | `N/A` |

This payload is used when we update enterprises in p360 that are flagged as duplicates.

It should look something like this.

```json
"duplicate_remove_payload": {
    "Recno": null,
    "Active": false,
    "EnterpriseNumber": ""
}
```

Here you can choose what to do with the Recno and Enterprise number and actually any other parameter than the `/UpdateEnterprise` endpoint can handle. This means that you can set for example `name` to `Disabled by duplicatecheck` or anything you want.
