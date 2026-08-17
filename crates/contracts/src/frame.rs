use serde::{Serialize, de::DeserializeOwned};
use std::io::{ErrorKind, Read};

pub const LENGTH_PREFIX_BYTES: usize = 4;
pub const MAX_PAYLOAD_BYTES: usize = 65_536;
pub const MAX_WIRE_FRAME_BYTES: usize = LENGTH_PREFIX_BYTES + MAX_PAYLOAD_BYTES;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum FrameError {
    TruncatedPrefix,
    EmptyPayload,
    PayloadTooLarge { declared: usize, max: usize },
    TruncatedPayload { declared: usize },
    Io,
    SerializationFailed,
    InvalidJson,
}

pub fn encode_frame<T>(value: &T) -> Result<Vec<u8>, FrameError>
where
    T: Serialize,
{
    let payload = serde_json::to_vec(value).map_err(|_| FrameError::SerializationFailed)?;
    if payload.is_empty() {
        return Err(FrameError::EmptyPayload);
    }
    if payload.len() > MAX_PAYLOAD_BYTES {
        return Err(FrameError::PayloadTooLarge {
            declared: payload.len(),
            max: MAX_PAYLOAD_BYTES,
        });
    }

    let declared = u32::try_from(payload.len()).map_err(|_| FrameError::PayloadTooLarge {
        declared: payload.len(),
        max: MAX_PAYLOAD_BYTES,
    })?;
    let mut wire = Vec::with_capacity(LENGTH_PREFIX_BYTES + payload.len());
    wire.extend_from_slice(&declared.to_be_bytes());
    wire.extend_from_slice(&payload);
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
        return Err(FrameError::Io);
    }

    let declared = u32::from_be_bytes(prefix) as usize;
    if declared == 0 {
        return Err(FrameError::EmptyPayload);
    }
    if declared > MAX_PAYLOAD_BYTES {
        return Err(FrameError::PayloadTooLarge {
            declared,
            max: MAX_PAYLOAD_BYTES,
        });
    }

    let mut payload = vec![0_u8; declared];
    if let Err(error) = reader.read_exact(&mut payload) {
        if error.kind() == ErrorKind::UnexpectedEof {
            return Err(FrameError::TruncatedPayload { declared });
        }
        return Err(FrameError::Io);
    }

    serde_json::from_slice(&payload).map_err(|_| FrameError::InvalidJson)
}
