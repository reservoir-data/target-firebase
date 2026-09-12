# Copyright (c) 2026 Edgar-Ramírez Mondragón

"""Firebase target sink class, which handles writing streams."""

from __future__ import annotations

import datetime as dt
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, override

from singer_sdk.sinks import RecordSink

if TYPE_CHECKING:
    from google.cloud.firestore_v1 import Client
    from singer_sdk.helpers.types import Context, Record


class FirebaseSink(RecordSink):
    """Firebase target sink class."""

    def __init__(self, *args: Any, db: Client, **kwargs: Any) -> None:
        """Initialize the sink."""
        super().__init__(*args, **kwargs)
        if len(self.key_properties) > 1:
            msg = "Composite keys are not supported"
            raise NotImplementedError(msg)

        self._db: Client = db

    @property
    def db(self) -> Client:
        """The Firestore client."""
        return self._db

    @override
    def process_record(self, record: Record, context: Context | None) -> None:
        """Process the record.

        Args:
            record: Individual record in the stream.
            context: Stream partition or context dictionary.
        """
        record = _conform_record(record)

        if len(self.key_properties) == 1:
            record_id = str(record[self.key_properties[0]])
            self.db.collection(self.stream_name).document(record_id).set(record)
            return

        self.db.collection(self.stream_name).add(record)


def _conform_record(record: Record) -> Record:
    """Conform the record to something Firestore can accept.

    Valid types are handled in https://github.com/googleapis/google-cloud-python/blob/3bbcbdf1a62dd10ab96f72e5c8198cffe9174ac7/packages/google-cloud-firestore/google/cloud/firestore_v1/_helpers.py#L166-L231.

    Args:
        record: The record to conform.

    Returns:
        The conformed record.
    """
    conformed_record: Record = {}
    for key, value in record.items():
        if isinstance(value, (bool, int, float, dt.datetime, str, list, Mapping)) or value is None:
            conformed_record[key] = value
        elif isinstance(value, (dt.date, dt.time)):
            conformed_record[key] = value.isoformat()
        else:
            conformed_record[key] = str(value)

    return conformed_record
