import json
import os

from deepmerge import always_merger, conservative_merger

inherited_merger = conservative_merger


def process_type(prop, field, includes, add_field=True, root=None, content_pointer=None):
    # get the type - it can be a simple type or an array (think of multiple inheritance)
    mapping_type = prop.pop(field, None)
    if not mapping_type:
        return  # strange, should never happen

    if not isinstance(mapping_type, list):
        mapping_type = [mapping_type]

    # will contain merged parent types
    for mpt in mapping_type:
        # for each of the mapping type
        while True:
            # try to load the type
            mapping = includes.load_type(mpt, content=prop, root=root, content_pointer=content_pointer)

            if mapping:

                # merge into mpt_res, overwriting any previously existing values
                inherited_merger.merge(prop, mapping)

                # extract the new type
                new_type = prop.get('type', None)
                if not new_type:
                    break

                if mpt == new_type:
                    raise ValueError('Infinite recursion in type %s detected' % mpt)

                mpt = new_type
            else:
                # remember the last extracted type and break
                break

    # if included mappings do not add type, use the first one in the original type
    if add_field and field not in prop:
        prop[field] = mapping_type[0]


def convert_props(includes, properties, root, content_pointer):
    # for each property, update its type and definition if needed
    for name, prop in properties.items():
        prop_pointer = content_pointer + '/' + name
        process_type(prop, 'type', includes, True, root, prop_pointer)
        # and go recursively
        convert_props(includes, prop.get('properties', {}), root, prop_pointer + '/properties')
        convert_props(includes, prop.get('fields', {}), root, prop_pointer + '/fields')


def convert_extends(includes, el, root, content_pointer):
    for name, prop in el.items():
        if not isinstance(prop, dict):
            continue
        prop_pointer = content_pointer + '/' + name
        process_type(prop, 'oarepo:extends', includes, False, root=root, content_pointer=prop_pointer)
        # and go recursively
        convert_extends(includes, prop, root, prop_pointer)


def process(includes, base_dir, filename):
    # load the file, convert its types and write it back into cache directory
    dest_file = os.path.join(base_dir, os.path.basename(filename))
    with open(filename) as f:
        mapping = json.load(f)
    convert_extends(includes, mapping, root=mapping, content_pointer='')
    convert_props(includes, mapping['mappings']['properties'], mapping, '/mappings/properties')
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
