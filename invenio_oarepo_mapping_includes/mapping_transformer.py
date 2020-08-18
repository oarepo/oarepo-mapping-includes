import json
import os

from deepmerge import always_merger, conservative_merger

base_merger = always_merger
inherited_merger = conservative_merger


def convert_props(includes, properties):
    # for each property, update its type and definition if needed
    for prop in properties.values():

        # get the type - it can be a simple type or an array (think of multiple inheritance)
        mapping_type = prop['type']
        if not isinstance(mapping_type, list):
            mapping_type = [mapping_type]

        # will contain merged parent types
        mpt_res = {}
        for mpt in mapping_type:
            # for each of the mapping type
            while True:
                # if there is a json pointer inside the type
                if '#' in mpt:
                    # get the resource and json pointer
                    resource, json_pointer = mpt.split('#', maxsplit=1)

                    # look it up in cache
                    mapping = includes.load_resource(resource, json_pointer)

                    # merge into mpt_res, overwriting any previously existing values
                    base_merger.merge(mpt_res, mapping)

                    # extract the new type
                    if mpt == mpt_res['type']:
                        raise ValueError('Infinite recursion in type %s detected' % mpt)

                    mpt = mpt_res['type']
                else:
                    # remember the last extracted type and break
                    mpt_res['type'] = mpt
                    break

        if len(mpt_res) > 1:
            # if there are more properties then just the ['type'], merge them but do not override what we have
            inherited_merger.merge(prop, mpt_res)

        # and set the type as it has not been overridden on the previous line
        prop['type'] = mpt_res['type']

        # and go recursively
        convert_props(includes, prop.get('properties', {}))


def process(includes, base_dir, filename):
    # load the file, convert its types and write it back into cache directory
    dest_file = os.path.join(base_dir, os.path.basename(filename))
    with open(filename) as f:
        mapping = json.load(f)

    convert_props(includes, mapping['mappings']['properties'])
    with open(dest_file, 'w') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=4)

    return dest_file


def mapping_transformer(source, app=None, **kwargs):
    includes = app.extensions['oarepo-mapping-includes']
    mappings = app.extensions['invenio-search'].mappings

    # create cache directory
    transformed_mappings_dir = os.path.join(app.instance_path, 'mappings')
    if not os.path.exists(transformed_mappings_dir):
        os.makedirs(transformed_mappings_dir)

    # and transform each mapping
    for k, v in list(mappings.items()):
        mappings[k] = process(includes, transformed_mappings_dir, v)
