# Copyright (c) 2026 Edgar-Ramírez Mondragón

"""Firebase target sink class, which handles writing streams."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, override

from singer_sdk.sinks import RecordSink

if TYPE_CHECKING:
    from google.cloud.firestore_v1 import Client
    from singer_sdk.helpers.types import Context, Record


class FirebaseSink(RecordSink):
    """Firebase target sink class."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the sink."""
        super().__init__(*args, **kwargs)
        if len(self.key_properties) > 1:
            msg = "Composite keys are not supported"
            raise NotImplementedError(msg)

        self._db: Client | None = None

    @property
    def db(self) -> Client:
        """The Firestore client.

        Raises:
            ValueError: If the client is not initialized.
        """
        if self._db is None:
            msg = "Firestore client not initialized"
            raise ValueError(msg)
        return self._db

    @db.setter
    def db(self, db: Client) -> None:
        """Set the Firestore client."""
        self._db = db

    @override
    def process_record(self, record: Record, context: Context | None) -> None:
        """Process the record.

        Args:
            record: Individual record in the stream.
            context: Stream partition or context dictionary.
        """
        if len(self.key_properties) == 1:
            self.db.collection("cities").document(self.key_properties[0]).set(record)
            return

        self.db.collection("cities").add(record)
