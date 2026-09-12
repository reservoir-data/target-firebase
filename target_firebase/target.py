# Copyright (c) 2026 Edgar-Ramírez Mondragón

"""Firebase target class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, override

import firebase_admin
from firebase_admin import credentials, firestore
from singer_sdk import typing as th
from singer_sdk.target_base import Target

from target_firebase.sinks import FirebaseSink

if TYPE_CHECKING:
    from singer_sdk.singerlib.types import KeyProperties


class TargetFirebase(Target):
    """Sample target for Firebase."""

    name = "target-firebase"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "credential_file",
            th.StringType,
            description=(
                "The path to the Google Cloud Firestore credential file. "
                "If none is provided, Google Application Default Credentials are used."
            ),
        ),
        th.Property(
            "credential",
            th.ObjectType(
                th.Property(
                    "type",
                    th.Constant("service_account"),
                    required=True,
                    description="The type of credential.",
                    default="service_account",
                ),
                th.Property(
                    "client_email",
                    th.StringType,
                    required=True,
                    description="The service account's email.",
                ),
                th.Property(
                    "token_uri",
                    th.StringType,
                    description="The OAuth 2.0 Token URI.",
                    default="https://oauth2.googleapis.com/token",
                ),
                th.Property(
                    "project_id",
                    th.StringType,
                    required=True,
                    description="Project ID associated with the service account credential.",
                ),
                th.Property(
                    "universe_domain",
                    th.StringType,
                    description=(
                        "The universe domain. The default universe domain is "
                        "googleapis.com. For default value self signed jwt is "
                        "used for token refresh."
                    ),
                ),
                th.Property(
                    "trust_boundary",
                    th.StringType,
                    description="String representation of trust boundary meta.",
                ),
            ),
            description=(
                "The Google Cloud Firestore credential object. "
                "If none is provided, Google Application Default Credentials are used."
            ),
        ),
        th.Property(
            "firebase_app",
            th.StringType,
            description="The name of the Firebase app to use.",
            default="[DEFAULT]",
            nullable=False,
        ),
        th.Property(
            "database_id",
            th.StringType,
            description=(
                "The database ID of the Google Cloud Firestore database to be used. "
                "Defaults to the default Firestore database ID if not specified or an "
                "empty string."
            ),
        ),
    ).to_dict()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the target.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        if credential := self.config.get("credential"):
            cred = credentials.Certificate(credential)  # type: ignore[no-untyped-call]
        elif credential_file := self.config.get("credential_file"):
            cred = credentials.Certificate(credential_file)  # type: ignore[no-untyped-call]
        else:
            cred = credentials.ApplicationDefault()  # type: ignore[assignment,no-untyped-call]

        try:
            app = firebase_admin.get_app(name=self.config["firebase_app"])  # type: ignore[no-untyped-call]
        except ValueError:
            app = firebase_admin.initialize_app(credential=cred, name=self.config["firebase_app"])  # type: ignore[no-untyped-call]

        self.db = firestore.client(app=app, database_id=self.config.get("database_id"))

    @override
    def create_sink(
        self,
        *,
        stream_name: str,
        schema: dict[str, Any],
        key_properties: KeyProperties | None = None,
    ) -> FirebaseSink:
        return FirebaseSink(
            target=self,
            stream_name=stream_name,
            schema=schema,
            key_properties=key_properties,
            db=self.db,
        )


if __name__ == "__main__":
    """Run the TargetFirebase CLI."""
    TargetFirebase.cli()
