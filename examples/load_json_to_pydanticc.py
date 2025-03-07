from pydantic import BaseModel

json_str = """
{
    "vocab_size": 102400,
    "dim": 2048,
    "inter_dim": 10944,
    "moe_inter_dim": 1408,
    "n_layers": 27,
    "n_dense_layers": 1,
    "n_heads": 16,
    "n_routed_experts": 64,
    "n_shared_experts": 2,
    "n_activated_experts": 6,
    "route_scale": 1.0,
    "q_lora_rank": 0,
    "kv_lora_rank": 512,
    "qk_nope_head_dim": 128,
    "qk_rope_head_dim": 64,
    "v_head_dim": 128,
    "mscale": 0.707
}
"""


def load_json_from_str(json_str: str):
    import json

    return json.loads(json_str)


class ModelConfig(BaseModel):
    vocab_size: int
    dim: int
    inter_dim: int
    moe_inter_dim: int
    n_layers: int
    n_dense_layers: int
    n_heads: int
    n_routed_experts: int
    n_shared_experts: int
    n_activated_experts: int
    route_scale: float
    q_lora_rank: int
    kv_lora_rank: int
    qk_nope_head_dim: int
    qk_rope_head_dim: int
    v_head_dim: int
    mscale: float


if __name__ == "__main__":
    json_data = load_json_from_str(json_str)
    config = ModelConfig.model_validate(json_data)
    print(config)
