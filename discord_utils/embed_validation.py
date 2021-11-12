import discord

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
def validate_embed(embed:discord.Embed):
    embed_ok = True
    if (validate_embed_total_length(embed) == False):
        embed_ok = False
    if (validate_embed_title(embed.title) == False):
        embed_ok = False
    if (validate_embed_description(embed.description) == False):
        embed_ok = False
    if (validate_embed_fields(embed.fields) == False):
        embed_ok = False
    if (validate_embed_footer(embed.footer) == False):
        embed_ok = False
    if (validate_embed_author(embed.author) == False):
        embed_ok = False        
    return embed_ok

def validate_embed_total_length(embed:discord.Embed):
    if (len(embed) > 6000):
        print(f'Embed size too long: {len(embed)}')
        return False
    return True

def validate_embed_title(title:discord.Embed.title):
    if (str(title) != 'Embed.Empty'):
        if (len(title) > 256):
            print(f'title too long: {len(title)}')
            return False
    return True

def validate_embed_description(description:discord.Embed.description):
    if (str(description) != 'Embed.Empty'):
        if (len(description) > 4096):
            print(f'description too long: {len(description)}')
            return False
    return True

def validate_embed_fields(fields:discord.Embed.fields):
    fields_ok = True
    if (validate_embed_no_of_fields(fields) == False):
        fields_ok = False
    if (validate_embed_field_names(fields) == False):
        fields_ok = False
    if (validate_embed_field_value(fields) == False):
        fields_ok = False
    return fields_ok

def validate_embed_no_of_fields(fields:discord.Embed.fields):
    if (len(fields) > 25):
        print(f'too many fields!: {len(fields)}')
        return False
    return True

def validate_embed_field_names(fields:discord.Embed.fields):
    fields_name = []
    fields_name.extend([field.name for field in fields])
    for name in fields_name:
        if (len(name) > 256):
            print(f'field.name too long: {len(name)}')
            return False

def validate_embed_field_value(fields:discord.Embed.fields):
    fields_value = []
    fields_value.extend([field.value for field in fields])
    for value in fields_value:
        if (len(value) > 1024):
            print(f'field.value too long: {len(value)}')
            return False
    return True

def validate_embed_footer(footer:discord.Embed.footer):
    if (str(footer.text) != 'Embed.Empty'):
        if (len(footer.text) > 2048):
            print(f'footer.text too long: {len(footer.text)}')
            return False
    return True

def validate_embed_author(author:discord.Embed.author):
    if (str(author.name) != 'Embed.Empty'):
        if (len(author.name) > 256):
            print(f'author.name too long: {len(author.name)}')
            return False
    return True
