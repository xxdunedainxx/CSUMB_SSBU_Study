# IDK if ima finish this. might not be worth it :(
import os

# Regex tested w/ https://regexr.com/
import re

SEMANTIC_VERSION = "1.0.3"

# Get the mod JS into one big ass string
modJavaScript = "".join(
    open(f"mods{os.sep}ZPsyToolkitMod.js").readlines()
)

VERSION_REGEX_PATTERN = r'VERSION=\"[0-9].[0-9].[0-9]\"'

def injectVersion(modJavaScript):
    versionMatch = re.findall(
        VERSION_REGEX_PATTERN,
        modJavaScript
    )[0]
    print(versionMatch)
    return modJavaScript.replace(versionMatch, f"VERSION={SEMANTIC_VERSION}")

modJavaScript=injectVersion(modJavaScript)

print("'Compilation' complete :)")