import datetime

import pytest

from application import crud, dto
from application.database.models import Ad, Photo


@pytest.fixture
def ads_small_input():
    return [{
        'name': f'Ad #{i}',
        'description': f'Ad #{i} description',
        'price': price,
        'photos': [
            {
                'url': 'http://example.com/1.jpg'
            },
            {
                'url': 'http://example.com/2.jpg'
            }
        ]
    } for i, price in zip(range(1, 4), (200, 100, 100))] # 1..3


@pytest.fixture
def ads_large_input():
    return [{
        'name': f'Ad #{i}',
        'description': f'Ad #{i} description',
        'price': i * 100,
        'photos': [
            {
                'url': 'http://example.com/1.jpg'
            }
        ]
    } for i in range(1, 21)] # 1..20


@pytest.fixture
def page():
    return 1


@pytest.fixture
def offset(page):
    crud.PAGE_SIZE * (page - 1)


def test_get_ads_empty_db(client, test_db):
    response = client.get('/ad/')

    assert response.status_code == 200
    assert response.json() == []


def test_get_ads_price_asc(client, test_db, ads_small_input, page, offset):
    ids = [crud.save_ad(test_db, dto.AdIn(**ad)) for ad in ads_small_input]

    for i, ad_id in enumerate(ids):
        ad = crud.get_ad_by_id(test_db, ad_id)
        ad.date = datetime.datetime(2021, 1, 1, 0, 0, i)
        test_db.add(ad)
        test_db.commit()

    response = client.get('/ad/', params={
        'page': page,
        'price_order': crud.SortOrder.ASC
    })

    assert response.status_code == 200

    actual = [ad['id'] for ad in response.json()]
    expected = [
        ad.id for ad in test_db.query(Ad)
            .order_by(Ad.price.asc())
            .join(Photo).offset(offset)
            .limit(crud.PAGE_SIZE)
    ]

    assert actual == expected


def test_get_ads_price_desc(client, test_db, ads_small_input, page, offset):
    ids = [crud.save_ad(test_db, dto.AdIn(**ad)) for ad in ads_small_input]

    for i, ad_id in enumerate(ids):
        ad = crud.get_ad_by_id(test_db, ad_id)
        ad.date = datetime.datetime(2021, 1, 1, 0, 0, i)
        test_db.add(ad)
        test_db.commit()

    response = client.get('/ad/', params={
        'page': page,
        'price_order': crud.SortOrder.DESC
    })

    assert response.status_code == 200

    actual = [ad['id'] for ad in response.json()]
    expected = [
        ad.id for ad in test_db.query(Ad)
            .order_by(Ad.price.desc())
            .join(Photo).offset(offset)
            .limit(crud.PAGE_SIZE)
    ]

    assert actual == expected


def test_get_ads_date_asc(client, test_db, ads_small_input, page, offset):
    ids = [crud.save_ad(test_db, dto.AdIn(**ad)) for ad in ads_small_input]

    for i, ad_id in enumerate(ids):
        ad = crud.get_ad_by_id(test_db, ad_id)
        ad.date = datetime.datetime(2021, 1, 1, 0, 0, i)
        test_db.add(ad)
        test_db.commit()

    response = client.get('/ad/', params={
        'page': page,
        'date_order': crud.SortOrder.ASC
    })

    assert response.status_code == 200

    actual = [ad['id'] for ad in response.json()]
    expected = [
        ad.id for ad in test_db.query(Ad)
            .order_by(Ad.date.asc())
            .join(Photo).offset(offset)
            .limit(crud.PAGE_SIZE)
    ]

    assert actual == expected


def test_get_ads_date_desc(client, test_db, ads_small_input, page, offset):
    ids = [crud.save_ad(test_db, dto.AdIn(**ad)) for ad in ads_small_input]

    for i, ad_id in enumerate(ids):
        ad = crud.get_ad_by_id(test_db, ad_id)
        ad.date = datetime.datetime(2021, 1, 1, 0, 0, i)
        test_db.add(ad)
        test_db.commit()

    response = client.get('/ad/', params={
        'page': page,
        'date_order': crud.SortOrder.DESC
    })

    assert response.status_code == 200

    actual = [ad['id'] for ad in response.json()]
    expected = [
        ad.id for ad in test_db.query(Ad)
            .order_by(Ad.date.desc())
            .join(Photo).offset(offset)
            .limit(crud.PAGE_SIZE)
    ]

    assert actual == expected


