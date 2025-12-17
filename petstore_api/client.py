from dataclasses import dataclass
from typing import Tuple, List, Dict, Any, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


@dataclass(frozen=True)
class PetstoreConfig:
    base_url: str
    timeout: Tuple[float, float] = (3.0, 15.0)


class PetstoreClient:
    def __init__(self, cfg: PetstoreConfig):
        self.cfg = cfg
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

        retry = Retry(
            total=3,
            connect=3,
            read=3,
            backoff_factor=0.4,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset({"GET", "POST"}),
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def create_users_with_list(self, users: List[Dict[str, Any]]) -> requests.Response:
        url = f"{self.cfg.base_url}/user/createWithList"
        return self.session.post(url, json=users, timeout=self.cfg.timeout)

    def get_user_by_username(self, username: str) -> requests.Response:
        url = f"{self.cfg.base_url}/user/{username}"
        return self.session.get(url, timeout=self.cfg.timeout)

    @staticmethod
    def safe_json(resp: requests.Response) -> Optional[Dict[str, Any]]:
        try:
            data = resp.json()
        except ValueError:
            return None
        return data if isinstance(data, dict) else None