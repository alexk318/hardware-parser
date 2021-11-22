import ast


def find_product_data_shop(item):
    product_data = {

        'image_url': 'https:' + item.find('div', class_='bx_catalog_item_container gtm-impression-product'
                                          ).find('figure', class_='item_image_container').find('a')['style']
        [23:-2],

        'title': ast.literal_eval(
            item.find('div', class_='bx_catalog_item_container gtm-impression-product')['data-product'])[
            'name'],

        'description': '',

        'cost': ast.literal_eval(
            item.find('div', class_='bx_catalog_item_container gtm-impression-product')['data-product'])[
            'price'],

        'url': 'https://shop.kz' + item.find('div',
                                             class_='bx_catalog_item_container gtm-impression-product').find
        ('div', class_='bx-catalog-middle-part').find('div', class_='bx_catalog_item_title').find('a')
        ['href']

    }

    description_spans = item.find('div',
                                  class_='bx_catalog_item_container gtm-impression-product').find_all(
        'span')

    for description_span in description_spans:
        product_data['description'] = product_data['description'] + description_span.get_text() + ' '

    product_data['description'] = product_data['description'][:100] + ' ...'

    return product_data


def find_product_data_forcecom(item):
    product_data = {

        'image_url': 'https://' + 'forcecom.kz' + item.find('table').find('tr', class_='').find
        ('td', class_='image_block').find('div', class_='image_wrapper_block').find('a').find('img')['src'],

        'title': item.find('table').find('tr', class_='').find('td', class_='description_wrapp').find(
            'div', class_='description').find('div', class_='item-title').find('a').find('span').get_text(),

        'description': None,

        'cost': None,

        'url': 'https://forcecom.kz' + item.find('table').find('tr', class_='').find
        ('td', class_='image_block').find('div', class_='image_wrapper_block').find('a')['href']

    }

    try:
        d = item.find('table').find('tr', class_='').find('td', class_='description_wrapp').find(
            'div', class_='description').find('div', class_='preview_text').get_text()

        product_data['description'] = d[1:-1]  # d[0]
    except AttributeError:
        pass

    try:
        product_data['cost'] = int(item.find('table').find('tr', class_='').find
                                   ('td', class_='information_wrapp main_item_wrapper').find
                                   ('div', class_='information').find('div', class_='cost prices clearfix').find
                                   ('div', class_='price_group 1497a90b-3ddf-11e6-89ef-ac9e1788bb3d').find
                                   ('div', class_='price_matrix_wrapper').find('div', class_='price')
                                   ['data-value'])

    except AttributeError:
        pass

    return product_data


def find_product_data_tomas(item):
    product_data = {

        'image_url': None,

        'title': None,

        'description': None,

        'cost': None,

        'url': None,

    }

    try:
        product_data['image_url'] = 'https:' + item.find('div', class_='goods__img-row').find('a').find('span').find(
            'img')['src']
        product_data['title'] = item.find('div', class_='goods__img-row').find('a')['title']
        product_data['cost'] = item.find('div', class_='goods__price-row').find('span').find('div').find('div').\
            get_text()
        product_data['url'] = item.find('div', class_='goods__img-row').find('a')['href']
    except AttributeError:
        pass

    if product_data['cost'] is not None:
        product_data['cost'] = product_data['cost'].replace(" ", "")
        product_data['cost'] = product_data['cost'].replace('тг', '')
        product_data['cost'] = product_data['cost'].replace(',', '.')

        product_data['cost'] = int(float(product_data['cost']))

    return product_data
