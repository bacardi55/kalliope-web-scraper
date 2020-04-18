import logging
import requests

from bs4 import BeautifulSoup
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
        self.url = kwargs.get('url', None)
        self.main_selector_tag = kwargs.get('main_selector_tag', None)
        self.main_selector_class = kwargs.get('main_selector_class', None)
        self.title_selector_tag = kwargs.get('title_selector_tag', None)
        self.title_selector_class = kwargs.get('title_selector_class', None)
        self.title2_selector_tag = kwargs.get('title2_selector_tag', None)
        self.title2_selector_class = kwargs.get('title2_selector_class', None)
        self.content_selector_tag = kwargs.get('content_selector_tag', None)
        self.content_selector_class = kwargs.get('content_selector_class', None)
        self.detail_selector_tag = kwargs.get('detail_selector_tag', None)
        self.detail_selector_class = kwargs.get('detail_selector_class', None)
        # self.dual_content = kwargs.get('dual_content', False)
        
        # check parameters
        if self._is_parameters_ok():
            title2bool = True # if either tag or class is not defined, then set the variable as false
            if self.title2_selector_tag is None:
                title2bool = False
            if self.title2_selector_class is None:
                title2bool = False
            descr2bool = True # if either tag or class is not defined, then set the variable as false
            if self.detail_selector_tag is None:
                descr2bool = False
            if self.detail_selector_class is None:
                descr2bool = False

            self.infos = {
                "data": [],
                "returncode": None
            }

            try:
                r = requests.get(self.url)
                self.infos['returncode'] = r.status_code

                soup = BeautifulSoup(r.text, 'html.parser')
                if title2bool:
                    if descr2bool:
                        for selector in soup.find_all(self.main_selector_tag,
                                                    class_=self.main_selector_class):
                            self.infos['data'].append({                                             # channel name
                                'title': selector.find(
                                    self.title_selector_tag,
                                    class_=self.title_selector_class).get_text().strip(),
                                'title2': selector.find(
                                    self.title2_selector_tag,
                                    class_=self.title2_selector_class).get_text().strip(),
                                'content': selector.find(
                                    self.content_selector_tag,
                                    class_=self.content_selector_class).get_text().strip(),
                                'detail': selector.find(
                                    self.detail_selector_tag,
                                    class_=self.detail_selector_class).get_text().strip()})
                    else:
                        for selector in soup.find_all(self.main_selector_tag,
                                                    class_=self.main_selector_class):
                            self.infos['data'].append({                                             # channel name
                                'title': selector.find(
                                    self.title_selector_tag,
                                    class_=self.title_selector_class).get_text().strip(),
                                'title2': selector.find(
                                    self.title2_selector_tag,
                                    class_=self.title2_selector_class).get_text().strip(),
                                'content': selector.find(
                                    self.content_selector_tag,
                                    class_=self.content_selector_class).get_text().strip()})
                else:
                    if descr2bool:
                        for selector in soup.find_all(self.main_selector_tag,
                                                    class_=self.main_selector_class):
                            self.infos['data'].append({                                             # channel name
                                'title': selector.find(
                                    self.title_selector_tag,
                                    class_=self.title_selector_class).get_text().strip(),
                                'content': selector.find(
                                    self.content_selector_tag,
                                    class_=self.content_selector_class).get_text().strip(),
                                'detail': selector.find(
                                    self.detail_selector_tag,
                                    class_=self.detail_selector_class).get_text().strip()})
                    else:
                        for selector in soup.find_all(self.main_selector_tag,
                                                    class_=self.main_selector_class):
                            self.infos['data'].append({                                             # channel name
                                'title': selector.find(
                                    self.title_selector_tag,
                                    class_=self.title_selector_class).get_text().strip(),
                                'content': selector.find(
                                    self.content_selector_tag,
                                    class_=self.content_selector_class).get_text().strip()})

            except requests.exceptions.HTTPError:
                print("exception") 
                self.infos['returncode'] = "HTTPError"

            logger.debug("Web scraper return : %s" % len(self.infos))

            self.say(self.infos)

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise
        .. raises:: InvalidParameterException
        """

        if self.url is None:
            raise InvalidParameterException("Web scraper needs a url")

        if self.main_selector_tag is None:
            raise InvalidParameterException(
                "Web scraper needs a main_selector tag")

        if self.main_selector_class is None:
            raise InvalidParameterException(
                "Web scraper needs a main_selector class")

        if self.title_selector_tag is None:
            raise InvalidParameterException(
                "Web scraper needs a title_selector tag")

        if self.title_selector_class is None:
            raise InvalidParameterException(
                "Web scraper needs a title_selector class")

        if self.content_selector_tag is None:
            raise InvalidParameterException(
                "Web scraper needs a content_selector tag")

        if self.content_selector_class is None:
            raise InvalidParameterException(
                "Web scraper needs a content_selector class")

        return True
