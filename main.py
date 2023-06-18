import base64
import json

from fastapi import FastAPI, Request, Form
from fastapi.responses import Response, PlainTextResponse
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException

from httpx import AsyncClient
from converter import VMessQRCode, convert_link

app = FastAPI(title='vmess-converter')
templating = Jinja2Templates('templates')


def convert_all(text: str):
    response_links = []
    for link in text.split('\n'):
        converted_link = link
        if link.startswith('vmess'):
            try:
                decoded_vmess_qr_code = base64.b64decode(link[8:].encode()).decode()
                json_vmess_qr_code = json.loads(decoded_vmess_qr_code)
                converted_link = convert_link(VMessQRCode(**json_vmess_qr_code))
            except Exception as e:
                print(str(e))
                pass
        response_links.append(converted_link)
    return '\n'.join(response_links)


def decode_base64(source_text: str):
    try:
        text = base64.b64decode(source_text).decode()
    except Exception:
        text = source_text
    return text


def encode_base64(source_text: str):
    return base64.b64encode(source_text.encode()).decode()


@app.get("/")
async def root(request: Request):
    return templating.TemplateResponse('index.html', {'request': request})


@app.get('/http{sub_url:path}')
async def convert_sub(sub_url: str, request: Request):
    sub_url = f'http{sub_url}'
    user_agent = request.headers.get('user-agent', 'None')

    try:
        async with AsyncClient() as client:
            client: AsyncClient
            response = await client.get(sub_url, headers={'user-agent': user_agent})
    except Exception:
        raise HTTPException(422, detail=':(')

    response_text = decode_base64(response.text)
    delete_headers = ['content-length', 'content-encoding']
    for header in delete_headers:
        response.headers.pop(header, None)

    if 'vmess' not in response_text or 'foxray' not in user_agent.lower():
        return Response(encode_base64(response_text), headers=response.headers)

    response_base64 = encode_base64(convert_all(response_text))
    return Response(response_base64, headers=response.headers)


@app.post('/config', response_class=PlainTextResponse)
async def convert_text_config(config: str = Form(...)):
    config = decode_base64(config)

    return convert_all(config)
