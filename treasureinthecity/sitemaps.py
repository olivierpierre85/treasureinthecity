from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    i18n = True
    def items(self):
        return [
            { 'page':'index','args':{}},
            { 'page':'city','args':{'brussels'}},
            { 'page':'city','args':{'paris'}}
        ]

    def location(self, item):
        return reverse(item['page'], args=item['args'])


