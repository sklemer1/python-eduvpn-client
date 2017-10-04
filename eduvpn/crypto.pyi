# python-eduvpn-client - The GNU/Linux eduVPN client and Python API
#
# Copyright: 2017, The Commons Conservancy eduVPN Programme
# SPDX-License-Identifier: GPL-3.0+

def gen_code_verifier(length: int = ...): ...
def gen_code_challenge(code_verifier): ...
def make_verifier(key: str) -> nacl.signing.VerifyKey: ...
