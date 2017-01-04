import logging
import requests

from xextract import String, Group
from kalliope.core.NeuronModule import NeuronModule, InvalidParameterException

logging.basicConfig()
logger = logging.getLogger("kalliope")

class Web_scraper (NeuronModule):
    def __init__(self, **kwargs):
        # we don't need the TTS cache for this neuron
        cache = kwargs.get('cache', None)
        if cache is None:
            cache = False
            kwargs["cache"] = cache
        super(Web_scraper, self).__init__(**kwargs)

        # get parameters form the neuron
        self.configuration = {
            "url": kwargs.get('url', None),
            "main_selector": kwargs.get('main_selector', None),
            "title_selector": kwargs.get('title_selector', None),
            "description_selector": kwargs.get('description_selector', None)
        }

        # check parameters
        if self._is_parameters_ok():
            self.infos = {
                "news": [],
                "returncode": None
            }

            try:
                r = requests.get(self.configuration['url'])
                news = Group(css=self.configuration['main_selector'], children=[
                    String(name="title", css=self.configuration['title_selector'], attr='_all_text', quant=1),
                    String(name="teaser", css=self.configuration['description_selector'], attr='_all_text', quant=1)
                ]).parse(r.text)

                self.infos['returncode'] = r.status_code

                for new in news:
                    self.infos['news'].append({
                        'title': unicode(new['title']),
                        'content': unicode(new['teaser'])
                    })

            except requests.exceptions.HTTPError:
                self.infos['returncode'] = "HTTPError"

            logger.debug("Web scraper return : %s" % len(self.infos))

            self.say(self.infos)

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise
        .. raises:: InvalidParameterException
        """

        if self.configuration['url'] is None:
            raise InvalidParameterException("Web scraper needs a url")

        if self.configuration['main_selector'] is None:
            raise InvalidParameterException("Web scraper needs a main_selector")

        if self.configuration['title_selector'] is None:
            raise InvalidParameterException("Web scraper needs a title_selector")

        if self.configuration['description_selector'] is None:
            raise InvalidParameterException("Web scraper needs a description_selector")

        return True
