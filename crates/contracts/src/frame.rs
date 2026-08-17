use serde::{Serialize, de::DeserializeOwned};
use serde_json::error::Category as JsonErrorCategory;
use std::io::{Error, ErrorKind, Read, Write};

pub const LENGTH_PREFIX_BYTES: usize = 4;
pub const MAX_PAYLOAD_BYTES: usize = 65_536;
pub const MAX_WIRE_FRAME_BYTES: usize = LENGTH_PREFIX_BYTES + MAX_PAYLOAD_BYTES;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum FrameError {
    TruncatedPrefix,
    EmptyPayload,
    PayloadTooLarge { length: usize, max: usize },
    TruncatedPayload { declared: usize },
    Io { kind: ErrorKind },
    SerializationFailed { category: JsonErrorCategory },
    InvalidJson { category: JsonErrorCategory },
}

#[derive(Default)]
struct BoundedPayloadWriter {
    bytes: Vec<u8>,
    overflow_length: Option<usize>,
}

impl Write for BoundedPayloadWriter {
    fn write(&mut self, buffer: &[u8]) -> std::io::Result<usize> {
        let attempted = self.bytes.len().saturating_add(buffer.len());
        if attempted > MAX_PAYLOAD_BYTES {
            self.overflow_length = Some(attempted);
            return Err(Error::other("serialized payload exceeds frame bound"));
        }

        self.bytes.extend_from_slice(buffer);
        Ok(buffer.len())
    }

    fn flush(&mut self) -> std::io::Result<()> {
        Ok(())
    }
}

pub fn encode_frame<T>(value: &T) -> Result<Vec<u8>, FrameError>
where
    T: Serialize,
{
    let mut payload = BoundedPayloadWriter::default();
    let serialization = serde_json::to_writer(&mut payload, value);
    if let Some(length) = payload.overflow_length {
        return Err(FrameError::PayloadTooLarge {
            length,
            max: MAX_PAYLOAD_BYTES,
        });
    }
    serialization.map_err(|error| FrameError::SerializationFailed {
        category: error.classify(),
    })?;

    if payload.bytes.is_empty() {
        return Err(FrameError::EmptyPayload);
    }

    let length = payload.bytes.len();
    let declared = u32::try_from(length).map_err(|_| FrameError::PayloadTooLarge {
        length,
        max: MAX_PAYLOAD_BYTES,
    })?;
    let mut wire = Vec::with_capacity(LENGTH_PREFIX_BYTES + length);
    wire.extend_from_slice(&declared.to_be_bytes());
    wire.extend_from_slice(&payload.bytes);
    Ok(wire)
}

pub fn read_frame<R, T>(reader: &mut R) -> Result<T, FrameError>
where
    R: Read,
    T: DeserializeOwned,
{
    let mut prefix = [0_u8; LENGTH_PREFIX_BYTES];
    if let Err(error) = reader.read_exact(&mut prefix) {
        if error.kind() == ErrorKind::UnexpectedEof {
            return Err(FrameError::TruncatedPrefix);
        }
        return Err(FrameError::Io { kind: error.kind() });
    }

    let declared = u32::from_be_bytes(prefix) as usize;
    if declared == 0 {
        return Err(FrameError::EmptyPayload);
    }
    if declared > MAX_PAYLOAD_BYTES {
        return Err(FrameError::PayloadTooLarge {
            length: declared,
            max: MAX_PAYLOAD_BYTES,
        });
    }

    let mut payload = vec![0_u8; declared];
    if let Err(error) = reader.read_exact(&mut payload) {
        if error.kind() == ErrorKind::UnexpectedEof {
            return Err(FrameError::TruncatedPayload { declared });
        }
        return Err(FrameError::Io { kind: error.kind() });
    }

    serde_json::from_slice(&payload).map_err(|error| FrameError::InvalidJson {
        category: error.classify(),
    })
}
