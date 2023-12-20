import nextcord

# +-------------+------------------------+
# |    Field    |         Limit          |
# +-------------+------------------------+
# | length      | 6000 characters        |
# | title       | 256 characters         |
# | description | 4096 characters*       |
# | fields      | Up to 25 field objects |
# | field.name  | 256 characters         |
# | field.value | 1024 characters        |
# | footer.text | 2048 characters        |
# | author.name | 256 characters         |
# +-------------+------------------------+
def validate_embed(embed:nextcord.Embed):
    """Validate the embed"""
    embed_ok = True
    if validate_embed_total_length(embed) is False:
        embed_ok = False
    if validate_embed_title(embed.title) is False:
        embed_ok = False
    if validate_embed_description(embed.description) is False:
        embed_ok = False
    if validate_embed_fields(embed.fields) is False:
        embed_ok = False
    if validate_embed_footer(embed.footer) is False:
        embed_ok = False
    if validate_embed_author(embed.author) is False:
        embed_ok = False
    return embed_ok

def validate_embed_total_length(embed:nextcord.Embed):
    """Validate the total length of the embed"""
    if len(embed) > 6000:
        print(f'Embed size too long: {len(embed)}')
        return False
    return True

def validate_embed_title(title:nextcord.Embed.title):
    """Validate the embed title"""
    if str(title) != 'Embed.Empty':
        if len(title) > 256:
            print(f'title too long: {len(title)}')
            return False
    return True

def validate_embed_description(description:nextcord.Embed.description):
    """Validate the embed description"""
    if str(description) != 'Embed.Empty':
        if len(description) > 4096:
            print(f'description too long: {len(description)}')
            return False
    return True

def validate_embed_fields(fields:nextcord.Embed.fields):
    """Validate the embed fields"""
    fields_ok = True
    if validate_embed_no_of_fields(fields) is False:
        fields_ok = False
    if validate_embed_field_names(fields) is False:
        fields_ok = False
    if validate_embed_field_value(fields) is False:
        fields_ok = False
    return fields_ok

def validate_embed_no_of_fields(fields:nextcord.Embed.fields):
    """Validate the number of fields"""
    if len(fields) > 25:
        print(f'too many fields!: {len(fields)}')
        return False
    return True

def validate_embed_field_names(fields:nextcord.Embed.fields):
    """Validate the embed field names"""
    fields_name = []
    fields_name.extend([field.name for field in fields])
    for name in fields_name:
        if len(name) > 256:
            print(f'field.name too long: {len(name)}')
            return False
    return True

def validate_embed_field_value(fields:nextcord.Embed.fields):
    """Validate the embed fields value"""
    fields_value = []
    fields_value.extend([field.value for field in fields])
    for value in fields_value:
        if len(value) > 1024:
            print(f'field.value too long: {len(value)}')
            return False
    return True

def validate_embed_footer(footer:nextcord.Embed.footer):
    """Validate the embed footer"""
    if footer.text is not None:
        if str(footer.text) != 'Embed.Empty':
            if len(footer.text) > 2048:
                print(f'footer.text too long: {len(footer.text)}')
                return False
    return True

def validate_embed_author(author:nextcord.Embed.author):
    """Validate the embed author"""
    if author.name is not None:
        if str(author.name) != 'Embed.Empty':
            if len(author.name) > 256:
                print(f'author.name too long: {len(author.name)}')
                return False
    return True
