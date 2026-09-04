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


# class Singleton(type):
#     _instances:Dict  = {}
#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
#         return cls._instances[cls]


# class OverriddenClientCredential(ClientCredential,metaclass=Singleton):
#     def __init__(self, client_id, client_secret,site_url):
#         self.clientId = client_id
#         self.clientSecret = client_secret
#         self.ctx=ClientContext(site_url).with_credentials(self)
#         web = self.ctx.web
#         self.ctx.load(web)
#         self.ctx.execute_query()


class FeatherLoader:
    def __init__(self, ctx_factory=get_ctx):
        self._ctx_factory = ctx_factory
        self.cache = {}
    
    def load_feather(self, filename: str, cache_flag = True) -> pl.DataFrame:
        """Returns a cached pl DataFrame (loads if needed)"""
        if filename in self.cache:
            return self.cache[filename]

        file_bytes = None
        for attempt in range(3):
            try:
                file_bytes = self._download_from_sharepoint(filename)
                df = pl.read_ipc(io.BytesIO(file_bytes))
                if isinstance(df, pl.DataFrame):
                    if cache_flag:
                        self.cache[filename] = df
                    return df
                else:
                    raise  ValueError("Result is not a Polars DataFrame")
    
            except Exception as e:
                if attempt == 2:
                    hx.errors.fatal(f"Failed to load {filename}: {str(e)}")
                time.sleep(1)

    def load_parquet(self, filename: str, cache_flag = True) -> pl.DataFrame:
        """Returns a cached pl DataFrame (loads if needed)"""
        if filename in self.cache:
            return self.cache[filename]

        file_bytes = None
        for attempt in range(3):
            try:
                file_bytes = self._download_from_sharepoint(filename)
                df = pl.read_parquet(io.BytesIO(file_bytes))
                if isinstance(df, pl.DataFrame):
                    if cache_flag:
                        self.cache[filename] = df
                    return df
                else:
                    raise  ValueError("Result is not a Polars DataFrame")
    
            except Exception as e:
                if attempt == 2:
                    hx.errors.fatal(f"Failed to load {filename}: {str(e)}")
                time.sleep(1)   
    
    def _download_from_sharepoint(self, filename: str) -> bytes:
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
        return response.content

    def clear_cache(self):
        self.cache.clear()

    def get_cached_keys(self):
        return list(self.cache.keys())

    def __contains__(self, key):
        return key in self.cache




def load_from_em_database(query):
    try:
        # Determine environment
        env = hx.secrets.environment_name.lower()
        if "dev" in env or "tst" in env:
            host = hx.secrets.exposuremanagement_host_uat
            user = hx.secrets.exposuremanagement_login_uat
            pwd = hx.secrets.exposuremanagement_password_uat
        else:
            host = hx.secrets.exposuremanagement_host_prd
            user = hx.secrets.exposuremanagement_login_prd
            pwd = hx.secrets.exposuremanagement_password_prd

        # Connect to DB
        conn_str = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            f"SERVER={host};DATABASE=Property_data;"
            f"UID={user};PWD={pwd};"
        )

        with pyodbc.connect(conn_str, timeout=30, autocommit=True) as cnxn:
            cnxn.cursor()
            df = pd.read_sql(query, cnxn)
            return df

    except Exception as e:
        hx.errors.fatal(f"Query failed: {str(e)}")



class LoadFromSQL:
    def __init__(self, ctx_factory=get_ctx):
        self.cache = {}
    
    def clear_cache(self):
        self.cache.clear()

    def get_cached_keys(self):
        return list(self.cache.keys())
    
    def get_elt(self, accgrpid, perspcode):
        """Returns a cached pl DataFrame (loads if needed)"""
        cache_key = perspcode + '_ELT'
        if cache_key in self.cache:
            return self.cache[cache_key]

        query = f"""
            SELECT  
                EventID,
                Rate,
                perspvalue AS MeanLoss,
                stddevi AS StdevI,
                stddevc AS StDevC,
                expvalue AS ExpVal,
                Peril,
                region
            FROM property_data.dbo.vw_elt_policy vlp WITH (NOLOCK) 
            WHERE 1=1 
            AND accgrpid = '{accgrpid}'
            AND perspcode = '{perspcode}'
        """
        df = load_from_em_database(query)
        if df.empty:
            hx.errors.fatal("Fetch failed. ELT not found in EM database. Please check accgrpid and simulation type.")     
        
        df = pl.from_pandas(df)
        if isinstance(df, pl.DataFrame):
            self.cache[cache_key] = df
            return df


    def get_yelt(self, accgrpid, perspcode):
        """Returns a cached pl DataFrame (loads if needed)"""
        cache_key = perspcode + '_YELT'
        if cache_key in self.cache:
            return self.cache[cache_key]

        query = f"""
            SELECT
                eym.[year] AS Yr,
                pol.EventID,
                pol.Rate,
                pol.perspvalue AS MeanLoss,
                pol.stddevi AS StdevI,
                pol.stddevc AS StDevC,
                pol.expvalue AS ExpVal,
                pol.Peril
            FROM property_data.dbo.vw_elt_policy pol WITH (NOLOCK)
            INNER JOIN Property_reference.dbo.vw_eventYearMapping eym WITH (NOLOCK)
                ON pol.EventID = eym.[event]
            WHERE accgrpid = '{accgrpid}'
            AND perspcode = '{perspcode}'

        """
        df = load_from_em_database(query)
        if df.empty:
            hx.errors.fatal("Fetch failed. ELT not found in EM database. Please check accgrpid and simulation type.")     
        
        df = pl.from_pandas(df)
        if isinstance(df, pl.DataFrame):
            self.cache[cache_key] = df
            return df

    
    def get_rds_elt(self, accgrpid, perspcode):
        """Returns a cached pl DataFrame (loads if needed)"""
        cache_key = perspcode + '_RDS'
        if cache_key in self.cache:
            return self.cache[cache_key]

        rds_events = hx.params.rds_eventids
        sql_ids = ','.join(rds_events['EventID'].astype(float).astype(int).astype(str))
        query = f"""
            SELECT  
                ANLSID,
                NAME,
                EventID,
                Rate,
                perspvalue AS MeanLoss,
                stddevi AS StdevI,
                stddevc AS StDevC,
                expvalue AS ExpVal,
                Peril
            FROM property_data.dbo.vw_elt_policy vlp WITH (NOLOCK) 
            WHERE 1=1 
            AND accgrpid = '{accgrpid}'
            AND perspcode = '{perspcode}'
            AND EventID IN ({sql_ids})
        """
        df = load_from_em_database(query)
        df = pl.from_pandas(df)
        if isinstance(df, pl.DataFrame):
            self.cache[cache_key] = df
            return df


    def __contains__(self, key):
        return key in self.cache
