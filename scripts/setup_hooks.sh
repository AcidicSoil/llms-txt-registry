#!/bin/bash
HOOK_FILE=".git/hooks/pre-push"

echo "Installing pre-push hook..."

cat <<EOF > "$HOOK_FILE"
#!/bin/bash
# Task Master Registry - Pre-push Hook
# Validates that artifacts are updated if sources.json changed.

python3 scripts/refresh.py --check
RESULT=\$?

if [ \$RESULT -ne 0 ]; then
  echo "Error: Stale artifacts detected. Please run 'scripts/refresh.py' and commit the changes before pushing."
  exit 1
fi

exit 0
EOF

chmod +x "$HOOK_FILE"
echo "Hook installed successfully at $HOOK_FILE"
