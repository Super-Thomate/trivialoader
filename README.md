# trivialoader
Red Discord Bot cog to upload and download trivia without accessing the machine

Install the cog with the others cogs from Red.

Load *trivialoader* like any other Red cogs.

```
[p]load trivialoader
```

Then set the path for the directory containing the trivia files

```
[p]triviapath set <mypath>
```

You can now upload, download or delete trivia directly from Discord.

To upload a trivia (from Me to Red)
```
[p]triviaupload
```
Red will ask you to give one or more trivia files.

To download a trivia (from Red to Me)
```
[p]trividownload <trivia>
```
Red will give you the corresponding yaml file.

To delete a trivia (cannot be undone)
```
[p]trividelete <trivia>
```
Red will delete the corresponding yaml file.


