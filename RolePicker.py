import discord

# custom class that represents a role
class Role():
    def __init__(self, id:int, name:str, emoji:str=None):
        self.id = id
        self.name = name
        self.emoji = emoji
        
        self.component = discord.SelectOption(
            label=name, 
            value=self.id, 
            emoji=self.emoji
        )
    
# Defines a simple View that allows the user to use the Select menu.
class RolePicker(discord.ui.View):
    def __init__(self, interaction, roles=None):
        super().__init__(timeout=None)
        
        # first year courses
        roles = [
            Role("753708542917345281", "CPSC 1030"),
            Role("753708824233246955", "CPSC 1045"),
            Role("753708888213291138", "CPSC 1050"),
            Role("753709149782671475", "CPSC 1091"),
            Role("753709204253966428", "CPSC 1150"),
            Role("753709250714402816", "CPSC 1155"),
            Role("753709292690997298", "CPSC 1160"),
            Role("753709389323698176", "CPSC 1181"),
            Role("753709451407524011", "CPSC 1280"),
            Role("753692547863281805", "CPSC 1480"),
        ]
        self.add_item(Dropdown(roles, interaction, placeholder="First Year Courses"))
        
        # second year courses
        roles = [
            Role("753710200631853096", "CPSC 2030"),
            Role("753710271389761667", "CPSC 2130"),
            Role("753710338754478201", "CPSC 2150"),
            Role("753710588617687171", "CPSC 2190"),
            Role("753710647367172217", "CPSC 2211"),
            Role("753710683484454973", "CPSC 2221"),
            Role("753710835930628278", "CPSC 2280"),
            Role("753711234309816511", "CPSC 2350"),
            Role("753711474991693974", "CPSC 2600"),
            Role("753711524924751988", "CPSC 2650"),
            Role("753711567748595893", "CPSC 2810")
        ]
        self.add_item(Dropdown(roles, interaction, placeholder="Second Year Courses"))
        
        # Bioinformatics / Data Analysis Courses
        roles = [
            Role("753711634320588883", "CPSC 3260"),
            Role("753711736368005261", "CPSC 3280"),
            Role("753711841259159574", "CPSC 4160"),
            Role("753711958854860932", "CPSC 4260"),
            Role("753712074101620858", "CPSC 4800"),
            Role("753712150505324566", "CPSC 4810"),
            Role("753712210815221791", "CPSC 4820"),
            Role("753712291794649108", "CPSC 4830"),
        ]
        self.add_item(Dropdown(roles, interaction, placeholder="Bioinformatics / Data Analytics Courses"))
        
        # Programs
        roles = [
            Role("946702905015152641", "Computer Science", "🤖"),
            Role("946704191634690100", "Computer Studies", "📚"),
            Role("946702429423013949", "Web and Mobile", "📱"),
            Role("946705220245790760", "Data Analytics", "📊"),
            Role("946708061257596969", "Internet and Web Technology", "🌐"),
            Role("946708684141129748", "Bioinformatics", "🧬"),
            Role("946702302784405554", "Other Major", "🏫"),
        ]
        self.add_item(Dropdown(roles, interaction, placeholder="Program"))
        
        # Institutions
        roles = [
            Role("795817563430584351", "Langara"),
            Role("946701386672898048", "UBC"),
            Role("946701202501009459", "SFU"),
            Role("946700899793928233", "BCIT"),
        ]
        self.add_item(Dropdown(roles, interaction, placeholder="Institution"))



class Dropdown(discord.ui.Select):
    def __init__(self, roles:list[Role], interaction:discord.Interaction, placeholder=None,min=0,max=-1):
        
        if max == -1:
            max = len(roles)
        self.roles:list[Role] = roles
            
        # generate a list of components
        # each component represents 1 course
        # enable the component if the user has the role
        roleComponents = []
        
        for role in roles:
            if interaction.user.get_role(int(role.id)) != None:
                role.component.default = True
            roleComponents.append(role.component)
                              
        # initiate the discord.Select
        super().__init__(
            placeholder=placeholder,
            min_values=min,
            max_values=max,
            options=roleComponents,
        )
        
    # callback when user submits the select menu
    async def callback(self, interaction: discord.Interaction):
                
        add, rem = [], []
        
        
        # you could use a list comprehension here but those become messy quickly 
        # only modifying roles that need to modified speeds up the interaction by a bit .-.       
        for role in self.roles:
            r:discord.Role = interaction.guild.get_role(int(role.id))
            
            if role.id in self.values and r not in interaction.user.roles:
                add.append(role)
                
            if role.id not in self.values and r in interaction.user.roles:
                rem.append(role)
        
        # these methods look for an id property in whatever you pass to them
        # * unpacks lists
        await interaction.user.add_roles(*add, reason="role menu")
        await interaction.user.remove_roles(*rem, reason="role menu")
        
        await interaction.response.send_message(f"Updated your roles!", ephemeral=True, delete_after=5)
        
        
