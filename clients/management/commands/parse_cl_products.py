from os import path
from pathlib import Path
import re

from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from requests_html import HTMLSession

from clients.models import (
    CLCategory,
    CLProduct,
)
from proj_dating.settings import (
    BASE_DIR,
    MEDIA_ROOT,
    MEDIA_CLPRODUCTS_DIR,
)

BASE_URL = 'https://www.citilink.ru/'

class Command(BaseCommand):
    help = 'parses top100 citilink products'

    def handle(self, *args, **options):
        sess = HTMLSession()
        resp = sess.get(BASE_URL + 'top100/')
        soup = BeautifulSoup(resp.text, 'lxml')

        quant_downloaded = 0

        for product_card in soup.find_all(class_='ProductCardVerticalLayout'):
            p_price = int(product_card.find(class_='ProductCardVerticalPrice__price-current_current-price').text.strip().replace(' ', ''))
            p_link = BASE_URL[0:-1] + product_card.find(class_='ProductCardVertical__name')['href']

            p_resp = sess.get(p_link)
            p_soup = BeautifulSoup(p_resp.text, 'lxml')

            try:
                p_name = p_soup.find(class_='ProductHeader__title').text.strip()
                p_image_link = p_soup.find(class_='PreviewList__image')['src']
            except AttributeError as e:
                self.stdout.write(self.style.ERROR(f"didn't download data for {p_link}. probably some error at the site."))
                continue

            p_image_name = re.search(r'[^\/]+$', p_image_link)[0]
            pathtofile = Path.joinpath(BASE_DIR, MEDIA_ROOT, MEDIA_CLPRODUCTS_DIR, p_image_name)
            with open(pathtofile, 'wb') as file:
                img_resp = sess.get(p_image_link)
                file.write(img_resp.content)

            # creating category and subcategories if they weren't created yet
            categories = p_soup.find_all(class_='Breadcrumbs')
            c_parent = None
            for category in categories:
                c_name = category['data-breadcrumb-name'].strip()
                c_link = category.a['href']
                
                category_obj = CLCategory.objects.filter(link=c_link).first()
                if not category_obj:
                    category_attrs = {
                        'parent_category': c_parent,
                        'name': c_name,
                        'link': c_link,
                    }
                    new_category = CLCategory.objects.create(**category_attrs)

                    self.stdout.write(self.style.SUCCESS(f'successfully created the category #{new_category.id}: {new_category.name}'))

                    c_parent = new_category
                else:
                    c_parent = category_obj

            # creating product or updating it
            product_attrs = {
                'name': p_name,
                'price': p_price,
                'link': p_link,
                'picture': path.join(MEDIA_CLPRODUCTS_DIR, p_image_name),
                'category': c_parent,
            }
            product_q = CLProduct.objects.filter(link=p_link)
            if product_q:
                product_q.update(**product_attrs)
                product_obj = product_q.first()
                self.stdout.write(self.style.SUCCESS(f'successfully updated the product #{product_obj.id}: {product_obj.name}'))
            else:
                product_obj = CLProduct.objects.create(**product_attrs)
                self.stdout.write(self.style.SUCCESS(f'successfully created the product #{product_obj.id}: {product_obj.name}'))

            quant_downloaded += 1

        print(quant_downloaded)
