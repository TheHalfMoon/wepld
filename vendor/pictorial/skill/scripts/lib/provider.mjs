// Modified by WePLD on 2026-08-23: deterministic Pictorial rebrand/path integration from the pinned upstream source.
// Source scripts default to slash commands. The provider build replaces only
// this exact declaration, avoiding heuristic rewrites across executable code.
export const PICTORIAL_COMMAND_PREFIX = '/'; // @pictorial-provider-command-prefix
export const PICTORIAL_PROVIDER_ID = 'source'; // @pictorial-provider-id
export const PICTORIAL_COMMAND = `${PICTORIAL_COMMAND_PREFIX}pictorial`;
