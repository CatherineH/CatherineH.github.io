---
layout: default
title: Catherine's Auxiliary Brain
tagline: Mostly Programming stuff
---
{% for post in site.posts %}
<div class="page-header">
  <h1>{{ post.title }} {% if post.tagline %}<small>{{post.tagline}}</small>{% endif %}</h1>
</div>

<div class="row post-full">
  <div class="col-xs-12">
    <div class="date">
      <span>{{ post.date | date_to_long_string }}</span>
    </div>
    <div class="content">
      {{ post.content }}
    </div>

  </div>
</div>
{% endfor %}