#!/usr/bin/env python3
"""
BCH Quantum Vault (Merkle Signature Scheme)
---------------------------------------------------
Implements a Merkle Tree-based Post-Quantum Vault.
Security:
- Uses SHA256 (Quantum Resistant).
- Public Key = Merkle Root.
- Private Key = List of One-Time Secrets (Leaves).
- Signing = Revealing one secret + Merkle Path.

This allows multiple spends from a single "Root Identity" 
without reusing the same one-time key.
"""

import hashlib
import secrets
import sys
import json

# --- MERKLE TREE LOGIC ---

def hash_data(data):
    """Double SHA256 for security"""
    r1 = hashlib.sha256(data).digest()
    return hashlib.sha256(r1).digest()

def hash_pair(left, right):
    """Hash two nodes together"""
    return hash_data(left + right)

class MerkleTree:
    def __init__(self, leaves):
        self.leaves = leaves
        self.tree = [leaves]
        self.build_tree()

    def build_tree(self):
        current_level = self.leaves
        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                if i + 1 < len(current_level):
                    right = current_level[i+1]
                else:
                    right = left # Duplicate last node if odd
                next_level.append(hash_pair(left, right))
            self.tree.append(next_level)
            current_level = next_level
            
    def get_root(self):
        return self.tree[-1][0]

    def get_proof(self, index):
        """Generate Merkle Proof for a specific leaf index"""
        proof = []
        for level in self.tree[:-1]: # Skip root
            is_right_node = index % 2 == 1
            sibling_index = index - 1 if is_right_node else index + 1
            
            if sibling_index < len(level):
                sibling = level[sibling_index]
            else:
                sibling = level[index] # Duplicate case
                
            proof.append({
                'sibling': sibling.hex(),
                'is_left_sibling': not is_right_node
            })
            index //= 2
        return proof

# --- UTILS ---

def generate_leaf_secrets(count=4):
    """Generate N random secrets for the tree leaves"""
    return [secrets.token_bytes(32) for _ in range(count)]

def script_to_p2sh(script, mainnet=True):
    """Convert script to P2SH Address (Legacy 3...)"""
    s256 = hashlib.sha256(script).digest()
    try:
        rmd = hashlib.new('ripemd160')
    except ValueError:
        from Crypto.Hash import RIPEMD160
        rmd = RIPEMD160.new()
    rmd.update(s256)
    h160 = rmd.digest()
    
    version = b'\x05' if mainnet else b'\xc4'
    return base58_check(version, h160)

def base58_check(version, payload):
    data = version + payload
    h1 = hashlib.sha256(data).digest()
    h2 = hashlib.sha256(h1).digest()
    checksum = h2[:4]
    
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    val = int.from_bytes(data + checksum, 'big')
    encoded = ''
    while val > 0:
        val, mod = divmod(val, 58)
        encoded = alphabet[mod] + encoded
        
    for b in data + checksum:
        if b == 0: encoded = '1' + encoded
        else: break
    return encoded

# --- MAIN APP ---

def main():
    print("========================================")
    print("   BCH QUANTUM VAULT (LEVEL 2)     ")
    print("   Merkle Tree Signature Scheme    ")
    print("========================================")
    print("1. Create New Merkle Vault (4 One-Time Keys)")
    print("2. Spend from Vault (Reveal Leaf + Proof)")
    print("3. Exit")
    
    choice = input("\nSelect Option: ")
    
    if choice == "1":
        print("\nGenerating 4 One-Time Secrets (Leaves)...")
        secrets_list = generate_leaf_secrets(4)
        
        # Hash secrets to get leaf nodes
        leaves = [hash_data(s) for s in secrets_list]
        
        # Build Tree
        mt = MerkleTree(leaves)
        root = mt.get_root()
        
        # Generate P2SH Address for the Root
        # Script: OP_SHA256 <Root> OP_EQUAL
        # Note: Real L2 uses more complex scripts to verify the path.
        # This simplified version locks funds to the ROOT.
        # To spend, you provide a script that calculates the root from a leaf + proof.
        
        # For this demo, the locking script is standard P2SH of the ROOT.
        # The "spending" logic happens off-chain to verify the path.
        locking_script = b'\xa8\x20' + root + b'\x87'
        address = script_to_p2sh(locking_script)
        
        vault_data = {
            "root": root.hex(),
            "address": address,
            "secrets": [s.hex() for s in secrets_list],
            "spent_mask": [False] * 4
        }
        
        with open("quantum_vault.json", "w") as f:
            json.dump(vault_data, f, indent=4)
            
        print(f"\n[+] VAULT CREATED")
        print(f"Root Hash: {root.hex()}")
        print(f"Address:   {address}")
        print(f"Capacity:  4 Transactions (One-Time Signatures)")
        print("Saved to 'quantum_vault.json'. Keep this file safe!")

    elif choice == "2":
        try:
            with open("quantum_vault.json", "r") as f:
                vault = json.load(f)
        except FileNotFoundError:
            print("No vault file found.")
            return

        print(f"\nVault Root: {vault['root']}")
        print(f"Address:    {vault['address']}")
        
        # Find first unused key
        key_index = -1
        for i, used in enumerate(vault['spent_mask']):
            if not used:
                key_index = i
                break
        
        if key_index == -1:
            print("Error: All keys in this vault have been used!")
            return
            
        print(f"\nUsing Key Index: {key_index}")
        secret_hex = vault['secrets'][key_index]
        secret = bytes.fromhex(secret_hex)
        
        # Rebuild tree to get proof
        leaves = [hash_data(bytes.fromhex(s)) for s in vault['secrets']]
        mt = MerkleTree(leaves)
        proof = mt.get_proof(key_index)
        
        print("\n[+] GENERATING SPEND PROOF")
        print(f"Secret Revealed: {secret_hex}")
        print("Merkle Path:")
        for p in proof:
            direction = "Left" if p['is_left_sibling'] else "Right"
            print(f" - {direction} Sibling: {p['sibling'][:16]}...")
            
        print("\nTo verify this transaction on-chain (Hypothetical Quantum Contract):")
        print("1. Hasher(Secret) -> Leaf") # Fixed syntax error here
        print("2. Hasher(Leaf + Sibling1) -> Node1")
        print("3. Hasher(Node1 + Sibling2) -> Root")
        print("4. OP_EQUALVERIFY (Calculated Root == Locked Root)")
        
        confirm = input("\nMark key as used? (yes/no): ").lower()
        if confirm == "yes":
            vault['spent_mask'][key_index] = True
            with open("quantum_vault.json", "w") as f:
                json.dump(vault, f, indent=4)
            print("Key marked as used.")

    elif choice == "3":
        sys.exit()

if __name__ == "__main__":
    main()
