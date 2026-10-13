#!/usr/bin/env python3
"""Make dart:io on Android also trust the additional root CAs.

Usage: patch_security_context.py <dart_sdk_root> <roots.pem>

Dart (3.9) compiles runtime/bin/security_context_linux.cc for both Linux and
Android. On Android, TrustBuiltinRoots() loads /system/etc/security/cacerts
only. This script injects a helper that also adds the PEM bundle to the
context's X509 store, and calls it from the Android branch. It fails loudly
if the upstream file no longer looks the way we expect.
"""
import pathlib
import sys

root, pem_path = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
target = root / "runtime/bin/security_context_linux.cc"
src = target.read_text()
if "AddExtraRoots" in src:
    sys.exit("already patched")

pem = pem_path.read_text().strip()
literal = "\n".join('    "%s\\n"' % line for line in pem.splitlines())

helper = f'''
// Added by the engine build: additional root CAs.
static const char kExtraRoots[] =
{literal};

static void AddExtraRoots(SSL_CTX* ctx) {{
  X509_STORE* store = SSL_CTX_get_cert_store(ctx);
  BIO* bio = BIO_new_mem_buf(kExtraRoots, -1);
  if (store == nullptr || bio == nullptr) {{
    if (bio != nullptr) BIO_free(bio);
    return;
  }}
  while (X509* cert = PEM_read_bio_X509(bio, nullptr, nullptr, nullptr)) {{
    X509_STORE_add_cert(store, cert);  // duplicates are harmless
    X509_free(cert);
  }}
  BIO_free(bio);
}}
'''

def replace_once(text, old, new):
    if text.count(old) != 1:
        sys.exit(f"anchor not found exactly once: {old!r}")
    return text.replace(old, new)

src = replace_once(src, "#include <openssl/bio.h>\n",
                   "#include <openssl/bio.h>\n#include <openssl/pem.h>\n")
src = replace_once(src, "namespace dart {\nnamespace bin {\n",
                   "namespace dart {\nnamespace bin {\n" + helper)
src = replace_once(src, "    LoadRootCertCache(android_cacerts);\n    return;\n",
                   "    LoadRootCertCache(android_cacerts);\n"
                   "    AddExtraRoots(context());\n    return;\n")
target.write_text(src)
print("patched", target)
