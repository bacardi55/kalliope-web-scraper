# kalliope-web-scraper

A simple neuron for Kalliope to read part of web pages


## Synopsis

Make kalliope read information from any web page

## Installation

  ```
  kalliope install --git-url git@github.com:bacardi55/kalliope-web-scraper.git
  ```


## Options

| parameter            | required | default | choices | comment                                                                                    |
|----------------------|----------|---------|---------|--------------------------------------------------------------------------------------------|
| url                  | yes      |         |         | The url of the site to parse                                                               |
| main_selector        | yes      |         |         | The main selector that shoud return a list of htmlelement (each one being a news)          |
| title_selector       | yes      |         |         | The selector for the the title in each element of the main_selector                        |
| description_selector | yes      |         |         | The selector for the the description/summary/teaser/… in each element of the main_selector |
| file_template        | yes      |         |         | Template file to use                                                                       |


## Return Values

| Name         | Description                                                                           | Type     | sample   |
| ------------ | ------------------------------------------------------------------------------------- | -------- | -------- |
| returncode   | The http response code. If everything is ok, should be 200                            | string   |          |
| items        | List of item. Each news contains the title and content (new['title'] new['content']   | list     |          |


## Synapses example

This synapse will find read all "main" news on news.google.com
```
---
  - name: "Google-news-en"
    signals:
      - order: "what are the latest news"
    neurons:
      - say:
          message: "Searching latest news Sir"
      - web_scraper:
          url: "https://news.google.com"
          main_selector: "div.top-stories-section div.section-content div.story"
          title_selector: "h2.esc-lead-article-title > a > span"
          description_selector: "div.esc-lead-snippet-wrapper"
          file_template: "templates/en_web_scraper.j2"
```

## Template example

```
{% if returncode != 200 %}
    Error while retrieving web page.
{% else %}
    {% for g in news: %}
        Title: {{ g['title'] }}
        Summary: {{ g['content'] }}
    {% endfor %}
{% endif %}
```




* [my posts about kalliope](https://bacardi55.org/en/blog/2017/kalliope-neuron-google-calendar)
