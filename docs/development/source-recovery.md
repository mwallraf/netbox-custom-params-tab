> **Historical maintainer evidence.** This file contains the original recovery manifest,
> consumed by `scripts/source_snapshot.py`. Hashes and historical paths are intentionally unchanged.
> For current implementation details, see [architecture.md](architecture.md).

# Source recovery

Original renamed working snapshot; feature history: `42ad9c2`.

```json
{
  "version": 1,
  "files": {
    ".dockerignore": "21ba6757e92077c4fbf1f99c171cc81b8583a055837cacec95f700c781ad9bdf",
    "Makefile": "38010f49a47368b1bb8f29f7945ccf59d344930417d7144b9f89025163a46db3",
    "docker/Dockerfile": "9590d955be81ef542e5ab350056a8f104e61e2fae47e2d60b7a9da68efbe18dd",
    "docker/configuration.py": "61f7403beaefc94f7234abe98a25f664858ee799f68196e9bb595b1785e0eb32",
    "docker-compose.yml": "b46285fef527332e666d071d5538609582dd09bc956d642ceeee504ca90dfd40",
    "netbox_custom_field_profiles/__init__.py": "d85ddf2a284b5d6ad75e2ccef71710259e8eefa3c7e77b4997a917ac6fb79708",
    "netbox_custom_field_profiles/api/__init__.py": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "netbox_custom_field_profiles/api/serializers.py": "47477827ba351c62fc679bcc503916d53097f0b4c8ff5d315a408eac296d8aac",
    "netbox_custom_field_profiles/api/urls.py": "529c998829032bbda4152120ca06845c04f31272df897cfa9ef6a052fc372cf6",
    "netbox_custom_field_profiles/api/views.py": "b7439ca64bbb7dbc1e38cf3cf9473a3124c327ffe873cc11e96ef8139b30d6c5",
    "netbox_custom_field_profiles/forms.py": "3bcf5dc0eca23968c8ed37333e72a4fabd021cd0745243b4929d40d851935699",
    "netbox_custom_field_profiles/management/__init__.py": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "netbox_custom_field_profiles/management/commands/__init__.py": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "netbox_custom_field_profiles/management/commands/make_plugin_migrations.py": "25788519f60b544c8488956f1d0c96586278bba613ad25289de2fb9083964e65",
    "netbox_custom_field_profiles/migrations/0001_initial.py": "f5f735202e4525d651db506b83acae39664340243e74c8dbfdf81ebc26b81632",
    "netbox_custom_field_profiles/migrations/__init__.py": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "netbox_custom_field_profiles/models.py": "24820736b80e45d3f9f78e448901d7633f6a04f6809f097a9c4949cd185e0df6",
    "netbox_custom_field_profiles/navigation.py": "79f26e7cb1f5c2cd4d60cd3c40b489db9530facc895fb51ac18ca13f213c9277",
    "netbox_custom_field_profiles/tables.py": "329032b47438b4922e77f3b420396c207c3850aae39e1b6c1c74cac5a6af3fda",
    "netbox_custom_field_profiles/template_content.py": "e5cefd34175ba02ae203a0314f5bd98fd91b02c082fbe2725503961d2ca39f88",
    "netbox_custom_field_profiles/templates/netbox_custom_field_profiles/customtabconfig_delete.html": "6bb3cfb4f544293de791c143dc8846b539fc7120d8dba1ccf1056e4d7df393a7",
    "netbox_custom_field_profiles/templates/netbox_custom_field_profiles/customtabconfig_edit.html": "92ccd275d08d49ff4583cc546c4bbb58e848d9753d41191c5cdb27f7273abbbd",
    "netbox_custom_field_profiles/templates/netbox_custom_field_profiles/tab_panel.html": "d474e9521aca4233f7d7cecc2c657c3b75967f95577dfa354782fd5d30594907",
    "netbox_custom_field_profiles/templatetags/__init__.py": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "netbox_custom_field_profiles/templatetags/customtab_tags.py": "5800e72f513718fbf5bac0b72fb471431d3ae06da5103d8dc58dd05dadb7c1e2",
    "netbox_custom_field_profiles/urls.py": "e6a870a525d99d4749785f6a21d69f3d6dfa5565d5970cd4b06b9a6006684175",
    "netbox_custom_field_profiles/views.py": "3eda1698213790ccd32d58a039d3967ae1f7eaf090e0fb0bb1e1b63098c46669",
    "pyproject.toml": "cf246217df06da2c22c55b046e228fba9705f8e85577a3021f20c1329953a9e1",
    "pytest.ini": "2db414f152d780e560669d4c727ba696608c69f49b5a7608477b4cc5257238b5",
    "testing/__init__.py": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "testing/settings.py": "b12422142699a5fae7fef570826c9e448f4e603eed2b167df7b38c82b64807f3",
    "tests/__init__.py": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "tests/conftest.py": "15b4a889a4d740ba2bc41536115896e9337155bc1b1447ad7099ea7546621e68",
    "tests/test_forms.py": "1371f3f803747b6cfe26599ad7bbd7a311f3c7ad74229fed68eed0fea35863f6",
    "tests/test_models.py": "428496dea392fdeb5fe2e66045a4aa8efd028ced1010ca5d90cd0defa6682f3b",
    "tests/test_tables.py": "f5fc0d4741dcaee24ec5669724480195b60727ea34ad597af2b122ef07dffd95",
    "tests/test_template_content.py": "27dc781be276fc261912c080a44ef608284ad0580dbec5e5a69c1f6361f2e25a",
    "tests/test_views.py": "6b2904400a91a04cbfc36840fde55bd184ea008b42570630d88e350697bb1730"
  }
}
```

Canonical reconciliation commit: `4dba67e` (merge retaining `42ad9c2`).
Original snapshot retained unchanged at ignored `.recovery/implement-plugin`; no prune was run.
Only the normal checkout is registered. Current root docs/planning survived the merge unchanged.
Initial root status had the old-name historical spec deleted and three .DS_Store files.
The spec deletion is retained; its renamed content already exists unchanged.
Verify original bytes after later edits with `python3 scripts/source_snapshot.py verify --commit 4dba67e`.
