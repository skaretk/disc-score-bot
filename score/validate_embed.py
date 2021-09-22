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
class ValidateEmbed():
    def __init__(self , embed:discord.Embed=None):
        self.embed = embed
    
    def validate(self):
        embed_ok = True
        if (self.validate_total_length() == False):
            embed_ok = False
        if (self.validate_title() == False):
            embed_ok = False
        if (self.validate_description() == False):
            embed_ok = False
        if (self.validate_fields() == False):
            embed_ok = False
        if (self.validate_footer() == False):
            embed_ok = False
        if (self.validate_author() == False):
            embed_ok = False        
        return embed_ok

    def validate_total_length(self):
        if (len(self.embed) > 6000):
            print(f'Embed size too long: {len(self.embed)}')
            return False
        return True

    def validate_title(self):
        if (str(self.embed.title) != 'Embed.Empty'):
            if (len(self.embed.title) > 256):
                print(f'description too long: {len(self.embed.description)}')
                return False
        return True

    def validate_description(self):
        if (str(self.embed.description) != 'Embed.Empty'):
            if (len(self.embed.description) > 4096):
                print(f'description too long: {len(self.embed.description)}')
                return False
        return True
    
    def validate_fields(self):
        fields_ok = True
        if (self.validate_no_of_fields() == False):
            fields_ok = False
        if (self.validate_field_names() == False):
            fields_ok = False
        if (self.validate_field_value() == False):
            fields_ok = False
        return fields_ok

    def validate_no_of_fields(self):
        if (len(self.embed.fields) > 25):
            print(f'too many fields!: {len(self.embed.fields)}')
            return False
        return True
    
    def validate_field_names(self):
        fields_name = []
        fields_name.extend([field.name for field in self.embed.fields])
        for name in fields_name:
            if (len(name) > 256):
                print(f'field.name too long: {len(name)}')
                return False

    def validate_field_value(self):
        fields_value = []
        fields_value.extend([field.value for field in self.embed.fields])
        for value in fields_value:
            if (len(value) > 1024):
                print(f'field.value too long: {len(value)}')
                return False
        return True

    def validate_footer(self):
        if (str(self.embed.footer.text) != 'Embed.Empty'):
            if (len(self.embed.footer.text) > 2048):
                print(f'footer.text too long: {len(self.embed.footer.text)}')
                return False
        return True

    def validate_author(self):
        if (str(self.embed.author.name) != 'Embed.Empty'):
            if (len(self.embed.author.name) > 256):
                print(f'author.name too long: {len(self.embed.author.name)}')
                return False
        return True
