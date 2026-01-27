def get_system_prompt(fewshots: int) -> str:
    webshop_instruction_react = """
Solve a shopping task with interleaving Observation, Thought, and Action steps. Here are some guidelines:
- You will be given a user request and some observations from a web shop environment.
- You need to response with Thought and Action, then you wiil be given corresponding observation
- Thought needs to reason about the user request based on the Observations in 1-2 sentences.
- If the Observations are unclear, you must navigate the environment until relevant data is found using provided actions. You MUST NEVER say in your thought that you don't know the answer.

### Tools Available:
- **search['search text']**: Searches for 'search text' in the webshop environment.
You can only use this tool when the observation explicitly shows a [search] button.
- **click['button']**: Clicks a button to inspect product details, navigate pages, or interact with options.
You are only allowed to click buttons displayed inside the [brackets].

### Rules to Follow:
1. **Error Handling**: If the observation shows an Error message, refer to the last valid observation to determine the next action. If you cannot decide the next action based on the valid observation, try clicking [Back to Search] to return to the search page or [< Prev] to go to the previous page.
2. **Step-by-Step and replan**: Carefully analyze each observation and ensure your actions align with the given information. You can replan after receiving the action results, so just plan for current state.
3. **Numbered Plans Only**: Present your plan as a numbered list, detailing each action step by step. Do not include explanations or extra text outside the numbered list.
4. **Navigating Pages**:
  - After clicking Description, Features, Reviews, or Attributes, make sure to click '< Prev' to get back to the item page. 
  - If you want to navigate another item after clicking specific item, you need to click '< Prev' first and then click the next item ID.
  - For example,
    Thought: ...
    Action: search[search query]
    Observation: 
    [Back to Search] 
    Page 1 (Total results: 50) 
    [Next >] 
    [B011S76LB0] 
    Item description for B011S76LB0
    [B0096E5948]
    Item description for B0096E5948
    
    (Based on the search result,)
    Thought: ...
    Action: click[B011S76LB0]
    Observation: 
    [Back to Search] 
    [< Prev] 
    Item description for B011S76LB0
    Price: $21.99 
    Rating: N.A. 
    [Description] 
    [Features] 
    [Reviews] 
    [Attributes] 
    [Buy Now] 
    
    (If you want to see other product's details, you need to click '< Prev' to go back to search result page!)
    Thought: ...
    Action: click[< Prev]
    Observation: 
    [Back to Search] 
    Page 1 (Total results: 50) 
    [Next >] 
    [B011S76LB0] 
    Item description for B011S76LB0
    [B0096E5948]
    Item description for B0096E5948
    
    Thought: ...
    Action: click[B0096E5948]
    Observation: 
    [Back to Search] 
    [< Prev] 
    Item description for B0096E5948
    Price: $21.99 
    Rating: N.A. 
    [Description] 
    [Features] 
    [Reviews] 
    [Attributes] 
    [Buy Now] 
    
    (Assuming B011S76LB0 is better item you think,)
    Thought: ...
    Action: click[< Prev]
    Observation: 
    [Back to Search] 
    Page 1 (Total results: 50) 
    [Next >] 
    [B011S76LB0] 
    Item description for B011S76LB0
    [B0096E5948]
    Item description for B0096E5948
    
    Thought: ...
    Action: click[B011S76LB0]
    Observation: 
    [Back to Search] 
    [< Prev] 
    Item description for B011S76LB0
    Price: $21.99 
    Rating: N.A. 
    [Description] 
    [Features] 
    [Reviews]
    [Attributes] 
    [Buy Now] 
    
    (Inspect details of the product. Also, make sure to click '< Prev',)
    Thought: ...
    Action: click[Description]
    Observation: 
    [< Prev] 
    Item description for B011S76LB0
    
    Thought: ...
    Action: click[< Prev]
    Observation: 
    [Back to Search] 
    [< Prev] 
    Item description for B011S76LB0
    Price: $21.99 
    Rating: N.A. 
    [Description] 
    [Features] 
    [Reviews] 
    [Attributes] 
    [Buy Now]

    Thought: ...
    Action: click[Features]
    Observation: 
    [< Prev] 
    Item Features for B011S76LB0
    
    Thought: ...
    Action: click[< Prev]
    Observation: 
    [Back to Search] 
    [< Prev] 
    Item description for B011S76LB0
    Price: $21.99 
    Rating: N.A. 
    [Description] 
    [Features] 
    [Reviews] 
    [Attributes] 
    [Buy Now]
    
    (After checking the details of items, click options and 'Buy Now')
    Thought: ...
    Action: click[option1]
    Observation:
    Thought: ...
    Action: click[option2]
    Observation:
    Thought: ...
    Action: click[Buy Now]
    Observation:
    Success!

5. **End condition**: The phrase "Your score (min 0.0, max 1.0) [the score]" will only appear after clicking "Buy Now". You must click "Buy Now" to end the task at appropriate item page.
"""
    examples = ["""
Here are some example trajectories:
                
Instruction:
i am looking for dairy free and apple variety pack of chips, and price lower than 30.00 dollars
[Search]

Thought: search for diary free and apple variety pack of chips under $30
Action: search[dairy free and apple variety pack of chips under $30]
Observation:
[Back to Search]
Page 1 (Total results: 50)
[Next >]
[B07HRFJWP8]
Enjoy Life Foods Soft Baked Ovals, Breakfast Bars, Nut Free Bars, Soy Free, Dairy Free, Non GMO, Gluten Free, Vegan, Variety Pack, 4 Boxes (20 Bars Total)
$100.0
[B01KMHY5PG]
Enjoy Life Soft Baked Chewy Bars, Variety Pack, Nut Free Bars, Soy Free, Dairy Free, Gluten Free, 6 Boxes (30 Total Bars)
$21.49
[B008D2X8C4]
Enjoy Life Lentil Chips Variety Pack, Dairy Free Chips, Soy Free, Nut Free, Non GMO, Vegan, Gluten Free, 24 Bags (0.8 oz)
$100.0

Thought: The second item matches the criteria as it is dairy-free, a variety pack, and priced below $30.
Action: click[B01KMHY5PG]
Observation:
[Back to Search]
[< Prev]
flavor name [Apple][Strawberry]
size [Pack of 6][Pack of 12]
Price: $21.49
Rating: 4.5 stars
[Description]
[Features]
[Reviews]
[Buy Now]

Thought: The product has the option 'Apple' which matches my preference. I will select it.
Action: click[Apple]
Observation: You have clicked Apple.


Thought: Now, I will click “Buy Now” to complete the purchase.
Action: click[Buy Now]
Observation: Your score (min 0.0, max 1.0): 0.5
Purchase successful with score 0.5
###
""",
"""
Instruction:
i need gluten free vegetarian smoked peppered bacon - 4 ounce (pack of 2), and price lower than 40.00 dollars
[Search]

Thought: Search for gluten-free vegetarian smoked peppered bacon 4-ounce pack of 2 under $40.
Action: search[gluten free vegetarian smoked peppered bacon 4 ounce pack of 2 under $40]
Observation:
[Back to Search]
Page 1 (Total results: 50)
[Next >]
[B06Y96MXJV]
Smoked Bacon Sea Salt 3-Pack: Smoked Bacon Chipotle, Smoked Bacon and Onion, Smoked Peppered Bacon - All-Natural Sea Salts Slowly Smoked Over Alderwood - No Gluten, No MSG, Non-GMO (12 total oz.)
$29.99
[B06Y96N1KG]
Spicy Hot Pepper Sea Salt 3-Pack: Ghost Pepper, Jalapeno, Habanero - All Natural, Delicious Blends of Peppers & Sea Salt - Gluten-Free, Kosher, No MSG, Non-GMO (12 total oz.)
$29.99
[B07GJTKYJQ]
Louisville Vegan Jerky - 5 Flavor Variety Pack, Non-GMO Soy Protein, Gluten-Free (Black Pepper, Buffalo Dill, Pepperoni, Maple Bacon, and Carolina BBQ, 3 Ounces)
$42.99

Thought: The first item partially matches the query but needs confirmation of the pack size.
Action: click[B06Y96MXJV]
Observation:
[Back to Search]
[< Prev]
Smoked Bacon Sea Salt 3-Pack: Smoked Bacon Chipotle, Smoked Bacon and Onion, Smoked Peppered Bacon - All-Natural Sea Salts Slowly Smoked Over Alderwood - No Gluten, No MSG, Non-GMO (12 total oz.)
Options:
size [4 oz (Pack of 2)][12 oz (Pack of 1)]
Price: $29.99
Rating: 4.8 stars
[Description]
[Features]
[Reviews]
[Buy Now]

Thought: The product has the size '4 oz (Pack of 2)' and meets the gluten-free and price constraints.
Action: click[4 oz (Pack of 2)]
Observation: You have clicked 4 oz (Pack of 2).

Thought: Now, I will click “Buy Now” to complete the purchase.
Action: click[Buy Now]
Observation: Your score (min 0.0, max 1.0): 1.0
Purchase successful with score 1.0
###

Instruction:
i need vegan snack pack with a variety of flavors, and price lower than 15.00 dollars
[Search]

Thought: Search for a vegan snack pack with a variety of flavors under $15.
Action: search[vegan snack pack flavor variety under $15]
Observation:
[Back to Search]
Page 1 (Total results: 50)
[Next >]
[B09XYZ123]
Vegan Snack Pack Variety - $14.99
[B08ABCDE12]
Vegan Chips, Single Flavor - $10.00

Thought: The first item matches the criteria as it is vegan, includes a flavor variety, and is priced at $14.99.
Action: click[B09XYZ123]
Observation:
[Back to Search]
[< Prev]
Options:
flavor name [Flavor A][Flavor B]
size [Variety Pack]
Price: $14.99
Rating: 4.6 stars
[Description]
[Features]
[Reviews]
[Buy Now]

Thought: The product has the 'Variety Pack' option and meets the price constraint.
Action: click[Variety Pack]
Observation: You have clicked Variety Pack.

Thought: Now, I will click “Buy Now” to complete the purchase.
Action: click[Buy Now]
Observation: Your score (min 0.0, max 1.0): 0.9
Purchase successful with score 0.9
###
"""]
    return webshop_instruction_react + "\n".join(examples[:fewshots]) + "Now you need to answer\nThought:\nAction:"