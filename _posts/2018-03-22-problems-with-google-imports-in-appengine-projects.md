---
layout: post
title: "Problems with Google imports in AppEngine Projects"
description: "just reload google"
category: programming
tags: [python, appengine]
---
{% include JB/setup %}

If you want to use google's [cloud libraries](https://github.com/GoogleCloudPlatform/google-cloud-python) so that you can take advantage bigquery or cloudstorage, you need to add them to the code you deploy with your app. Typically, I check out the repository to a lib directory, then put the lines: 

```python
import os
import sys
# path to lib directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))
```

in the file **appengine_config.py**.

This works when the code is deployed, but it doesn't work locally, where the **lib/google** folder conflicts with the **google-cloud-sdk/platform/google_appengine/google** folder, resulting in the error:

```
ImportError: No module named google.cloud.bigquery
```

or

```
ImportError: No module named google.api_core
```

The solution I've found is to initialize the files **lib/google/__init__.py** and **lib/google/cloud/__init__.py** (so that the version of python running appengine can recognize these folders as packages) and then reload the google module in **appengine_config.py**:

```python
import os
import sys
# path to lib directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))
# google needs to be reloaded so that it is taken from the 'lib' folder, and not the
# sandbox environment. Google needs to be loaded once to trigger python to look for the
# module
import google
reload(google)
# after reloading, trigger importing sub modules so that they are in the sys.modules
# dictionary in the correct location on future handlers
import google.api_core
import google.cloud
import google.cloud.bigquery
```

I'm not sure why this works, but it does.



