import discord
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")

UNVERIFIED_ROLE = "Unverified"
VERIFIED_ROLE = "Verified"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


class VerifyButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="✅ Verify",
        style=discord.ButtonStyle.green,
        custom_id="verify_button"
    )
    async def verify(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        member = interaction.user
        guild = interaction.guild

        unverified = discord.utils.get(
            guild.roles,
            name=UNVERIFIED_ROLE
        )

        verified = discord.utils.get(
            guild.roles,
            name=VERIFIED_ROLE
        )

        if verified in member.roles:
            await interaction.response.send_message(
                "Već si verifikovan!",
                ephemeral=True
            )
            return

        if unverified:
            await member.remove_roles(unverified)

        if verified:
            await member.add_roles(verified)

        await interaction.response.send_message(
            "✅ Uspešno si verifikovan!",
            ephemeral=True
        )


@bot.event
async def on_ready():
    print(f"Bot je online kao {bot.user}")
    bot.add_view(VerifyButton())


@bot.event
async def on_member_join(member):

    role = discord.utils.get(
        member.guild.roles,
        name=UNVERIFIED_ROLE
    )

    if role:
        await member.add_roles(role)


@bot.command()
@commands.has_permissions(administrator=True)
async def verifysetup(ctx):

    embed = discord.Embed(
        title="🔒 Server Verification",
        description=(
            "Klikni dugme ispod da se verifikuješ "
            "i dobiješ pristup serveru."
        ),
        color=0x00ff00
    )

    await ctx.send(
        embed=embed,
        view=VerifyButton()
    )


bot.run(TOKEN)