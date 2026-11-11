FROM netboxcommunity/netbox:v4.7.4-5.1.1
USER root
COPY pyproject.toml README.md LICENSE /opt/netbox-custom-field-profiles/
COPY netbox_custom_field_profiles /opt/netbox-custom-field-profiles/netbox_custom_field_profiles
RUN uv pip install --python /opt/netbox/venv/bin/python --no-deps --editable /opt/netbox-custom-field-profiles
# The upstream image collected static files before this plugin was installed.
# Its web server serves STATIC_ROOT, not the bind-mounted plugin source tree.
COPY netbox_custom_field_profiles/static/ /opt/netbox/netbox/static/
USER netbox
