# -*- coding: utf-8 -*-

from odoo import http
from odoo.addons import website_sale
from odoo.http import request


class WebsiteSaleWarnMessage(website_sale.controllers.main.WebsiteSale):

    @http.route(['/shop/product/<model("product.template"):product>'], type='http', auth="public", website=True)
    def product(self, product, category='', search='', **kwargs):
        '''
        Saving the url before entered a product page

        '''

        prev_url = (
            request.httprequest.referrer
            if request.httprequest.referrer
            else ''
        )

        request.session['last_shop_page'] = prev_url

        return super(WebsiteSaleWarnMessage, self).product(
            product=product,
            category=category,
            search=search,
            kwargs=kwargs
        )

    @http.route(['/shop/cart'], type='http', auth="public", website=True, sitemap=False)
    def cart(self, access_token=None, revive='', **post):

        '''
        In case the product is added from somewhere else than the product
        page,the previous shop page will be saved to be able to return to it.
        '''
        prev_url = request.httprequest.referrer or ''

        # Check if previous page was a product page. If NOT save it as the
        # previous shop page to return to
        if '/shop/product/' not in prev_url:
            request.session['last_shop_page'] = prev_url

        return super(WebsiteSaleWarnMessage, self).cart(
            access_token=access_token,
            revive=revive,
            post=post
        )

    @http.route(['/last_shop_page'], type='http', auth="public", website=True)
    def last_shop_page(self, **post):
        '''
        :return: Redirects the user to the last visited shop page if
        available, otherwise to the shop main page.
        '''
        last_shop_page = request.session.pop('last_shop_page', '/shop')
        if 'payment' in last_shop_page:
            last_shop_page = request.session.pop('last_shop_page', '/shop')

        return request.redirect(last_shop_page)
