FROM ghcr.io/netbox-community/netbox:v4.2-latest

USER root

# Copy plugin source and install as editable so volume-mounted edits are live
COPY . /opt/netbox-custom-params-tab/
RUN pip install --no-cache-dir -e /opt/netbox-custom-params-tab/

USER unit
