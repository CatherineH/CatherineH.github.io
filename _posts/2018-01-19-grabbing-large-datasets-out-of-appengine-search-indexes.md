---
layout: post
title: "Grabbing Large Datasets out of AppEngine Search Indexes"
description: ""
category: programming 
tags: [python, web development, appengine]
---
{% include JB/setup %}

If you're building a Big Data application on AppEngine, you'll probably need to grab more than a thousand entries out of a search index. It turns out this is not as straightforward as expected. I've built a [sample project](https://github.com/CatherineH/appengine-large-offset-example) to demo how to do this.

In this demo we initialize our index to have 3000 entries of the numbers between 0 and 3000:

```python
search_index = search.Index(name=INDEX_NAME, namespace=NAMESPACE)
for i in range(3000):
    fields = [search.NumberField(name='number_value', value=i),
              search.NumberField(name='last_modified', value=int(time()))]
    doc = search.Document(fields=fields)
    results = search_index.put(doc)
```

A first attempt at building a handler to query this index would be:

```python
class Search(webapp2.RedirectHandler):
    def get(self):
        try:
            limit = int(self.request.get('limit'))
        except:
            limit = DOCS_PER_PAGE_LIMIT
        try:
            offset = int(self.request.get('offset'))
        except:
            offset = 0

        expr_list = [
            search.SortExpression(
                expression='number_value',
                default_value=int(0),
                direction=search.SortExpression.ASCENDING
            )
        ]
        sort_opts = search.SortOptions(expressions=expr_list)
        index = search.Index(name=INDEX_NAME, namespace=NAMESPACE)
        search_query = search.Query(
            query_string='',
            options=search.QueryOptions(
                limit=limit, sort_options=sort_opts, offset=offset, ids_only=False)
        )
```

This works well for values under 1000, but if you try to run the query /search?limit=3000, you'll get the error:

```python
Traceback (most recent call last):
  File "/home/catherine/installed/google-cloud-sdk/platform/google_appengine/lib/webapp2-2.5.2/webapp2.py", line 1535, in __call__
    rv = self.handle_exception(request, response, e)
  File "/home/catherine/installed/google-cloud-sdk/platform/google_appengine/lib/webapp2-2.5.2/webapp2.py", line 1529, in __call__
    rv = self.router.dispatch(request, response)
  File "/home/catherine/installed/google-cloud-sdk/platform/google_appengine/lib/webapp2-2.5.2/webapp2.py", line 1278, in default_dispatcher
    return route.handler_adapter(request, response)
  File "/home/catherine/installed/google-cloud-sdk/platform/google_appengine/lib/webapp2-2.5.2/webapp2.py", line 1102, in __call__
    return handler.dispatch()
  File "/home/catherine/installed/google-cloud-sdk/platform/google_appengine/lib/webapp2-2.5.2/webapp2.py", line 572, in dispatch
    return self.handle_exception(e, self.app.debug)
  File "/home/catherine/installed/google-cloud-sdk/platform/google_appengine/lib/webapp2-2.5.2/webapp2.py", line 570, in dispatch
    return method(*args, **kwargs)
  File "/home/catherine/python_projects/appengine-large-offset-example/main.py", line 55, in get
    limit=limit, sort_options=sort_opts, offset=offset, ids_only=False)
  File "/home/catherine/installed/google-cloud-sdk/platform/google_appengine/google/appengine/api/search/search.py", line 3073, in __init__
    self._limit = _CheckLimit(limit)
  File "/home/catherine/installed/google-cloud-sdk/platform/google_appengine/google/appengine/api/search/search.py", line 2858, in _CheckLimit
    upper_bound=MAXIMUM_DOCUMENTS_RETURNED_PER_SEARCH)
  File "/home/catherine/installed/google-cloud-sdk/platform/google_appengine/google/appengine/api/search/search.py", line 496, in _CheckInteger
    raise ValueError('%s, %d must be <= %d' % (name, value, upper_bound))
ValueError: limit, 3000 must be <= 1000
``` 

We can't get all 3000 entries in one query, so we'll have to spread the acquisition over three queries:

- /search?limit=1000
- /search?limit=1000&offset=1000
- /search?limit=1000&offset=2000

The first two queries work, but if you set offset to 2000, you'll get the error:

