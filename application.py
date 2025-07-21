# THIS CODE IS FOR ACCEPT AND DENY BUTTONS

class ApplicationReviewView(View):
    def __init__(self, applicant: discord.User, role_ids: list[int], reviewer_role_id: int):
        super().__init__(timeout=None)
        self.applicant = applicant
        self.role_ids = role_ids
        self.reviewer_role_id = reviewer_role_id

    def is_allowed(self, member: discord.Member):
        return self.reviewer_role_id in [role.id for role in member.roles]

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.success)
    async def accept_button(self, interaction: discord.Interaction, button: Button):
        if not self.is_allowed(interaction.user):
            await interaction.response.send_message("You don’t have permission to do this.", ephemeral=True)
            return

        member = interaction.guild.get_member(self.applicant.id)
        if not member:
            await interaction.response.send_message("User not found in the server.", ephemeral=True)
            return

        roles_given = []
        for rid in self.role_ids:
            role = interaction.guild.get_role(rid)
            if role:
                await member.add_roles(role)
                roles_given.append(role.mention)

        await self.applicant.send(f"You have been accepted and given the roles: {', '.join(roles_given)}")
        await interaction.message.edit(content="Application accepted.", view=None)
        await interaction.response.send_message("User has been accepted and notified.", ephemeral=True)

    @discord.ui.button(label="Deny", style=discord.ButtonStyle.danger)
    async def deny_button(self, interaction: discord.Interaction, button: Button):
        if not self.is_allowed(interaction.user):
            await interaction.response.send_message("You don’t have permission to do this.", ephemeral=True)
            return

        await self.applicant.send("Unfortunately, your application has been denied.")
        await interaction.message.edit(content="Application denied.", view=None)
        await interaction.response.send_message("User has been denied and notified.", ephemeral=True)
