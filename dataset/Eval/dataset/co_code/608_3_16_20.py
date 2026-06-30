#     return cls(
#         k=jnp.zeros((layers, bsz, max_seq_len, kv_heads, head_dim), dtype=jnp.bfloat16),
#         v=jnp.zeros((layers, bsz, max_seq_len, kv_heads, head_dim), dtype=jnp.bfloat16)
#     )
