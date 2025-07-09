from db.valkey import valkey_client

# Get all keys
keys = valkey_client.scan_iter()

# Iterate and print key, type, and value
for key in keys:
    key_type = r.type(key)
    print(f"Key: {key} (Type: {key_type})")

    if key_type == "string":
        print(f"  Value: {r.get(key)}")
    elif key_type == "list":
        print(f"  Value: {r.lrange(key, 0, -1)}")
    elif key_type == "set":
        print(f"  Value: {r.smembers(key)}")
    elif key_type == "zset":
        print(f"  Value: {r.zrange(key, 0, -1, withscores=True)}")
    elif key_type == "hash":
        print(f"  Value: {r.hgetall(key)}")
    else:
        print("  Unknown type")
