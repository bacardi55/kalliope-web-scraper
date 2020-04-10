# kalliope-web-scraper

A simple neuron for Kalliope to read part of web pages


## Synopsis

Make kalliope read information from any webside, as an example below from https://www.programme-tv.net web page to get the TV programm.
Quick note : if you want to ge the program for tomorrow, you will need a new URL. To build the new url you can use the example at the end of the description.

## Installation

  ```
  kalliope install --git-url https://github.com/DuduNord/kalliope-web-scraper.git
  ```


## Options

| parameter                  | required | default | choices | comment                                                                                         |
|----------------------------|----------|---------|---------|-------------------------------------------------------------------------------------------------|
| url                        | yes      |         |         | The url of the site to parse                                                                    |
| main_selector_tag          | yes      |         |         | The main selector html tag that shoud return a list of htmlelement                              |
| main_selector_class        | yes      |         |         | The main selector class that shoud return a list of htmlelement                                 |
| title_selector_tag         | yes      |         |         | The selector html tag for the title in each element of the main_selector                        |
| title_selector_class       | yes      |         |         | The selector class for the title in each element of the main_selector                           |
| title2_selector_tag        | yes      |         |         | The selector html tag for a 2nd title in each element of the main_selector                        |
| title2_selector_class      | yes      |         |         | The selector class for for a 2nd title in each element of the main_selector                           |
| content_selector_tag       | yes      |         |         | The selector html tag for the description/summary/teaser/… in each element of the main_selector |
| content_selector_class     | yes      |         |         | The selector class for the description/summary/teaser/… in each element of the main_selector    |
| detail_selector_tag        | yes      |         |         | The selector html tag for the second detail element in each element of the main_selector |
| detail_selector_class      | yes      |         |         | The selector class for the second detail element in each element of the main_selector    |


## Return Values

| Name         | Description                                                                           | Type     | sample   |
| ------------ | ------------------------------------------------------------------------------------- | -------- | -------- |
| returncode   | The http response code. If everything is ok, should be 200                            | string   |          |
| data         | List of item. Each news contains the title and content (new['title'] new['content']   | list     |          |


## Synapses example

This synapse will find read all "main" news on news.google.com
```
---
  - name: "Programme-tv"
    signals:
      - order: "What's on TV tonight"
    neurons:
      - web_scraper:
          url: "https://www.programme-tv.net/programme/sfr-25/en-ce-moment.html"
          main_selector_tag: "div"
          main_selector_class: "doubleBroadcastCard"
          title_selector_tag: "a"
          title_selector_class: "doubleBroadcastCard-channelName"
          title2_selector_tag: "div"
          title2_selector_class: "doubleBroadcastCard-channelNumber"
          # detail_selector_tag: "div"                    # optional info to get the hour of the programm
          # detail_selector_class: "doubleBroadcastCard-hour"
          content_selector_tag: "a"
          content_selector_class: "doubleBroadcastCard-title"
          file_template: "templates/programme_tv_enfant.j2"

  - name: "Programme-tv-tomorrow"
    signals:
      - order: "What's on TV tomorrow"
    neurons:
      - shell:
        cmd: "python3 gettomorowlink.py"
        kalliope_memory:
          tomorrowlink: "{{ output }}"
      - web_scraper:
          url: "{{ kalliope_memory['tomorrowlink'] }}"
          main_selector_tag: "div"
          main_selector_class: "doubleBroadcastCard"
          title_selector_tag: "a"
          title_selector_class: "doubleBroadcastCard-channelName"
          title2_selector_tag: "div"
          title2_selector_class: "doubleBroadcastCard-channelNumber"
          # detail_selector_tag: "div"                    # optional info to get the hour of the programm
          # detail_selector_class: "doubleBroadcastCard-hour"
          content_selector_tag: "a"
          content_selector_class: "doubleBroadcastCard-title"
          file_template: "templates/programme_tv_enfant.j2"
```

## Py file example to load into the starter kit folder (make sure to make it executable with CHMOD)

```
import datetime
from datetime import timedelta

date_object = datetime.date.today() + datetime.timedelta(days=1)
print("https://www.programme-tv.net/programme/sfr-25/"+date_object.strftime("%Y-%m-%d")+"/",end='')
```

## Template example

```
{% set myFav = [    "Chaîne n°14",
                    "Chaîne n°18",
                    "Chaîne n°200",
                    "Chaîne n°201",
                    "Chaîne n°203",
                    "Chaîne n°205",
                    "Chaîne n°210",
                    "Chaîne n°213"
                    ] %}

{% if returncode != 200 %}
    Erreur à la lecture de la page.
{% else %}
    {% for g in data: -%} 
        {% if g['title2'] in myFav %} Sur {{ g['title'] }}, {{ g['content'] }}. {% endif %}  
        {# can also add here the hour with g['detail'] #}
    {%- endfor %}
{% endif %}
```



* [a blog about this neuron](http://bacardi55.org/2017/01/13/web-scrapping-kalliope-neuron.html)
* [my posts about kalliope](http://bacardi55.org/kalliope.html)