```python
Traceback (most recent call last):
  File "/home/catherine/installed/google-cloud-sdk/platform/google_appengine/lib/webapp2-2.5.2/webapp2.py", line 1535, in __call__
    rv = self.handle_exception(request, response, e)
  File "/home/catherine/installed/google-cloud-sdk/platform/google_appengine/lib/webapp2-2.5.2/webapp2.py", line 1529, in __call__
    rv = self.router.dispatch(request, response)
  File "/home/catherine/installed/google-cloud-sdk/platform/google_appengine/lib/webapp2-2.5.2/webapp2.py", line 1278, in default_dispatcher
    return route.handler_adapter(request, response)
  File "/home/catherine/installed/google-cloud-sdk/platform/google_appengine/lib/webapp2-2.5.2/webapp2.py", line 1102, in __call__
    return handler.dispatch()
  File "/home/catherine/installed/google-cloud-sdk/platform/google_appengine/lib/webapp2-2.5.2/webapp2.py", line 572, in dispatch
    return self.handle_exception(e, self.app.debug)
  File "/home/catherine/installed/google-cloud-sdk/platform/google_appengine/lib/webapp2-2.5.2/webapp2.py", line 570, in dispatch
    return method(*args, **kwargs)
  File "/home/catherine/python_projects/appengine-large-offset-example/main.py", line 55, in get
    limit=limit, sort_options=sort_opts, offset=offset, ids_only=False)
  File "/home/catherine/installed/google-cloud-sdk/platform/google_appengine/google/appengine/api/search/search.py", line 3082, in __init__
    self._offset = _CheckOffset(offset)
  File "/home/catherine/installed/google-cloud-sdk/platform/google_appengine/google/appengine/api/search/search.py", line 2895, in _CheckOffset
    upper_bound=MAXIMUM_SEARCH_OFFSET)
  File "/home/catherine/installed/google-cloud-sdk/platform/google_appengine/google/appengine/api/search/search.py", line 496, in _CheckInteger
    raise ValueError('%s, %d must be <= %d' % (name, value, upper_bound))
ValueError: offset, 2000 must be <= 1000
```

Darn. Because of these limitations, we're going to need a concept from Databases usually reserved for operations that span multiple computers: a cursor.

You can set as a parameter to the query options:

```python
        search_query = search.Query(
            query_string='',
            options=search.QueryOptions(
                limit=self.limit,
                sort_options=self.sort_opts,
                cursor=search.Cursor(per_result=False),
                ids_only=False,
            )
        )
```

you can access the cursor for this search query after getting the results:

```python
search_results = self.index.search(search_query)
cursor = search_results.cursor        
```

The strategy for pulling out the entries is this:

1. create a search with no offset and a new cursor
2. initialize current_offset to 0
3. while current_offset is less than the desired offset, query the search index again with the cursor of the last query, and add the limit to the current_offset
4. output the last search results

It would be nice if we could start our loop at the maximum offset in order to limit the number of repetitions of step 3, but if you do, you'll get the error:

```python
ValueError: cannot set cursor and offset together
```

Also, make sure that you set the **per_result** value of **search.Cursor** to **False**, or else the cursor will be None:

```python
  File "/home/catherine/python_projects/appengine-large-offset-example/main.py", line 109, in query_with_cursors
    cursor_cache[current_offset] = search_results.cursor.web_safe_string
AttributeError: 'NoneType' object has no attribute 'web_safe_string'
```

Here's the implementation:

```python
        current_offset = self.limit
        search_query = search.Query(query_string='',
            options=search.QueryOptions(
                limit=self.limit,
                sort_options=self.sort_opts,
                cursor=search.Cursor(per_result=False),
                ids_only=False,
            )
        )

        search_results = self.index.search(search_query)
        if self.offset >= search_results.number_found:
            return self.render_search_doc([])
        while current_offset < self.offset:
            current_offset += self.limit
            search_query = search.Query(query_string='',
                options=search.QueryOptions(
                    limit=self.limit,
                    sort_options=self.sort_opts,
                    cursor=search_results.cursor
                )
            )
            search_results = self.index.search(search_query)
        self.render_search_doc(search_results)
```

Now, if we're going to be querying an offset of up to 100000, it will take a while to do 1000 queries. So, it would be better if we could cache these cursors. We can stick the web_safe_string in memcache:

```python
        cursor_cache = {}
        current_offset = self.limit
        search_query = search.Query(query_string='',
            options=search.QueryOptions(
                limit=self.limit,
                sort_options=self.sort_opts,
                cursor=search.Cursor(per_result=False),
                ids_only=False,
            )
        )

        search_results = self.index.search(search_query)
        cursor_cache[current_offset] = search_results.cursor.web_safe_string
        if self.offset >= search_results.number_found:
            return self.render_search_doc([])
        while current_offset < self.offset:
            current_offset += self.limit
            search_query = search.Query(query_string='',
                options=search.QueryOptions(
                    limit=self.limit,
                    sort_options=self.sort_opts,
                    cursor=search_results.cursor
                )
            )
            search_results = self.index.search(search_query)
            cursor_cache[current_offset] = search_results.cursor.web_safe_string
        memcache.set(cursor_cache_key, json.dumps(cursor_cache))
        self.render_search_doc(search_results)
```

And then the next time, we can pull out the cursor for that offset:

```python
        cursor_cache_key = 'cursors'
        cursor_cache = memcache.get(cursor_cache_key)
        if cursor_cache:
            cursor_cache = json.loads(cursor_cache)
            offset_key = str(self.offset)
            if offset_key in cursor_cache:
                cursor_cache = cursor_cache[offset_key]
            else:
                logging.info("%s not in %s" %(offset_key, cursor_cache))
                cursor_cache = None

        if cursor_cache:
            logging.info("found cursor cache string %s " % cursor_cache)

            # construct the sort options
            search_query = search.Query(
                query_string='',
                options=search.QueryOptions(
                    limit=self.limit,
                    sort_options=self.sort_opts,
                    cursor=search.Cursor(per_result=False, web_safe_string=cursor_cache),
                    ids_only=False,
                )
            )
            return self.render_search_doc(self.index.search(search_query))
```

A next step would be to find the nearest cursor offset, and start from there. But that would be another blog post. 
