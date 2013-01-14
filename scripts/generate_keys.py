#!/usr/bin/env python2

import rsa
import os
import os.path
import argparse
import json

# default values
PUBLIC_KEY_FILENAME = "public.pem"
PRIVATE_KEY_FILENAME = "private.pem"
KEY_SIZE = 512

DJANGO_SETTINGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../src/net_portal")
RSA_SETTINGS_FILENAME = "rsa_settings.json"

def generate_keys(size):
    return rsa.newkeys(size)

def create_gitignore(to_ignore):
    gitignore_exists = os.path.isfile(".gitignore")
    with open(".gitignore", 'a') as f:
        if gitignore_exists:
            f.write("\n")
        else:
            to_ignore.append(".gitignore")
        f.write("{0}\n".format('\n'.join(to_ignore)))

def save_keys(public_key, private_key, public_key_filename, private_key_filename, output_dir):
    exists = os.path.exists(output_dir)
    if exists and not os.path.isdir(output_dir):
        raise OSError("{0} already exists and is not a directory".format(output_dir))
    if not exists:
        os.makedirs(output_dir, 0755)
    old_dir = os.getcwd()
    os.chdir(output_dir)
    for filename in [private_key_filename, public_key_filename]:
        if os.path.exists(private_key_filename):
            raise OSError("{0} already exists in directory {1}".format(filename, output_dir))

    with open(public_key_filename, 'w') as f:
        f.write(public_key.save_pkcs1())
    with open(private_key_filename, 'w') as f:
        f.write(private_key.save_pkcs1())
    create_gitignore([public_key_filename, private_key_filename])

    output_dir_full_path = os.getcwd()
    public_key_full_path = os.path.join(output_dir_full_path, public_key_filename)
    private_key_full_path = os.path.join(output_dir_full_path, private_key_filename)
    os.chdir(os.path.join(old_dir, DJANGO_SETTINGS_DIR))

    with open(RSA_SETTINGS_FILENAME, "w") as f:
        f.write(json.dumps({"public_key_path": public_key_full_path, "private_key_path": private_key_full_path}))

    create_gitignore([RSA_SETTINGS_FILENAME])

class AddPemAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if not values.endswith(".pem"):
            values = "{0}.pem".format(values)
        setattr(namespace, self.dest, values)

def make_parser():
    parser = argparse.ArgumentParser(description='Generate RSA keys for encryption and decryption in net portal.')
    parser.add_argument("output_dir")
    parser.add_argument("-s", "--key-size", default=KEY_SIZE, type=int)
    parser.add_argument("--public-key",  action=AddPemAction, default=PUBLIC_KEY_FILENAME)
    parser.add_argument("--private-key", action=AddPemAction, default=PRIVATE_KEY_FILENAME)
    return parser

if __name__ == '__main__':
    parser = make_parser()
    data = parser.parse_args()

    (public_key, private_key) = generate_keys(data.key_size)
    try:
        save_keys(public_key, private_key, data.public_key, data.private_key, data.output_dir)
        print "Key generated in {0}".format(data.output_dir)
    except OSError as e:
        print "Impossible to save keys: {0}.".format(e.message)
