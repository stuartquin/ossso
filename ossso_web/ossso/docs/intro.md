---
sidebar_position: 1
---

# Getting Started

Add your first SAML based SSO login.

## What you'll need

API token and API URL

```
OSSSO_API_URL=https://ossso-dev.cloud.stuartquin.com/api
OSSSO_API_TOKEN=<TOKEN>
```

## Redirect to to sign in URL

Create an endpoint to convert a domain to a SSO login link.

OSSSO will lookup the connection matching the supplied `domain` and respond
with a Service Provider redirect URL

Your application should redirect users to this URL to begin the SSO process


import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<Tabs>
  <TabItem value="python" label="Python" default>

```python
import os
from flask import Flask, redirect
app = Flask(__name__)

OSSSO_API_TOKEN = os.environ.get("OSSSO_API_TOKEN")
OSSSO_API_URL = os.environ.get("OSSSO_API_URL")

@app.route('/sso')
def sso():
    domain = "example.com"
    headers = {
        "Authorization": f"Token {OSSSO_API_TOKEN}",
    }
    url = f"{OSSSO_API_URL}/v1/connection/url?domain={domain}"
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    data = json.loads(response.read().decode("utf-8"))

    return redirect(data["redirect_url"])
```

  </TabItem>
</Tabs>


## Handle OSSSO Callback

After a successful SSO sign-in, OSSSO will make a POST request back to your
application along with a unique code to retrieve the login details.


<Tabs>
  <TabItem value="python" label="Python" default>

```python
import os
from flask import Flask, redirect
app = Flask(__name__)

OSSSO_API_TOKEN = os.environ.get("OSSSO_API_TOKEN")
OSSSO_API_URL = os.environ.get("OSSSO_API_URL")

@app.route('/callback')
def callback():
    code = request.args.get('code')
    headers = {
        "Authorization": f"Token {OSSSO_API_TOKEN}",
    }
    url = f"{settings.OSSSO_API_URL}/v1/response/{code}"
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    saml_response_data = json.loads(response.read().decode("utf-8"))

    # {"FirstName": ["Joe"], "LastName": ["Blogs"], "Email": ["joe@bloggs.com"]}
```

  </TabItem>
</Tabs>
