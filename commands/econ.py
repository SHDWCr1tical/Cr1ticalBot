import discord
from discord.ext import commands
import json
import os


class EconCog(commands.Cog, name='Economy'):
    
    def __init__(self, client):
        self.client = client
    
    @commands.command(aliases=['bal'])
    async def balance(ctx):
        await open_account(self.ctx.author)
        user = self.ctx.author
        users = await get_bank_data()
        
        wallet_amt = users[str(user.id)]["wallet"]
        bank_amt = users[str(user.id)]["bank"]
        
        em = discord.Embed(title = f"{self.ctx.author.name}'s balance", color = 0x000000)
        em.add_field(name = "Wallet",value= f'⏣ {wallet_amt}')
        em.add_field(name = "Bank",value = f'⏣ {bank_amt}')
        await self.ctx.send(embed = em)
        
        
    @commands.command()
    async def shop(ctx):
        em = discord.Embed(title = "Shop")
    
        for item in mainshop:
            name = item["name"]
            price = item["price"]
            desc = item["description"]
            em.add_field(name = name, value = f"${price} | {desc}")
    
        await self.ctx.send(embed = em)
    
    
    
    @commands.command()
    async def buy(ctx,item,amount = 1):
        await open_account(self.ctx.author)
    
        res = await buy_this(self.ctx.author,item,amount)
    
        if not res[0]:
            if res[1]==1:
                await self.ctx.send("That Object isn't there!")
                return
            if res[1]==2:
                await self.ctx.send(f"You don't have enough money in your wallet to buy {amount} {item}")
                return
    
    
        await self.ctx.send(f"You just bought {amount} {item}")
    
    
    @commands.command()
    async def bag(ctx):
        await open_account(self.ctx.author)
        user = self.ctx.author
        users = await get_bank_data()
    
        try:
            bag = users[str(user.id)]["bag"]
        except:
            bag = []
    
    
        em = discord.Embed(title = "Bag")
        for item in bag:
            name = item["item"]
            amount = item["amount"]
    
            em.add_field(name = name, value = amount)
    
        await self.ctx.send(embed = em)
        
        
    @commands.command()
    async def sell(ctx,item,amount = 1):
        await open_account(self.ctx.author)
    
        res = await sell_this(self.ctx.author,item,amount)
    
        if not res[0]:
            if res[1]==1:
                await self.ctx.send("That Object isn't there!")
                return
            if res[1]==2:
                await self.ctx.send(f"You don't have {amount} {item} in your bag.")
                return
            if res[1]==3:
                await self.ctx.send(f"You don't have {item} in your bag.")
                return
    
        await self.ctx.send(f"You just sold {amount} {item}.")
    
    async def sell_this(user,item_name,amount,price = None):
        item_name = item_name.lower()
        name_ = None
        for item in mainshop:
            name = item["name"].lower()
            if name == item_name:
                name_ = name
                if price==None:
                    price = 0.9* item["price"]
                break
    
        if name_ == None:
            return [False,1]
    
        cost = price*amount
    
        users = await get_bank_data()
    
        bal = await update_bank(user)
    
    
        try:
            index = 0
            t = None
            for thing in users[str(user.id)]["bag"]:
                n = thing["item"]
                if n == item_name:
                    old_amt = thing["amount"]
                    new_amt = old_amt - amount
                    if new_amt < 0:
                        return [False,2]
                    users[str(user.id)]["bag"][index]["amount"] = new_amt
                    t = 1
                    break
                index+=1
            if t == None:
                return [False,3]
        except:
            return [False,3]
    
        with open("mainbank.json","w") as f:
            json.dump(users,f)
    
        await update_bank(user,cost,"wallet")
    
        return [True,"Worked"]
        
        
    @commands.command(aliases = ["lb"])
    async def leaderboard(ctx,x = 1):
        users = await get_bank_data()
        leader_board = {}
        total = []
        for user in users:
            name = int(user)
            total_amount = users[user]["wallet"] + users[user]["bank"]
            leader_board[total_amount] = name
            total.append(total_amount)
    
        total = sorted(total,reverse=True)
    
        em = discord.Embed(title = f"Top {x} Richest People" , description = "This is decided on the basis of raw money in the bank and wallet",color = discord.Color(0xfa43ee))
        index = 1
        for amt in total:
            id_ = leader_board[amt]
            member = commands.get_user(id_)
            name = member.name
            em.add_field(name = f"{index}. {name}" , value = f"{amt}",  inline = False)
            if index == x:
                break
            else:
                index += 1
    
        await self.ctx.send(embed = em)
        
    @commands.command()
    async def beg(ctx):
        await open_account(self.ctx.author)
        user = self.ctx.author
        users = await get_bank_data()
        
        
        earnings = random.randrange(101)
        
        
        
        await self.ctx.send(f'Someone gave you ⏣ {earnings}!')
        
        users[str(user.id)]["wallet"] += earnings
    
        with open("mainbank.json", "w") as f:
          json.dump(users,f)
        return True
        
    @commands.command(aliases=['with'])
    async def withdraw(ctx,amount= None):
        await open_account(self.ctx.author)
        if amount == None:
            await self.ctx.send("Please enter the amount.")
            return
        
        bal = await update_bank(self.ctx.author)
        
        amount = int(amount)
        if amount>bal[1]:
            await self.ctx.send("You don't have enough money.")
            return
        if amount<0:
            await self.ctx.send("Amount must be positive!")
            return
        
        await update_bank(self.ctx.author, amount)
        await update_bank(self.ctx.author,-1*amount, "bank")
        
        await self.ctx.send(f'You withdrew ⏣ {amount}!')
    
    @commands.command(aliases=['dep'])
    async def deposit(ctx,amount= None):
        await open_account(self.ctx.author)
        if amount == None:
            await self.ctx.send("Please enter the amount.")
            return
        
        bal = await update_bank(self.ctx.author)
        
        amount = int(amount)
        if amount>bal[0]:
            await self.ctx.send("You don't have enough money.")
            return
        if amount<0:
            await self.ctx.send("Amount must be positive!")
            return
        
        await update_bank(self.ctx.author,-1*amount)
        await update_bank(self.ctx.author,amount, "bank")
        
        await self.ctx.send(f'You deposited ⏣ {amount}!')
        
        
        
        
    @commands.command()
    async def send(ctx,member:discord.Member,amount= None):
        await open_account(self.ctx.author)
        await open_account(member)
        if amount == None:
            await self.ctx.send("Please enter the amount.")
            return
        
        bal = await update_bank(self.ctx.author)
        if amount == "all":
            amount = bal[0]
        
        amount = int(amount)
        if amount>bal[0]:
            await self.ctx.send("You don't have enough money.")
            return
        if amount<0:
            await self.ctx.send("Amount must be positive!")
            return
        
        await update_bank(self.ctx.author,-1*amount, "bank")
        await update_bank(member,amount, "bank")
        
        await self.ctx.send(f'You gave ⏣ {amount}!')
        
        
        
    @commands.command()
    async def slots(ctx,amount = None):
        await open_account(self.ctx.author)
        
        if amount == None:
            await self.ctx.send("Please enter the amount.")
            return
        
        bal = await update_bank(self.ctx.author)
        
        amount = int(amount)
        if amount>bal[0]:
            await self.ctx.send("You don't have enough money.")
            return
        if amount<0:
            await self.ctx.send("Amount must be positive!")
            return
        
        final = []
        for i in range(3):
            a = random.choice(["x","O","Q"])
            
            final.append(a)
            
        await self.ctx.send(str(final))
            
        if final[0] == final[1] or final[2] == final[2]:
          await update_bank(self.ctx.author,2*amount)
          await self.ctx.send('You won the bet!')
        else:
             await update_bank(self.ctx.author,-1*amount)
             await self.ctx.send('You lost the bet, sorry!')
        
        
    
    @commands.command()
    async def rob(ctx,member:discord.Member,):
        await open_account(self.ctx.author)
        await open_account(member)
        
        bal = await update_bank(member)
        
        if bal[0]<100:
            await self.ctx.send("It's not worth it!")
            return
        
        earnings = random.randrange(0, bal[0])
        
        await update_bank(self.ctx.author,earnings)
        await update_bank(member,-1*earnings)
        
        await self.ctx.send(f'You stole ⏣ {earnings} from {member}!')
    
    
    async def get_bank_data():
        with open("mainbank.json", "r") as f:
            users = json.load(f)
            
        return users
        
    async def update_bank(user,change = 0, mode = "wallet"):
        users = await get_bank_data()
        
        users[str(user.id)][mode] += change
        with open("mainbank.json", "w") as f:
            json.dump(users,f)
            
        bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]
        return bal
        
        
        
    async def buy_this(user,item_name,amount):
        item_name = item_name.lower()
        name_ = None
        for item in mainshop:
            name = item["name"].lower()
            if name == item_name:
                name_ = name
                price = item["price"]
                break
    
        if name_ == None:
            return [False,1]
    
        cost = price*amount
    
        users = await get_bank_data()
    
        bal = await update_bank(user)
    
        if bal[0]<cost:
            return [False,2]
    
    
        try:
            index = 0
            t = None
            for thing in users[str(user.id)]["bag"]:
                n = thing["item"]
                if n == item_name:
                    old_amt = thing["amount"]
                    new_amt = old_amt + amount
                    users[str(user.id)]["bag"][index]["amount"] = new_amt
                    t = 1
                    break
                index+=1
            if t == None:
                obj = {"item":item_name , "amount" : amount}
                users[str(user.id)]["bag"].append(obj)
        except:
            obj = {"item":item_name , "amount" : amount}
            users[str(user.id)]["bag"] = [obj]
    
        with open("mainbank.json","w") as f:
            json.dump(users,f)
    
        await update_bank(user,cost*-1,"wallet")
    
        return [True,"Worked"]
    
    async def open_account(user):
        users = await get_bank_data()
            
        if str(user.id) in users:
            return False
        else:
            users[str(user.id)] = {}
            users[str(user.id)]["wallet"] = 0
            users[str(user.id)]["bank"] = 0
            
        with open("mainbank.json", "w") as f:
            json.dump(users,f)
        return True



def setup(client):
    client.add_cog(EconCog(client))
    print('Economy is loaded.')
