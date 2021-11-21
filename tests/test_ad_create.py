import pytest

from application import crud, dto
from application.database.models import Ad, Photo


@pytest.fixture
def ad_sample_input():
    return {
        'name': "Ad's name",
        'description': "Ad's description",
        'price': 100,
        'photos': [
            {
                'url': 'http://example.com/1.jpg'
            },
            {
                'url': 'http://example.com/2.jpg'
            }
        ]
    }


def test_ad_create_success(client, test_db, ad_sample_input):
    response = client.post('/ad/', json=ad_sample_input)

    assert response.status_code == 201

    data = response.json()
    assert 'id' in data

    ad = crud.get_ad_by_id(test_db, data['id'])
    assert ad.name == ad_sample_input['name']
    assert ad.description == ad_sample_input['description']
    assert ad.price == ad_sample_input['price']
    assert all(
        photo.url == input_photo['url']
        for photo, input_photo in zip(ad.photos, ad_sample_input['photos'])
    )


@pytest.mark.parametrize('field', ['name', 'description', 'price', 'photos'])
def test_ad_create_without_required_field(client, ad_sample_input, field):
    input_data = {**ad_sample_input}
    del input_data[field]
    response = client.post('/ad/', json=input_data)

    assert response.status_code == 422


@pytest.mark.parametrize('name', [None, '', 'N' * 4, 'N' * 201])
def test_ad_create_invalid_name(client, ad_sample_input, name):
    response = client.post('/ad/', json={**ad_sample_input, 'name': name})

    assert response.status_code == 422


@pytest.mark.parametrize('description', [None, '', 'N' * 9, 'N' * 2001])
def test_ad_create_invalid_description(client, ad_sample_input, description):
    response = client.post('/ad/', json={**ad_sample_input, 'description': description})

    assert response.status_code == 422


@pytest.mark.parametrize('price', [None, 0, 0.99, 10_000_000.00])
def test_ad_create_invalid_price(client, ad_sample_input, price):
    response = client.post('/ad/', json={**ad_sample_input, 'price': price})

    assert response.status_code == 422


@pytest.mark.parametrize('photos', [
    [],
    [{}, {}],
    [
        {
            'url': 'invalid_url'
        },
        {
            'url': 'http://example.com/1.jpg'
        }
    ],
    [
        {
            'url': 'http://example.com/1.jpg'
        },
        {
            'url': 'http://example.com/2.jpg'
        },
        {
            'url': 'http://example.com/3.jpg'
        },
        {
            'url': 'http://example.com/4.jpg'
        }
    ]
])
def test_ad_create_invalid_photos(client, ad_sample_input, photos):
    response = client.post('/ad/', json={**ad_sample_input, 'photos': photos})

    assert response.status_code == 422
