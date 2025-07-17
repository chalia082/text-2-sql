import pickle
import os

# 📂 Get path to project root (one level up from /tools/)
base_dir = os.path.dirname(os.path.dirname(__file__))

# 📄 Build full path to id_to_col.pkl inside embeddings/
pkl_path = os.path.join(base_dir, "embeddings", "id_to_col.pkl")

# 📦 Load and preview
try:
    with open(pkl_path, "rb") as f:
        data = pickle.load(f)

    print(f"\n✅ Loaded .pkl file — Type: {type(data)}\n")

    # 🧠 Show based on structure
    if isinstance(data, dict):
        print("🔍 Top 5 entries from dictionary:")
        for i, (k, v) in enumerate(data.items()):
            print(f"{i+1}. {k} → {v}")
            if i >= 4:
                break

    elif isinstance(data, list):
        print("🔍 First item in list:")
        print(data[0])

    else:
        print("⚠️ Unrecognized format. Sample content:")
        print(data)

except FileNotFoundError:
    print(f"❌ File not found at: {pkl_path}")
except Exception as e:
    print(f"❌ Error loading pickle: {e}")