def test_get_ads_date_asc_price_asc(client, test_db, ads_small_input, page, offset):
    ids = [crud.save_ad(test_db, dto.AdIn(**ad)) for ad in ads_small_input]

    for i, ad_id in enumerate(ids):
        ad = crud.get_ad_by_id(test_db, ad_id)
        ad.date = datetime.datetime(2021, 1, 1, 0, 0, i)
        test_db.add(ad)
        test_db.commit()

    response = client.get('/ad/', params={
        'page': page,
        'date_order': crud.SortOrder.ASC,
        'price_order': crud.SortOrder.ASC
    })

    assert response.status_code == 200

    actual = [ad['id'] for ad in response.json()]
    expected = [
        ad.id for ad in test_db.query(Ad)
            .order_by(Ad.date.asc(), Ad.price.asc())
            .join(Photo).offset(offset)
            .limit(crud.PAGE_SIZE)
    ]

    assert actual == expected


def test_get_ads_date_desc_price_desc(client, test_db, ads_small_input, page, offset):
    ids = [crud.save_ad(test_db, dto.AdIn(**ad)) for ad in ads_small_input]

    for i, ad_id in enumerate(ids):
        ad = crud.get_ad_by_id(test_db, ad_id)
        ad.date = datetime.datetime(2021, 1, 1, 0, 0, i)
        test_db.add(ad)
        test_db.commit()

    response = client.get('/ad/', params={
        'page': page,
        'date_order': crud.SortOrder.DESC,
        'price_order': crud.SortOrder.DESC
    })

    assert response.status_code == 200

    actual = [ad['id'] for ad in response.json()]
    expected = [
        ad.id for ad in test_db.query(Ad)
            .order_by(Ad.date.desc(), Ad.price.desc())
            .join(Photo).offset(offset)
            .limit(crud.PAGE_SIZE)
    ]

    assert actual == expected


def test_get_ads_pagination(client, test_db, ads_large_input):
    page = 1
    ids = [crud.save_ad(test_db, dto.AdIn(**ad)) for ad in ads_large_input]

    for i, ad_id in enumerate(ids):
        ad = crud.get_ad_by_id(test_db, ad_id)
        ad.date = datetime.datetime(2021, 1, 1, 0, 0, i)
        test_db.add(ad)
        test_db.commit()

    response = client.get('/ad/', params={
        'page': page,
        'date_order': crud.SortOrder.ASC
    })

    assert response.status_code == 200

    actual = [ad['id'] for ad in response.json()]
    expected = [
        ad.id for ad in test_db.query(Ad)
            .order_by(Ad.date.asc())
            .join(Photo).offset(crud.PAGE_SIZE * (page - 1))
            .limit(crud.PAGE_SIZE)
    ]

    assert actual == expected


def test_get_ads_pagination_out_of_range(client, test_db, ads_large_input):
    page = len(ads_large_input) // crud.PAGE_SIZE + 2 # the page after the last non-empty page
    ids = [crud.save_ad(test_db, dto.AdIn(**ad)) for ad in ads_large_input]

    for i, ad_id in enumerate(ids):
        ad = crud.get_ad_by_id(test_db, ad_id)
        ad.date = datetime.datetime(2021, 1, 1, 0, 0, i)
        test_db.add(ad)
        test_db.commit()

    response = client.get('/ad/', params={
        'page': page,
        'date_order': crud.SortOrder.ASC
    })

    assert response.status_code == 200

    actual = [ad['id'] for ad in response.json()]
    expected = []

    assert actual == expected


def test_get_ads_pagination_negative_page_number(client, test_db, ads_large_input):
    page = -1
    ids = [crud.save_ad(test_db, dto.AdIn(**ad)) for ad in ads_large_input]

    for i, ad_id in enumerate(ids):
        ad = crud.get_ad_by_id(test_db, ad_id)
        ad.date = datetime.datetime(2021, 1, 1, 0, 0, i)
        test_db.add(ad)
        test_db.commit()

    response = client.get('/ad/', params={
        'page': page,
        'date_order': crud.SortOrder.ASC
    })

    assert response.status_code == 422
