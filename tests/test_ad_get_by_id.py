import pytest

from application import crud, dto


def test_get_ad_success(client, test_db, ad_sample_input):
    ad = crud.save_ad(test_db, dto.AdIn(**ad_sample_input))

    response = client.get(f'/ad/{ad.id}/')

    assert response.status_code == 200

    data = response.json()
    assert data['id'] == ad.id
    assert data['name'] == ad_sample_input['name']
    assert data['price'] == ad_sample_input['price']
    assert data['main_photo'] == ad_sample_input['photos'][0]


def test_get_ad_with_description_success(client, test_db, ad_sample_input):
    ad = crud.save_ad(test_db, dto.AdIn(**ad_sample_input))

    response = client.get(f'/ad/{ad.id}/', params={'fields': ['description']})

    assert response.status_code == 200

    data = response.json()
    assert data['id'] == ad.id
    assert data['name'] == ad_sample_input['name']
    assert data['description'] == ad_sample_input['description']
    assert data['price'] == ad_sample_input['price']
    assert data['main_photo'] == ad_sample_input['photos'][0]


def test_get_ad_with_photos_success(client, test_db, ad_sample_input):
    ad = crud.save_ad(test_db, dto.AdIn(**ad_sample_input))

    response = client.get(f'/ad/{ad.id}/', params={'fields': ['photos']})

    assert response.status_code == 200

    data = response.json()
    assert data['id'] == ad.id
    assert data['name'] == ad_sample_input['name']
    assert data['price'] == ad_sample_input['price']
    assert data['main_photo'] == ad_sample_input['photos'][0]
    assert data['photos'] == ad_sample_input['photos']


def test_get_ad_with_description_and_photos_success(client, test_db, ad_sample_input):
    ad = crud.save_ad(test_db, dto.AdIn(**ad_sample_input))

    response = client.get(f'/ad/{ad.id}/', params={'fields': ['photos', 'description']})

    assert response.status_code == 200

    data = response.json()
    assert data['id'] == ad.id
    assert data['name'] == ad_sample_input['name']
    assert data['description'] == ad_sample_input['description']
    assert data['price'] == ad_sample_input['price']
    assert data['main_photo'] == ad_sample_input['photos'][0]
    assert data['photos'] == ad_sample_input['photos']


def test_get_ad_with_unknown_field_success(client, test_db, ad_sample_input):
    ad_id = crud.save_ad(test_db, dto.AdIn(**ad_sample_input))

    response = client.get(f'/ad/{ad_id}/', params={'fields': ['unknown']})

    assert response.status_code == 422


def test_get_ad_not_found(client, test_db):
    response = client.get('/ad/1/')

    assert response.status_code == 404
    assert response.json() == {'detail': 'NOT_FOUND'}
