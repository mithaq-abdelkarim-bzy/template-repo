import hx
import time
from functools import lru_cache
from io import BytesIO
from docx import Document
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File

#"tenant": "9a50eba8-7568-447a-bcb9-27a0d464aa80",
#"tenant": "1287c196-4709-4c3f-a9e6-0ab12722d319",

@lru_cache(maxsize=None)
def get_ctx(site_url: str, client_id: str, thumbprint: str, private_key: str) -> ClientContext:
    private_key = f"""-----BEGIN PRIVATE KEY-----
{private_key}
-----END PRIVATE KEY-----
"""
    cert_credentials = {
        "tenant": "9a50eba8-7568-447a-bcb9-27a0d464aa80",
        "client_id": client_id,
        "thumbprint": thumbprint,
        "private_key": private_key,
    }
    ctx = ClientContext(site_url).with_client_certificate(**cert_credentials)
    ctx.load(ctx.web)
    ctx.execute_query()
    return ctx

class FeatherLoader:
    """Utility for downloading and caching SharePoint documents."""

    def __init__(self, endpoint, ctx_factory=get_ctx):
        self._ctx_factory = ctx_factory
        self.cache = {}
        self.endpoint = endpoint

    def load_word_document(self, filename: str, cache_flag: bool = True) -> Document:
        """Download a Word document from SharePoint and return a python-docx Document."""
        cached_value = self.cache.get(filename)
        if cache_flag and isinstance(cached_value, bytes):
            return self._bytes_to_document(cached_value)

        for attempt in range(3):
            try:
                file_bytes = self._download_from_sharepoint(filename)
                if cache_flag:
                    self.cache[filename] = file_bytes
                return self._bytes_to_document(file_bytes)
            except Exception as exc:  # pragma: no cover - retry loop
                if attempt == 2:
                    hx.errors.fatal(f"Failed to load {filename}: {exc}")
                time.sleep(1)

    @staticmethod
    def _bytes_to_document(file_bytes: bytes) -> Document:
        return Document(BytesIO(file_bytes))

    def _download_from_sharepoint(self, filename: str) -> bytes:
        env = hx.secrets.environment_name.lower()

        if "dev" in env or "tst" in env:
            #endpoint = hx.secrets.sharepoint_siteurl_dev
            endpoint = self.endpoint
            client_id = hx.secrets.sharepoint_clientid_dev
            thumbprint = hx.secrets.sharepoint_cert_thumbprint_dev
            private_key = hx.secrets.sharepoint_cert_private_key_dev
        else:
            #endpoint = hx.secrets.sharepoint_siteurl_prod
            endpoint = self.endpoint
            client_id = hx.secrets.sharepoint_clientid_prod
            thumbprint = hx.secrets.sharepoint_cert_thumbprint_prod
            private_key = hx.secrets.sharepoint_cert_private_key_prod

        site_url = endpoint[: endpoint.find("/", endpoint.rfind("/sites/") + len("/sites/"))]
        relative_path = f"{endpoint[endpoint.rfind('/sites/') : ]}/{filename}"

        ctx = self._ctx_factory(site_url, client_id, thumbprint, private_key)
        response = File.open_binary(ctx, relative_path)
        return response.content

    def clear_cache(self):
        self.cache.clear()

    def get_cached_keys(self):
        return list(self.cache.keys())

    def __contains__(self, key):
        return key in self.cache