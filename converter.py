from pydantic import BaseModel
from urllib.parse import urlencode


class VMessQRCode(BaseModel):
    v: int
    ps: str = ''
    add: str
    port: int
    id: str
    aid: str = ''
    scy: str = ''
    net: str = ''
    type: str = ''
    host: str = ''
    path: str = ''
    tls: str = ''
    sni: str = ''
    alpn: str = ''
    fp: str = ''


QR_TO_AEAD_PARAMS = {
    'scy': 'encryption',
    'tls': 'security',
    'net': 'type',
    'sni': 'sni',
    'alpn': 'alpn',
    'fp': 'fp',
    'host': 'host',
    'type': 'headerType',
    'path': 'path'
}


def convert_params(vmess_qr_code: VMessQRCode) -> dict:
    params = {}
    for key, val in vmess_qr_code.dict().items():
        if val and key in QR_TO_AEAD_PARAMS:
            converted_param = QR_TO_AEAD_PARAMS[key]
            params[converted_param] = val
    return params


def convert_link(vmess_qr_code: VMessQRCode) -> str:
    query_params = urlencode(convert_params(vmess_qr_code), safe='/,')
    return f'vmess://{vmess_qr_code.id}@{vmess_qr_code.add}:{vmess_qr_code.port}?' \
           f'{query_params}#{vmess_qr_code.ps}'

