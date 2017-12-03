import requests

from pynformatics.model.user_oauth_provider import UserOAuthProvider
from pynformatics.models import DBSession
from pynformatics.utils.exceptions import (
    AuthOAuthBadProvider,
    AuthOAuthUserNotFound,
)


OAUTH_CONFIG = {
    'vk': {
        'url': 'https://oauth.vk.com/access_token'
               '?client_id=%(client_id)s'
               '&client_secret=%(client_secret)s'
               '&redirect_uri=%(redirect_uri)s'
               '&code=%(code)s',
        'method': 'get',
        'client_id': '6279574',
        'client_secret': None,
        'redirect_uri': 'https://informatics.msk.ru/frontend/login',
        'oauth_id_key': 'user_id',
    },
    'google': {
        'url': 'https://www.googleapis.com/oauth2/v4/token',
        'url_profile': 'https://www.googleapis.com/oauth2/v1/userinfo?access_token=%(access_token)s',
        'method': 'post',
        'fields': [
            'client_id',
            'client_secret',
            'redirect_uri',
            'grant_type',
        ],
        'client_id': '629729803861-vilqpepmi33rdd5jtguq9cv0aifseera.apps.googleusercontent.com',
        'client_secret': None,
        'redirect_uri': 'https://informatics.msk.ru/frontend/login',
        'grant_type': 'authorization_code',
        'oauth_id_key': 'id',
    },
}


def fill_oauth_config_secrets(settings):
    """
    Заполняет пропущенные значения в OAUTH_CONFIG, значениями из настроек
    """
    for provider in OAUTH_CONFIG:
        for (key, value) in OAUTH_CONFIG[provider].items():
            if not value:
                OAUTH_CONFIG[provider][key] = settings.get('oauth.%s.%s' % (provider, key))


def get_oauth_id(provider, code):
    if provider not in OAUTH_CONFIG:
        raise AuthOAuthBadProvider
    provider_config = OAUTH_CONFIG[provider]

    # В зависимости от method отправляем GET/POST запрос на сервер провайдера
    if provider_config['method'] == 'get':
        url = provider_config['url'] % {**provider_config, 'code': code}
        response = requests.get(url)
    else:
        data = {
            field: provider_config[field]
            for field in provider_config['fields']
        }
        data['code'] = code
        response = requests.post(provider_config['url'], data=data)

    # Если в настройках провайдера указан дополнительный url для получения информации о пользователе,
    # нужно отправить GET запрос с параметром access_token, который получен из предыдущего запроса
    if 'url_profile' in provider_config:
        response = requests.get(provider_config['url_profile'] % response.json())

    oauth_id = response.json().get(provider_config['oauth_id_key'])
    return oauth_id
