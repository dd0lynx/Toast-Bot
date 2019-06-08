import requests
import asyncio
import discord
from discord.ext import commands

api_url = 'https://api.scryfall.com'

class MTG(commands.Cog):

    """Magic the gathering commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='mtg')
    async def mtg(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send('subcommands: [search], [card]')

    @mtg.command(name='search')
    async def search(self, ctx, *, query:str=None):
        if query is None:
            await ctx.send('Enter something to search on Scryfall.\n' +
                           'Returns the name of the top 20 card results.')
        else:
            response = requests.get(f'{api_url}/cards/search',
                                    params={'q': query})
            if response:
                card_list = response.json()['data'][:20]
                results = '\n'.join(card['name'] for card in card_list)
                await ctx.send(f'Top results for "{query}"\n{results}')
            else:
                await ctx.send(f'No results for "{query}"')

    def card_scryfall(self, card_name):
        found = True
        # performs an exact search first
        response = requests.get(f'{api_url}/cards/named',
                                params={'exact': card_name})
        if not response:
            asyncio.sleep(0.2)
            # performs a fuzzy search if the exact search failed
            response = requests.get(f'{api_url}/cards/named',
                                    params={'fuzzy': card_name})
        if not response:
            asyncio.sleep(0.2)
            # performs a general seach for cards matching
            # the name in the case of multiple
            # cards matching search name
            found = False
            response = requests.get(f'{api_url}/cards/search',
                                    params={'q': card_name})
        if found:
            asyncio.sleep(0.1)
        return found, response

    def embed_card(self, card, rulings_response):
        embed = discord.Embed(title=card['name'])
        embed.add_field(name='Set',
                        value= f'{card["set_name"]}({card["set"]})')
        if rulings_response:
            rulings = rulings_response.json()['data']
            if rulings:
                embed.add_field(name='Rulings',
                                value='\n\n'.join(rule['comment'] for rule in rulings))
        prices = card['prices']
        embed.set_footer(text=f'Regular: ${prices["usd"]} Foil: ${prices["usd_foil"]}')
        embed.set_image(url=card['image_uris']['normal'])
        return embed

    @mtg.command(name='card')
    async def card(self, ctx, *, card_name:str=None):
        if card_name is None:
            await ctx.send('Enter the name of a card to find on Scryfall.\n' +
                           'If the card is found, I will return details on' +
                           'the card or else I\'ll perform a general search' +
                           'return a list of card names')
        else:
            card_found, card_response = self.card_scryfall(card_name)
            if card_found:

                card = card_response.json()
                print(f'embeding card {card["name"]}')
                rulings_response = requests.get(card['rulings_uri'])
                embed = self.embed_card(card, rulings_response)
                await ctx.send(embed=embed)
            else:
                ctx.send('card not found, remind creator to fucing finish this')

    @mtg.group(name='deck')
    async def deck(self, ctx):
        ctx.send('not implemented yet')

def setup(bot):
    bot.add_cog(MTG(bot))
