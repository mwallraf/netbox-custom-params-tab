FROM netboxcommunity/netbox:v4.6-5.0.1

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy plugin source and install as editable so volume-mounted edits are live
COPY . /opt/netbox-custom-field-profiles/
RUN uv pip install --python /opt/netbox/venv/bin/python --no-cache-dir -e /opt/netbox-custom-field-profiles/
