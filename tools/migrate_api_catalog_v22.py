#!/usr/bin/env python3
"""Compatibility shim: V24 supersedes the V22 public generator entry point."""
from migrate_api_catalog_v24 import write_generated

if __name__ == "__main__":
    print("V22 API migration command is deprecated; using V24 generator.")
    write_generated()
