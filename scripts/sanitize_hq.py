import os

# THE IMPERIAL DICTIONARY
REPLACEMENTS = {
    "spacetime": "Magnetic Tension Field",
    "Spacetime": "Magnetic Tension Field",
    "speed of light": "Variable Sensor Lag",
    "General Relativity": "Vacuum Pressure Dynamics",
    "Big Bang": "ERROR: INVALID MODEL",
    "dark matter": "Geomagnetic Vacuum Sheet",
    "gravitational waves": "Lattice Stress Waves"
}

print(">>> SECURING THE IMPERIAL CHALLENGE <<<")
count = 0

for root, dirs, files in os.walk("."):
    if ".git" in root: continue
    
    for file in files:
        if file.endswith((".md", ".txt", ".py")):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = content
                for bad, good in REPLACEMENTS.items():
                    new_content = new_content.replace(bad, good)
                
                if new_content != content:
                    print(f"SANITIZED: {file}")
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    count += 1
            except:
                pass

print(f">>> HQ SECURED. {count} FILES SCRUBBED. <<<")
