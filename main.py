import discord
import os
import pandas
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model
from discord import Embed, Color, Member, utils, File
from random import randint
from os import environ
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("TOKEN")
df = pandas.read_csv("Book1.csv")
X = df[['Runs','Score']]
y = df['Earning per season']
poly = PolynomialFeatures(degree = 2)
X_poly = poly.fit_transform(X)
reg = linear_model.LinearRegression()
reg.fit(X_poly,y)
y_pred=reg.predict(X_poly)
def embed(text, color=None):
    color = Color(color) if color else Color(randint(0, 0xFFFFFF))
    return Embed(description=text, color=color)
client = discord.Client()
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
@client.event
async def on_message(message):
    if message.content.startswith('!help'):
        await message.channel.send(embed=embed('To get the predicted price of the batsman type: !runs average strike rate (e.g. !3000 29.3 141)'))
    elif message.content.startswith('!'):
        a, b, c = map(str, message.content.split())
        a = a[1:]
        a = int(a)
        b = float(b)
        c = int(c)
        price = reg.predict(poly.fit_transform([[a, b*c]]))[0]
        price/=10**7
        if price<=0:
            await message.channel.send(embed=embed('The Batsman will remain unsold'))
        else:
            await message.channel.send(embed=embed('Predicted price of the batsman is-> '+str(round(price,1))+' crores'))
client.run('ODIxNzE3Nzc1NTE2Njk2NTc2.YFHyUA.1beI8GS6719mjPYMgY6dcota6DY')