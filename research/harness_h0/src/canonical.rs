//! Frozen canonical JSON bytes for H0 identity material.

use serde::Serialize;
use serde_json::Value;
use std::{error::Error, fmt};

pub const CANONICAL_JSON_VERSION: &str = "wepld-h0-json-v1";
pub const MANIFEST_HASH_FIELD: &str = "manifest_hash";

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum CanonicalError {
    Serialization(String),
    UnsupportedNumber(String),
    ManifestMustBeObject,
    ManifestHashFieldPresent,
}

impl fmt::Display for CanonicalError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Serialization(message) => write!(f, "serialization failed: {message}"),
            Self::UnsupportedNumber(number) => {
                write!(f, "canonical JSON rejects non-integer number: {number}")
            }
            Self::ManifestMustBeObject => f.write_str("manifest hash material must be an object"),
            Self::ManifestHashFieldPresent => {
                f.write_str("manifest hash material must exclude manifest_hash")
            }
        }
    }
}

impl Error for CanonicalError {}

pub fn canonical_json_bytes<T: Serialize + ?Sized>(value: &T) -> Result<Vec<u8>, CanonicalError> {
    let value = serde_json::to_value(value)
        .map_err(|error| CanonicalError::Serialization(error.to_string()))?;
    canonical_value_bytes(&value)
}

pub fn canonical_value_bytes(value: &Value) -> Result<Vec<u8>, CanonicalError> {
    let mut out = Vec::new();
    write_value(value, &mut out)?;
    Ok(out)
}

pub fn canonical_manifest_payload_bytes<T: Serialize + ?Sized>(
    value: &T,
) -> Result<Vec<u8>, CanonicalError> {
    let value = serde_json::to_value(value)
        .map_err(|error| CanonicalError::Serialization(error.to_string()))?;
    let object = value
        .as_object()
        .ok_or(CanonicalError::ManifestMustBeObject)?;
    if object.contains_key(MANIFEST_HASH_FIELD) {
        return Err(CanonicalError::ManifestHashFieldPresent);
    }
    canonical_value_bytes(&value)
}

fn write_value(value: &Value, out: &mut Vec<u8>) -> Result<(), CanonicalError> {
    match value {
        Value::Null => out.extend_from_slice(b"null"),
        Value::Bool(true) => out.extend_from_slice(b"true"),
        Value::Bool(false) => out.extend_from_slice(b"false"),
        Value::Number(number) => {
            if let Some(value) = number.as_i64() {
                out.extend_from_slice(value.to_string().as_bytes());
            } else if let Some(value) = number.as_u64() {
                out.extend_from_slice(value.to_string().as_bytes());
            } else {
                return Err(CanonicalError::UnsupportedNumber(number.to_string()));
            }
        }
        Value::String(text) => write_string(text, out)?,
        Value::Array(values) => {
            out.push(b'[');
            for (index, item) in values.iter().enumerate() {
                if index != 0 {
                    out.push(b',');
                }
                write_value(item, out)?;
            }
            out.push(b']');
        }
        Value::Object(object) => {
            let mut keys: Vec<&String> = object.keys().collect();
            keys.sort_by(|left, right| left.as_bytes().cmp(right.as_bytes()));
            out.push(b'{');
            for (index, key) in keys.iter().enumerate() {
                if index != 0 {
                    out.push(b',');
                }
                write_string(key, out)?;
                out.push(b':');
                write_value(&object[*key], out)?;
            }
            out.push(b'}');
        }
    }
    Ok(())
}

fn write_string(text: &str, out: &mut Vec<u8>) -> Result<(), CanonicalError> {
    let encoded = serde_json::to_string(text)
        .map_err(|error| CanonicalError::Serialization(error.to_string()))?;
    out.extend_from_slice(encoded.as_bytes());
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde::Serialize;
    use serde_json::{Map, Number};

    #[test]
    fn object_keys_are_sorted_recursively() {
        let mut nested = Map::new();
        nested.insert("z".into(), Value::Null);
        nested.insert("a".into(), Value::Bool(true));
        let mut root = Map::new();
        root.insert("z".into(), Value::String("x".into()));
        root.insert("nested".into(), Value::Object(nested));
        root.insert("a".into(), Value::Number(Number::from(1)));
        let bytes = canonical_value_bytes(&Value::Object(root)).unwrap();
        assert_eq!(
            bytes.as_slice(),
            br#"{"a":1,"nested":{"a":true,"z":null},"z":"x"}"#
        );
    }

    #[test]
    fn array_order_is_identity_bearing() {
        assert_ne!(
            canonical_json_bytes(&serde_json::json!({"x": [1, 2]})).unwrap(),
            canonical_json_bytes(&serde_json::json!({"x": [2, 1]})).unwrap()
        );
    }

    #[test]
    fn floats_fail_closed() {
        assert!(matches!(
            canonical_json_bytes(&serde_json::json!({"x": 1.25})).unwrap_err(),
            CanonicalError::UnsupportedNumber(_)
        ));
    }

    #[derive(Serialize)]
    struct Demo<'a> {
        task_id: &'a str,
        revision: u64,
    }

    #[test]
    fn manifest_hash_material_is_non_self_referential() {
        let demo = Demo {
            task_id: "task-1",
            revision: 7,
        };
        let bytes = canonical_manifest_payload_bytes(&demo).unwrap();
        assert_eq!(
            bytes.as_slice(),
            br#"{"revision":7,"task_id":"task-1"}"#
        );
        assert_eq!(
            canonical_manifest_payload_bytes(&vec![1_u64]).unwrap_err(),
            CanonicalError::ManifestMustBeObject
        );
        assert_eq!(
            canonical_manifest_payload_bytes(&serde_json::json!({"manifest_hash":"00"}))
                .unwrap_err(),
            CanonicalError::ManifestHashFieldPresent
        );
    }

    #[test]
    fn strings_are_not_unicode_normalized() {
        assert_eq!(
            canonical_json_bytes(&"a\n\"é").unwrap(),
            "\"a\\n\\\"é\"".as_bytes()
        );
        assert_ne!(
            canonical_json_bytes(&"é").unwrap(),
            canonical_json_bytes(&"e\u{301}").unwrap()
        );
    }
}
