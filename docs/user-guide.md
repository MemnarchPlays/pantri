# Pantri User Guide

Pantri is a home pantry tracker. It helps you keep track of what food you have, store your recipes, and build shopping lists — all from a web browser.

---

## Table of Contents

1. [Getting Around](#getting-around)
2. [Managing Your Pantry](#managing-your-pantry)
3. [Recipes](#recipes)
4. [Shopping List](#shopping-list)
5. [Low Stock Alerts](#low-stock-alerts)
6. [Backups](#backups)
7. [Discord Bot](#discord-bot)
8. [Common Questions](#common-questions)

---

## Getting Around

Pantri has four main pages, accessible from the navigation bar at the top:

| Page | What it's for |
|------|--------------|
| **Inventory** | See and manage everything currently in your pantry |
| **Recipes** | Browse, add, and use recipes |
| **Shopping** | Your shopping list and restock needs |
| **Settings** | Storage locations, backups, appearance, Discord |

---

## Managing Your Pantry

### Adding an item

1. Go to **Inventory**.
2. Fill in the **Item Name**, **Quantity**, **Unit** (cups, lbs, cans, etc.), and **Location** (Pantry, Fridge, Freezer, etc.).
3. Click **Add Item**.

If you add an item that already exists with the same name and unit in the same location, Pantri automatically combines the quantities instead of creating a duplicate.

### Adding multiple items at once

In the **Inventory** page, look for the **Bulk Add** box. Paste items one per line in this format:

```
Item, Quantity, Unit, Location
```

Example:
```
Chicken breast, 2, lbs, Freezer
Black beans, 3, cans, Pantry
Milk, 1, gallon, Fridge
```

### Editing or removing an item

Find the item in your inventory list and click the **edit (pencil)** icon to change it, or the **delete (trash)** icon to remove it.

### Storage locations

Pantri comes with default locations: **Pantry, Fridge, Freezer, Cabinet**. You can add your own (like "Garage Shelf" or "Wine Rack") in **Settings → Locations**.

---

## Recipes

### Browsing recipes

Go to **Recipes** to see your recipe library. You can filter by meal type (Breakfast, Lunch, Dinner, Snack, Dessert, etc.) using the buttons at the top.

Pantri comes loaded with ~89 starter recipes to get you going.

### Adding a recipe from a website

1. Go to **Recipes → Add Recipe**.
2. Paste any recipe website URL into the **Import from URL** box.
3. Click **Import** — Pantri reads the page and fills in the recipe for you.
4. Review and save.

### Adding a recipe manually

1. Go to **Recipes → Add Recipe**.
2. Fill in the name, meal type, ingredients, and instructions.
3. Click **Save**.

### Can I Make This?

This is one of the most useful features. On the **Recipes** page, look for the **Can I Make This?** button.

It shows you every recipe you can make *right now* based on what's in your pantry, sorted from most to least complete. Recipes you have 100% of the ingredients for appear first.

### Using a recipe

When you cook a meal, open the recipe and click **Use Recipe**. Pantri automatically subtracts the ingredients from your pantry inventory so your stock stays accurate.

### Scaling a recipe

On any recipe page, you can change the serving size and Pantri will scale all ingredient quantities up or down automatically.

### Exporting recipes to PDF

Go to **Recipes** and click **Export to PDF**. Pantri generates a formatted recipe binder you can download and print.

---

## Shopping List

The **Shopping** page has two sections:

### Restock Needs

Items that have fallen below their minimum quantity (if you've set one — see [Low Stock Alerts](#low-stock-alerts)). These appear automatically so you always know what needs replacing.

### Missing Ingredients

Pick any recipe from the dropdown and Pantri will compare the ingredients against your pantry and list exactly what you're missing.

### Adding items to your list

You can manually add anything to the shopping list, or items will appear automatically from Restock Needs or Missing Ingredients.

### Checking off items

Tap an item to check it off as you shop. The list remembers your checked items even if you close the browser and come back.

### Exclusions

Some things you always have on hand — salt, oil, butter — and you probably don't want them showing up in shopping lists. In **Settings → Exclusions**, add those items and they'll be ignored in all shopping list calculations.

---

## Low Stock Alerts

You can set a minimum quantity for any item. When your stock drops below that number, the item shows up in **Shopping → Restock Needs**.

### Setting a minimum for an item

1. Go to **Inventory** and find the item.
2. Click the **edit (pencil)** icon.
3. Enter a value in the **Minimum Quantity** field.
4. Save.

You can also set a global fallback minimum in **Settings** — any item without its own minimum will use that number instead.

---

## Backups

Pantri automatically backs up your data on a schedule (default: every 10 pantry changes). You can also trigger a manual backup at any time.

### Downloading a backup

Go to **Settings → Backups** and click **Download**. Save the `.zip` file somewhere safe.

### Restoring from a backup

Go to **Settings → Backups** and click **Restore**. Upload your `.zip` file. Pantri will replace the current data with the backup.

Pantri keeps your last 10 backups by default. You can adjust this number in Settings.

---

## Discord Bot

The Discord bot is optional. It lets you check and update your pantry without opening a browser — useful when you're at the grocery store and want to check what you have.

### Setting it up

1. Go to [discord.com/developers/applications](https://discord.com/developers/applications), create an application, go to **Bot**, and copy the token.
2. In Pantri, go to **Settings → Discord**, paste the token, and click **Save & Start Bot**.

### What you can do with the bot

| Command | What it does |
|---------|-------------|
| `!stock chicken` | Check how much chicken you have |
| `!list` | See everything in your pantry |
| `!list Fridge` | See only what's in the Fridge |
| `!add milk 1 gallon` | Add 1 gallon of milk |
| `!remove eggs 6` | Subtract 6 eggs from your inventory |
| `!set butter 2` | Set butter to exactly 2 (whatever unit it's stored in) |
| `!restock` | Show items below their minimum |
| `!canmake` | See what recipes you can make right now |
| `!canmake dinner` | Filter Can I Make This? to dinner recipes |
| `!recipe lasagna` | Show the lasagna recipe with pantry availability |
| `!help` | Show all available commands |

### Low stock alerts in Discord

In **Settings → Discord**, enter your Discord channel ID in the **Alert Channel** field. Pantri will post a message in that channel whenever an item drops below its minimum.

---

## Common Questions

**My inventory went down by itself — what happened?**
Someone clicked **Use Recipe** on a recipe page. That button deducts the recipe's ingredients from your pantry. Check with anyone else who has access to the app.

**I added an item but it's not showing up separately — where did it go?**
If an item with the same name, unit, and location already exists, Pantri merges them and adds the quantities together instead of creating a duplicate.

**A recipe website URL didn't import correctly — what do I do?**
Not all recipe websites are supported. If import doesn't work, use **Add Recipe** manually — paste in the ingredients and instructions yourself.

**The shopping list isn't saving my checked items after I refresh.**
The list saves in your browser. If you're using a different browser or a private/incognito window, it won't carry over. The server-side list state is shared across all devices.

**How do I add a storage location like "Garage" or "Basement Shelf"?**
Go to **Settings → Locations**, type the new name, and click **Add**. It will appear in the location dropdown on the Inventory page immediately.

**Can multiple people use Pantri at the same time?**
Yes. Pantri is a web app — anyone with the URL can use it at the same time. All changes are shared instantly.

**How do I change how the app looks?**
Go to **Settings → Appearance** to change the accent color and font.

**How do I change the port Pantri runs on?**
Go to **Settings → Server** and change the port number. The app will need to restart for the change to take effect.

**Where is my data stored? Is it sent anywhere?**
All your data stays on the server running Pantri — nothing is sent to any external service. The only exception is the Discord bot, which communicates with Discord's API if you set it up.

**How do I update Pantri to a newer version?**
If you're running with Docker, contact the person who set up the server — they can pull the latest image and restart the container. Your data will be preserved automatically.
