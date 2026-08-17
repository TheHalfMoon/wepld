#![forbid(unsafe_code)]

pub mod frame;
pub mod protocol;

pub use frame::{
    FrameError, LENGTH_PREFIX_BYTES, MAX_PAYLOAD_BYTES, MAX_WIRE_FRAME_BYTES, encode_frame,
    read_frame,
};
pub use protocol::*;
