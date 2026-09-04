import hx, os, json, math, io, time, pyodbc
import pandas as pd
import polars as pl
import numpy as np
from typing import Dict
import pyarrow.feather as feather
from office365.runtime.auth.client_credential import ClientCredential
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
from functools import lru_cache


@lru_cache(maxsize=None)
def get_ctx(site_url: str, client_id: str, thumbprint: str, private_key: str) -> ClientContext:
    private_key = f"""-----BEGIN PRIVATE KEY-----
{private_key}
-----END PRIVATE KEY-----
"""
    cert_credentials = {
        'tenant': '9a50eba8-7568-447a-bcb9-27a0d464aa80',
        'client_id': client_id,
        'thumbprint': thumbprint,
        'private_key': private_key
    }
    ctx = ClientContext(site_url).with_client_certificate(**cert_credentials)
    # Load web once so subsequent calls don’t have that network round-trip
    ctx.load(ctx.web)
    ctx.execute_query()
    return ctx

    
class geojsonLoader:
    def __init__(self, ctx_factory=get_ctx):
        self._ctx_factory = ctx_factory
        self.cache = {}

    def download_geojson_from_sharepoint(self, filename: str) -> bytes:
        env = hx.secrets.environment_name.lower()

        if "dev" in env or "tst" in env:
            endpoint = hx.secrets.sharepoint_siteurl_dev
            client_id = hx.secrets.sharepoint_clientid_dev
            thumbprint = hx.secrets.sharepoint_cert_thumbprint_dev
            private_key = hx.secrets.sharepoint_cert_private_key_dev
        else:
            endpoint = hx.secrets.sharepoint_siteurl_prod
            client_id = hx.secrets.sharepoint_clientid_prod
            thumbprint = hx.secrets.sharepoint_cert_thumbprint_prod
            private_key = hx.secrets.sharepoint_cert_private_key_prod

        site_url = endpoint[:endpoint.find("/", endpoint.rfind("/sites/") + len("/sites/"))]
        relative_path = f'{endpoint[endpoint.rfind("/sites/"):]}/{filename}'

        ctx = self._ctx_factory(site_url, client_id, thumbprint, private_key)
        response = File.open_binary(ctx, relative_path)

        geojson_bytes = io.BytesIO(response.content)
        geojson = json.load(geojson_bytes)

        return geojson