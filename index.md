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
      {{ content }}
    </div>

  {% unless post.categories == empty %}
    <ul class="tag_box inline">
      <li><i class="glyphicon glyphicon-open"></i></li>
      {% assign categories_list = post.categories %}
      {% include JB/categories_list %}
    </ul>
  {% endunless %}

  {% unless post.tags == empty %}
    <ul class="tag_box inline">
      <li><i class="glyphicon glyphicon-tags"></i></li>
      {% assign tags_list = post.tags %}
      {% include JB/tags_list %}
    </ul>
  {% endunless %}

  </div>
</div>
{% endfor %}