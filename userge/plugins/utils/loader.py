from userge import userge, Message
from userge.utils import get_import_path
from userge.plugins import ROOT
import os


@userge.on_cmd('load', about="""\
__Load Userge plugin__

**Usage:**

    `.load [reply to userge plugin]`""")
async def load_cmd_handler(message: Message):
    await message.edit("Loading...")
    replied = message.reply_to_message
    if replied and replied.document:
        file_ = replied.document

        if file_.file_name.endswith('.py') and file_.file_size < 1024 ** 1024:
            path = await replied.download(file_name="userge/plugins/temp/")
            plugin = get_import_path(ROOT, path)

            try:
                userge.load_plugin(plugin)

            except Exception as e:
                os.remove(path)
                await message.err(e)

            else:
                await message.edit(f"`Loaded {plugin}`", del_in=3)

        else:
            await message.edit("`Plugin Not Found`")

    else:
        await message.edit("`Reply to Plugin`")


@userge.on_cmd('reload', about="__Reload all plugins__")
async def reload_cmd_handler(message: Message):
    await message.edit("`Reloading All Plugins`")
    await message.edit(f"`Reloaded {await userge.reload_plugins()} Plugins`", del_in=3)