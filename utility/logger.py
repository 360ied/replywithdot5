"""Logger"""
import discord

no_severity = 1  # Unimportant
low_severity = 2  # Warnings
medium_severity = 3  # Administrative Action
high_severity = 4  # Strong Administrative Action
emergency_severity = 5  # Requires Urgent Administrative Attention

# hex codes
severity_colours = {
    no_severity: "8B8386",
    low_severity: "FFFF00",
    medium_severity: "FF8000",
    high_severity: "CD0000",
    emergency_severity: "DC143C"
}

severity_titles = {
    no_severity: "no severity",
    low_severity: "Low Severity",
    medium_severity: "MEDIUM SEVERITY",
    high_severity: "**HIGH SEVERITY**",
    emergency_severity: "***@everyone EMERGENCY SEVERITY***"
}


async def log(channel: discord.TextChannel, severity: int, content: str) -> discord.Message:
    return await channel.send(
        f"{severity_titles[severity]}\n"
        f"{content}"
    )
