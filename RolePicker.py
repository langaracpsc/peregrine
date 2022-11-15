import discord

class Role():
    def __init__(self, id:str, name:str, emoji=None):
        self.id = id
        self.name = name
        self.emoji = emoji
    
    def toComponent(self):
        
        return discord.SelectOption(
            label=self.name, 
            value=self.id,
            emoji=self.emoji
        )
    
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name


# Defines a simple View that allows the user to use the Select menu.
class RolePicker(discord.ui.View):
    def __init__(self, interaction, roles=None):
        super().__init__(timeout=None)
        
        # FIRST YEAR COURSES
        roles = [
            Role("753708487070187651", "CPSC 1000"),
            Role("753708542917345281", "CPSC 1030"),
            Role("753708790477488210", "CPSC 1040"),
            Role("753708824233246955", "CPSC 1045"),
            Role("753708888213291138", "CPSC 1050"),
            Role("753709091867852822", "CPSC 1090"),
            Role("753709149782671475", "CPSC 1091"),
            Role("753709204253966428", "CPSC 1150"),
            Role("753709250714402816", "CPSC 1155"),
            Role("753709292690997298", "CPSC 1160"),
            Role("753709389323698176", "CPSC 1181"),
            Role("753709451407524011", "CPSC 1280"),
            Role("753709511386333244", "CPSC 1401"),
            Role("753692547863281805", "CPSC 1480"),
            Role("753709577723445259", "CPSC 1490"),
            Role("753710138619068537", "CPSC 1491"),
        ]
        self.add_item(Dropdown(roles, interaction, placeholder="First Year Courses:"))
        
        # SECOND YEAR COURSES
        roles = [
            Role("753710200631853096", "CPSC 2030"),
            Role("753710271389761667", "CPSC 2130"),
            Role("753710338754478201", "CPSC 2150"),
            Role("753710427535311089", "CPSC 2180"),
            Role("753710588617687171", "CPSC 2190"),
            Role("753710647367172217", "CPSC 2211"),
            Role("753710683484454973", "CPSC 2221"),
            Role("753710781199155210", "CPSC 2261"),
            Role("753710835930628278", "CPSC 2280"),
            Role("753710892943933612", "CPSC 2301"),
            Role("753711234309816511", "CPSC 2350"),
            Role("753711277024477185", "CPSC 2401"),
            Role("753711384721621012", "CPSC 2480"),
            Role("753711474991693974", "CPSC 2600"),
            Role("753711524924751988", "CPSC 2650"),
            Role("753711567748595893", "CPSC 2810"),
        ]
        self.add_item(Dropdown(roles, interaction, placeholder="Second Year Courses:"))
        
        # THIRD+FOURTH YEAR COURSES
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
        self.add_item(Dropdown(roles, interaction, placeholder="Third + Fourth Year Courses:"))
        
        # Program ROLES
        roles = [
            Role("946702905015152641", "🤖Computer Science"),
            Role("946704191634690100", "📚Computer Studies"),
            Role("946702429423013949", "📱Web and Mobile"),
            Role("946705220245790760", "📊Data Analytics"),
            Role("946708061257596969", "🌐Internet and Web Technology"),
            Role("946708684141129748", "🧬Bioinformatics"),
            Role("946702302784405554", "🏫Other Major"),
        ]
        self.add_item(Dropdown(roles, interaction, placeholder="Program"))
        
        roles = [
            Role("795817563430584351", "Langara"),
            Role("946701386672898048", "UBC"),
            Role("946701202501009459", "SFU"),
            Role("946700899793928233", "BCIT"),
        ]
        self.add_item(Dropdown(roles, interaction, placeholder="Institution",max=2))



class Dropdown(discord.ui.Select):
    def __init__(self, roles:list[Role], interaction:discord.Interaction, placeholder="No roles selected.",min=0,max=-1):
        if max == -1:
            max = len(roles)
        self.roles = roles
        
        # store all roles of user in a list (the id)
        user = interaction.user
        user_roles = []
        for role in user.roles:
            user_roles.append(str(role.id))
            
        # generate a list with components
        # each course is its own component
        # enable the component if the user has it
        options = []    
        for role in self.roles:
            comp: discord.SelectOption = role.toComponent()
            if str(role.id) in user_roles:
                comp.default = True
                
            #print(comp.value)
            options.append(comp)
        
        #print("USER ROLES:", user_roles)
            
        #options.append(discord.SelectOption(label="None", value="none", emoji="🚫"))
        
        # initiate the discord.Select
        super().__init__(
            placeholder=placeholder,
            min_values=min,
            max_values=max,
            options=options,
        )
        
    # callback when user is done with select menu
    async def callback(self, interaction: discord.Interaction):
        
        # make list of user roles
        user = interaction.user
        user_roles = []
        for role in user.roles:
            user_roles.append(str(role.id))
                   
        # iterate through each role the menu can change
        for role in self.roles:
            # if role selected AND role not already on user, add it
            if role.id in self.values and role.id not in user_roles:
                r = interaction.guild.get_role(int(role.id)) 
                await interaction.user.add_roles(r)
            # if role not selected AND role on user, remove it
            elif role.id not in self.values and role.id in user_roles:
                r = interaction.guild.get_role(int(role.id))
                await interaction.user.remove_roles(r)
        
        # removing this breaks the interaction???
        await interaction.response.send_message(f"Updated your roles!", ephemeral=True, delete_after=5)
        
        
