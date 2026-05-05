FROM netboxcommunity/netbox:v4.6-5.0.0

USER root

# Copy plugin source and install as editable so volume-mounted edits are live
COPY . /opt/netbox-custom-params-tab/
RUN pip install --no-cache-dir -e /opt/netbox-custom-params-tab/

USER unit
