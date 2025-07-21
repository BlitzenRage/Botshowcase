# THIS COMMAND BANS ANY PERSON FROM A DISCORD WHEN RUN

# This is the main command, it contains the fields alongside the appeals choices.
@bot.tree.command(name="blacklist", description="Add a username to blacklists.", guild=guild)
@app_commands.describe(
    user="Username to add to the blacklist",
    discord_user="Discord User",
    reason="Reason for Blacklist",
    type="Type of Blacklist",
    duration="Number of months"
)

# Defines choices for the field in type.
@app_commands.choices(
    type=[
        app_commands.Choice(name="Appealable", value="appealable"),
        app_commands.Choice(name="Unappealable", value="unappealable")
    ]
)

# This handles making sure that the user can actually use this command, fetch the blacklist channel, sends embed, fetches the user, and bans him.
async def blacklist(interaction: discord.Interaction, user: str, discord_user: discord.Member, reason: str, type: app_commands.Choice[str], duration: str):
    allowed_roles = {1384665316361240658, 1384527460816654416, 1384527702010101770, 1384525671572836352, 1384324243856297994, 1384324121927614547, 1384323937986547813, 1384323877940891678}
    user_roles = {role.id for role in interaction.user.roles}

    if not user_roles.intersection(allowed_roles):
        await interaction.response.send_message("You don't have the required role to use this command.", ephemeral=True)
        return
    await interaction.response.defer(ephemeral=True)

    try:
        channel = await bot.fetch_channel(TARGET_CHANNEL_ID_2)
    except discord.NotFound:
        await interaction.followup.send("Target channel not found.", ephemeral=True)
        return
    
    try:
        color=discord.Color.dark_red()
        embed = discord.Embed(
            title=str(user),
            color=discord.Color.dark_red(),
            description=(
                f"**Reason**\n"
                f"{reason}\n\n"
                f"**Type**\n"
                f"{type.name}\n\n"
                f"**Duration**\n"
                f"{duration} months"
            )
        )

        embed.set_author(name="Britannic Foreign Office")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1384527005080621237/1386709333542178958/RGBS_Header_1.png?ex=685ab134&is=68595fb4&hm=573585dfcb27255b12f5895aa3a79bcb2d12e9fd7fe665dd1543b5eb94f25559&")
        embed.set_footer(text="Official Blacklist of the BFO")
        await channel.send(embed=embed)
        await interaction.followup.send(f"{user} has been blacklisted for '{reason}'\nType: **{type.name}**", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"Error sending blacklist: {e}", ephemeral=True)

    member = discord.utils.find(member = discord_user)
    
    if member:
        try:
            await interaction.guild.ban(member, reason=f"Blacklisted: {reason}")
            ban_msg = f"{member.mention} has been banned from the server."
        except discord.Forbidden:
            ban_msg = "I don't have permission to ban that member."
        except Exception as e:
            ban_msg = f"Failed to ban member: {e}"
    else:
        ban_msg = "User not found in this server."

    await interaction.followup.send(f"Blacklist sent!\n{ban_msg}", ephemeral=True)
