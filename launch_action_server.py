from rasa.__main__ import create_argument_parser
from rasa.cli.run import run_actions
import rasa_sdk.__main__ as sdk
import argparse


args = argparse.Namespace(
    actions="actions",
    auth_token=None,
    auto_reload=True,
    connector=None,
    cors=None,
    credentials=None,
    enable_api=False,
    endpoints=None,
    func=run_actions,
    jwt_method="HS256",
    jwt_secret=None,
    log_file=None,
    loglevel=None,
    model="models",
    port=5055,
    remote_storage=None,
    response_timeout=3600,
    ssl_ca_file=None,
    ssl_certificate=None,
    ssl_keyfile=None,
    ssl_password=None,
    **{"model-as-positional-argument": None}
)

sdk.main_from_args(args)
