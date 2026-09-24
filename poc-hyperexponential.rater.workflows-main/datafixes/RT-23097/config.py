import os

class Config:
    def __init__(self):
        self.base_url = os.environ.get("HX_API_BASE_URL")
        self.tenant_id = os.environ.get("HX_AZURE_AD_TENANTID")
        self.client_id = os.environ.get("HX_AZURE_AD_CLIENTID")
        self.secret_value = os.environ.get("HX_AZURE_AD_CLIENTSECRET")
        self.secret_env_var = None
        self.scope = os.environ.get("HX_AZURE_AD_SCOPE")
        self.input_file = os.environ.get("INPUT_FILE")
        self.output_dir = os.environ.get("OUTPUT_DIR")
        self.retries = 3
        self.overall_retries = 1
        self.workers = 4