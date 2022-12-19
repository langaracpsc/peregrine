"""
A collection of methods to implement email verification.
Collects an email address from user, checks its validity,
then sends a confirmation email with code to that email.
User then brings the code back and is given the email-verified role.

Not currently used and I struggle to see how this will be useful,
but it was fun to code :)
"""

import sqlite3
import discord
import secrets
import time
import requests
import json


class EmailManager():
    def __init__(self, database_type, database_name, email_sender_webhook):
        
        if database_type != "sqlite3":
            raise Exception("Other database types are not supported.")
        
        self.database_type = database_type
        self.database_name = database_name
        
        # currently using integromat so i don't have to dig through
        # the gmail api - this can be changed in the future.
        self.webhook = email_sender_webhook
        self.role:discord.Role = None
        self.logging:discord.TextChannel = None
        self.MAX_EMAIL_ATTEMPTS = 50
        self.MAX_CODE_ATTEMPTS = 5
         
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()
        
        # create table if it does not exist
        try:
            self.cursor.execute("CREATE TABLE emails(datetime, discord_id, email, email_attempts, confirmation_code, code_attempts, status)")
        except:
            pass
        
        

    def generate_code(self):
        return secrets.token_urlsafe(16)
        
    # method to send verification code and handle other cases.
    async def start_verification(self, email, interaction:discord.Interaction):
        
        search = self.cursor.execute("SELECT * FROM emails WHERE email=?", (email,))
        if self.cursor.fetchone() is not None:
            await interaction.response.send_message("Email already in use.", ephemeral=True)
            return
            
        if not email.endswith("@mylangara.ca"):
            await interaction.response.send_message(f"`{email}` is not a valid email. Please use an address that ends in `@mylangara.ca`.", ephemeral=True)
            return
        
        
        template = (
            int(time.time()),
            interaction.user.id,
            email,
            0,
            self.generate_code(),
            0,
            "awaiting verification"
        )
        
        search = self.cursor.execute("SELECT * FROM emails WHERE discord_id=?", (template[1],))
        user_info = search.fetchone()
                
        # create row if user did not exist
        if user_info is None:
            self.cursor.execute("INSERT INTO emails VALUES(?, ?, ?, ?, ?, ?, ?)", template)
            self.connection.commit()
            
        # limit to 2 emails sent max so we don't get banned from langara
        elif user_info[3] > self.MAX_EMAIL_ATTEMPTS:
            await interaction.response.send_message("You have been ratelimited. Please contact a moderator.", ephemeral=True)
            return
        
        # otherwise, update row in database
        else:
            id = template[1]
            self.update_field(id, "datetime", template[0])
            self.update_field(id, "email", template[2])
            self.update_field(id, "email_attempts", user_info[3]+1) 
            self.update_field(id, "confirmation_code", template[4])
            self.update_field(id, "code_attempts", 0)
         
        # email is currently handled by an integromat webhook bacause i didn't want to dig through the
        # gmail api :)   
        send = {
            "email": template[2],
            "token": template[4]
        }
        requests.post(self.webhook, data=json.dumps(send), headers={'Content-Type': 'application/json'})
        await interaction.response.send_message("Please check your inbox.", ephemeral=True)
        
        # LOG EMAIL SENT
        log = discord.Embed()
        log.description = f"Verification email sent to `{template[2]}`"
        log.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        log.set_footer(text=f"User ID: {interaction.user.id}")
        
        await self.logging.send(embed=log)

    
    # method to check verification code and handle it
    async def check_verification_code(self, code, interaction:discord.Interaction):
        
        id = interaction.user.id
        search = self.cursor.execute("SELECT * FROM emails WHERE discord_id=?", (id,))
        user_info = search.fetchone()
        
        if user_info is None:
            await interaction.response.send_message("Enter your email first.", ephemeral=True)
        
        elif user_info[5] >= self.MAX_CODE_ATTEMPTS:
            await interaction.response.send_message("You have been ratelimited. Please contact a moderator.", ephemeral=True)

        elif code == user_info[4]:            
            self.update_field(id, "datetime", int(time.time()))
            self.update_field(id, "status", "verified")
            
            await interaction.user.add_roles(self.role)
            await interaction.response.send_message("Email verified!", ephemeral=True)

        else:
            self.update_field(id, "code_attempts", user_info[5]+1)
            
            await interaction.response.send_message("Code incorrect.", ephemeral=True)
        
    
    # method to modify SQL table
    def update_field(self, discord_id, field, value):
        sql = f"UPDATE emails SET {field} = ? WHERE discord_id = ?"
        values = (value, discord_id)
        
        self.cursor.execute(sql, values)
        self.connection.commit()
        
    def clear_data(self, discord_id):
        self.cursor.execute("DELETE FROM emails WHERE discord_id=?", (discord_id,))
        self.connection.commit()
    
        
