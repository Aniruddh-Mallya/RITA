import os

structure = {
    "frontend": ["components.js", "views.js"],
}

def create_structure():
    print("👷 Setting up Frontend Modules...")
    for folder, files in structure.items():
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"   [+] Created folder: {folder}/")
        
        for file in files:
            path = os.path.join(folder, file)
            with open(path, 'w') as f:
                f.write("// Module: " + file + "\n")
            print(f"   [+] Created file:   {path}")

    print("\n✅ Frontend structure ready! Paste the JS code into the files.")

if __name__ == "__main__":
    create_structure()