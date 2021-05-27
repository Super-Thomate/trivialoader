from redbot.core import commands
from redbot.core import Config, checks
from redbot.core.utils.chat_formatting import box
import discord
import os
import sys
import json
class TriviaLoader(commands.Cog):
  """Load a trivia file"""

  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases=['zei', 'triviaup', 'triviaul'])
  @commands.guild_only()
  @checks.mod_or_permissions()
  async def triviaupload(self, ctx: commands.Context):
    """
    Upload a file for the redbot trivia easily
    """
    info                     = self.readJSON("info.json")
    if not len(info["list_path"]):
      p = await self.bot.get_prefix(ctx.message)
      await ctx.send ("Path to trivia undefined. Use `{}triviapath set <path>`".format(p[0]))
      return
    await ctx.send ("Load a file (yaml)")
    def check (m):
      return m.channel == ctx.channel and len (m.attachments)
    message                  = await self.bot.wait_for ('message', check=check)
    file                     = message.attachments [0]
    file_name                = file.filename
    extension                = os.path.splitext(file_name)[1]
    if (extension != ".yaml"):
      await ctx.send ("File {0} is not a yaml file. ({1})".format (file_name, extension))
      return
    try:
      await file.save (info["list_path"]+file_name)
      await ctx.send("File "+file_name+" added to the trivia")
    except Exception as e:
      await ctx.send (f"{type(e).__name__} - {e}")

  @commands.command(aliases=['unzei', 'triviadel', 'triviad'])
  @commands.guild_only()
  @checks.mod_or_permissions()
  async def triviadelete(self, ctx: commands.Context, trivia: str):
    """
    Delete a trivia
    """
    info                     = self.readJSON("info.json")
    if not len(info["list_path"]):
      p = await self.bot.get_prefix(ctx.message)
      await ctx.send ("Path to trivia undefined. Use `{}triviapath set <path>`".format(p[0]))
      return
    try:
      file                   = os.path.splitext(trivia)[0]
      os.remove(info["list_path"]+file+".yaml")
    except Exception as e:
      if type(e).__name__ == "FileNotFoundError":
        await ctx.send ("Trivia `{}` does not exist.".format(trivia))
      else:
        await ctx.send (f"{type(e).__name__} - {e}")
      return
    await ctx.send ("Trivia `{}` removed.".format(trivia))

  @commands.command(aliases=['downzei''triviadown', 'triviadl'])
  @commands.guild_only()
  @checks.mod_or_permissions()
  async def triviadownload(self, ctx: commands.Context, trivia: str):
    """
    Download a trivia file
    """
    info                     = self.readJSON("info.json")
    if not len(info["list_path"]):
      p = await self.bot.get_prefix(ctx.message)
      await ctx.send ("Path to trivia undefined. Use `{}triviapath set <path>`".format(p[0]))
      return
    try:
      file                   = os.path.splitext(trivia)[0]
      file_to_upload         = discord.File (info["list_path"]+file+".yaml", filename=file+".yaml")
    except Exception as e:
      if type(e).__name__ == "FileNotFoundError":
        await ctx.send ("Trivia `{}` does not exist.".format(trivia))
      else:
        await ctx.send (f"{type(e).__name__} - {e}")
      return
    await ctx.send (file=file_to_upload)

  @commands.group()
  @commands.guild_only()
  @checks.mod_or_permissions()
  async def triviapath(self, ctx: commands.Context):
    """
    Manage the path to the trivia files
    """
    if ctx.invoked_subcommand is None:
      info                   = self.readJSON("info.json")
      msg                    = box (  (   "Current settings\n"
                                          "Path: '{0}'\n"
                                      ).format(info['list_path'])
                                     , lang="py"
                                   )
      await ctx.send(msg)

  @triviapath.command(name="set")
  async def triviapath_set(self, ctx: commands.Context, path: str):
    """
    Set the path to trivia files (where trivia files are found)
    """
    try:
      data                   = {}
      data     ["list_path"] = path if path.endswith('/') else path+'/'
      self.writeJSON ('info.json', data)
    except Exception as e:
      await ctx.send (f"{type(e).__name__} - {e}")
      return
    await ctx.send ("Path to trivia updated.")

  def readJSON(self, filename):
    dir_path = os.path.dirname(os.path.realpath(__file__)) + '/'
    with open (dir_path+filename) as json_file:
      data                   = json.load(json_file)
    return data

  def writeJSON(self, filename, data):
    dir_path = os.path.dirname(os.path.realpath(__file__)) + '/'
    with open (dir_path+filename, 'w') as json_file:
      json.dump(data, json_file)

  @commands.group()
  @commands.guild_only()
  @checks.mod_or_permissions()
  async def triviaclean(self, ctx: commands.Context):
    """
    Clean all trivia that are not Avatar
    """
    info                     = self.readJSON("info.json")
    if not len(info["list_path"]):
      p = await self.bot.get_prefix(ctx.message)
      await ctx.send ("Path to trivia undefined. Use `{}triviapath set <path>`".format(p[0]))
      return
    trivias = os.listdir (info["list_path"])
    for trivia in trivias:
      try:
        file                   = os.path.splitext(trivia)[0]
        if not (file == "atla" or file == "tlok"):
          os.remove(info["list_path"]+file+".yaml")
      except Exception as e:
        if type(e).__name__ == "FileNotFoundError":
          await ctx.send ("Trivia `{}` does not exist.".format(trivia))
        else:
          await ctx.send (f"{type(e).__name__} - {e}")
        return
      break
    await ctx.send ("Trivia `{}` removed.".format(trivia))

