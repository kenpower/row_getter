Testing

````
pip install -e . 
pytest
```


Virtual Environment

```
python -m venv env
source env/Scripts/activate
pip install -r requirements.txt
```

## Sign in with Google

When you perform local tests or development, you must add both http://localhost and http://localhost:<port_number> to the Authorized JavaScript origins box.

https://developers.google.com/identity/gsi/web/guides/get-google-api-clientid

https://developers.google.com/identity/gsi/web/guides/display-button

## .data folder for secrets

.data is the standard palce in glitch for secret files
