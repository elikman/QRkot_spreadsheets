import os
import secrets

# Google API JSON example (replace this with your actual JSON)
google_api_credentials = {
    "type": "service_account",
    "project_id": "qrkotspreadsheets-448816",
    "private_key_id": "a183bd98b24c71fcf4adefae8963d401f6abaae6",
    "private_key": """-----BEGIN PRIVATE KEY-----
MIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDKF/VkYKSFKk5K
Q+3vG6j0WUj0b5zU/abEK2XZUsVoXNHNE60Y4BPacag6YISPjp0YWXWZwebw3N0W
wa737eFHn/oYlLPS1b+qI8ys6xbEUwcdU9626fh3SDswwjsQnbPC3uMlc6JMeBQE
cpaw1MYcMDCDZsetGiyE/K1Tyv96MdhzT65Ss4YI6cLFml5CjIbKwz+tkArMJr9y
kdXrh1JvbEw8q1b0fykrlU1nPpO92U+bxE6VAjpSQWQhSEZKa1KRlP1mcNAn4rEJ
V+A+i5NRXvq9vVqgnk2gqyeVBiFKuwBpjnBrtfDKpNjCVkUzIlDDcCPYpN1vzGB7
bsV7RDJ1AgMBAAECggEAPvDFSXTb6Glrpq+PXAfWT/u6v/4+7wrstG37s3qW5tD5
upAlOfkX1dHOHhhPUNKO1LWP7co5Hcz7womh76+TmRYW8y7k7oYJwniR100EczKU
paqoU3l9G9FQNfhYIu2qvcdjIRfpdT10pon1qq8p4D+V7GbHS386XFTBurYfaTOs
12cO3O3BAtqY3SjwnSzmVegei/CFQi7al0kzQz7h0bdmh/vIvoSCeDCHhbAtqYTp
oyc9AaSlqEVuwe0NlHyDH69ANwWYAFwNXkkbXFQtkB6Od3PZcqUs7Zfj+0Cc3keU
QCVDkJjgARAkD5Mx62OoLpSuD5GPDbFP7qzyYPNmhQKBgQD3AUfMCTuFdOOpcbGr
6S7y+Y8Qdm8h+wxv11bj0XiYoab5mYPoCDFhOhDoe9fsFTPyIk+h/g6g3+G6N7Z6
IOaZbArXajeV+Z9TIyrXtP6QDH1igAWzkro47CgxThqypJgWYcjSQPSZlalclRjd
/a5qGlywS80V7I9tFrPdj+qNwwKBgQDRc/0YIY0zDZ0GANGozZAnZ4RfumHmo19P
CktoJNeQa1yKq9q6b6sSC/5vGeLoGsxh02XY4/C1/nT/a8XnfCiBQYERrQi9Fbef
15Idpys8FO5BSRbZewAxhICIvmPGDqukqZ+RedqOOwnYKkoKIBk9CTbP/vtxFK+h
GpgmkbajZwKBgQCWJ5Ed1/73Ajfjqdn4R6jizBLMTzL/1T2aP63ykERfhOWcllY5
l8Fs+X+N1LtOKRWK/JCsSWVbJr5yFaw4Ugfc/HEawtdHtJfGUnqY5s5Zgz41wt20
bF4IfIdycaiJMMXD1W3fYt1PAEwUnA6h5LVCiwQNqAbkbQpDpqlw5ywPQQKBgQC5
tDcAQC8qxrUj73H0Ul2vMi7BmUTX8p28PIpjCdc+KpJgOMKzbfKlC5FI/BCcbbYs
Pfwc8uwm0Db3h5xuAzz+bQ98loga7bhitgTM2byRhpU/uQfTRyUCwlIb64IWxkcU
tXfOydUnKd0ulUAT/iWiYhsBCzfwKMEW+7dO6v6dnQKBgQDQ6LprWbxTvGmpN+8W
/pPyKKScy0HipUPwl4nPD4t923CkM0aTnKicrZ8+XWDjpPeTyyj3BJMb4XYy8P1y
wRNC6D4D0vTrsn/oRKe02wB1BvF/yIwQzMGGSkqXC9m78QXWuaU6K31Ebn88BCbx
+H9fIiCj1Ucjm1LjcOTANw0aag==
-----END PRIVATE KEY-----""",
    "client_email": "qrkot-spreadsheets@qrkotspreadsheets-448816.iam.gserviceaccount.com",
    "client_id": "103902447577045894475",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/qrkot-spreadsheets%40qrkotspreadsheets-448816.iam.gserviceaccount.com",
}

# Prepare the environment variables
env_variables = {
    "APP_TITLE": "QRkot_spreadsheets",
    "DESCRIPTION": "Благотворительный фонд",
    "DATABASE_URL": "sqlite+aiosqlite:///./fastapi.db",
    "SECRET": secrets.token_urlsafe(32),
    "FIRST_SUPERUSER_EMAIL": "root@admin.ru",
    "FIRST_SUPERUSER_PASSWORD": "root",
    "TYPE": google_api_credentials["type"],
    "PROJECT_ID": google_api_credentials["project_id"],
    "PRIVATE_KEY_ID": google_api_credentials["private_key_id"],
    "PRIVATE_KEY": f"\"{google_api_credentials['private_key'].replace(chr(10), '\\n')}\"",
    "CLIENT_EMAIL": google_api_credentials["client_email"],
    "CLIENT_ID": google_api_credentials["client_id"],
    "AUTH_URI": google_api_credentials["auth_uri"],
    "TOKEN_URI": google_api_credentials["token_uri"],
    "AUTH_PROVIDER_X509_CERT_URL": google_api_credentials["auth_provider_x509_cert_url"],
    "CLIENT_X509_CERT_URL": google_api_credentials["client_x509_cert_url"],
}

# Write to .env file
with open(".env", "w") as env_file:
    for key, value in env_variables.items():
        env_file.write(f"{key}={value}\n")

print(".env file created successfully!")

