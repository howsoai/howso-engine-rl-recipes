from gymnasium.envs.registration import register

register(
    id="WaferThinMint-v0",
    entry_point="howso_recipes_engine_rl.wafer_thin_mint.wafer_thin_mint:WaferThinMintEnv",
)
