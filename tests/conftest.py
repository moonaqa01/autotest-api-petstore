import pytest

from petstore_api import PetstoreClient, PetstoreConfig


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--petstore-base-url",
        action="store",
        default="https://petstore.swagger.io/v2",
        help="Base URL for Swagger Petstore (default: https://petstore.swagger.io/v2)",
    )


@pytest.fixture(scope="session")
def petstore_cfg(request: pytest.FixtureRequest) -> PetstoreConfig:
    base_url = request.config.getoption("--petstore-base-url").rstrip("/")
    return PetstoreConfig(base_url=base_url)


@pytest.fixture()
def petstore(petstore_cfg: PetstoreConfig) -> PetstoreClient:
    return PetstoreClient(petstore_cfg)