from .trivialoader import TriviaLoader

def setup(bot):
    bot.add_cog(TriviaLoader(bot))