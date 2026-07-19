---
name: sjs-ingredient-lookup
description: Answer any question about ingredients in Sweet July Skin formulas using the official ingredient master list. Use this skill whenever someone asks what's in a Sweet July Skin product, which products contain a specific ingredient, whether a product has a particular ingredient (e.g., retinol, fragrance, alcohol, common allergens), how to respond to a customer asking about an ingredient, or anything else that requires looking up the official INCI list for a Sweet July Skin SKU. Trigger this skill on phrases like "what's in the Pava Toner", "does the Castaway Cream have niacinamide", "which products contain retinol", "ingredient list for the Coffee Fix Eye Cream", "is there fragrance in the lip treatments", "I need to answer a customer question about [product]", or any mention of a Sweet July Skin product alongside an ingredient-related question. Always use this skill — never answer ingredient questions about Sweet July Skin products from memory or by guessing, even if the question seems simple.
---

# Sweet July Skin Ingredient Lookup

This skill gives Claude access to the official ingredient lists for every Sweet July Skin product, so anyone in the org can ask ingredient questions and get accurate answers from the source.

## Step 1: Read the master ingredient file

Before answering any ingredient question, read the full reference:

```
/mnt/skills/user/sjs-ingredient-lookup/references/ingredients.md
```

This file is the source of truth. It contains the complete INCI (cosmetic ingredient) list for all 13 Sweet July Skin products, transcribed from the brand's master document.

## Step 2: Answer from the file only

The reference file is the only authoritative source. Follow these rules:

- **Never make up ingredients.** If a product isn't in the file, say so plainly. Don't guess based on what similar products contain.
- **Match the user's question to the right product.** Sweet July Skin uses both formal names ("Pava Exfoliating Cleanser") and short names ("the Pava Cleanser", "the cleanser"). Map casual references to the correct product. If it's truly ambiguous (e.g., "the Pava" could be cleanser or toner), ask which one.
- **Quote the file faithfully.** If a customer-facing answer is being drafted, use the exact ingredient names as they appear in the file. Don't paraphrase INCI names.
- **Ingredient order matters.** Ingredients are listed in descending order of concentration (with anything under 1% in any order, and "may contain" colorants last). Mention this when it's relevant to the question — for example, if someone asks how prominent an ingredient is in the formula.
- **Flag "May Contain" colorants.** These are color additives that may or may not be present depending on the shade. Always note this when answering questions about pigmented products like the lip treatments or Coffee Fix Eye Cream.

## Step 3: Match common names to INCI names

Many people ask about ingredients using common names (e.g., "lavender", "shea butter"), but the file lists INCI (scientific) names. The reference file includes a translation table at the bottom — use it to match terms. For example:

- "Does the Castaway Cream have shea butter?" → look for "Butyrospermum Parkii" in Castaway Cream → yes, second ingredient.
- "Which products have aloe?" → search for "Aloe Barbadensis" across all products.

For functional ingredient questions ("anything for hyperpigmentation?", "what brightening agents are in here?"), use the functional terms list at the bottom of the reference file. For example, tranexamic acid, ferulic acid, vitamin C derivatives, niacinamide, and AHAs are all relevant to discoloration.

## Step 4: Format the answer for the audience

Adjust the answer style based on what the question seems to be for:

- **Internal team question** ("does the Pava Toner have alcohol?") → direct, concise answer. Yes/no plus the relevant line from the ingredient list.
- **Drafting a customer reply** ("a customer is asking about discoloration in the Pava Cleanser, what should I tell them?") → pull out the relevant ingredients, explain in plain language what they do, and offer a clean draft response. Always recommend the customer consult a dermatologist for medical concerns.
- **Comparing products** ("what's the difference between the Lychee Jelly and Guava Jelly?") → compare side by side. Note that the lip treatments share a base formula and differ mostly in flavor, fragrance, and color.
- **Ingredient lookup across the line** ("which products are vegan / fragrance-free / safe for X concern?") → scan all 13 products in the file and list every match. Be exhaustive.

## Step 5: When something isn't clear

The source document has a few rough edges (truncated words, occasional typos, formatting inconsistencies). The cleaned reference file flags these inline with notes. If a question hinges on a flagged item, mention the ambiguity to the user and recommend confirming with the brand team or checking the original source document.

If an ingredient question goes beyond what the file can answer (e.g., "what concentration of retinol is in the Good Youth Serum?" — concentrations aren't disclosed on INCI lists), say so and suggest where to find the answer (formulator, COA, supplier spec sheet).

## What this skill does not cover

- **Concentrations / percentages** — not on INCI lists.
- **Allergen testing or claims** — direct these to the regulatory/QA team.
- **Medical advice** — never give skin-condition advice. Recommend a dermatologist.
- **Products not in the file** — if a SKU isn't listed, the file doesn't have it. Don't fabricate.
- **Updates to formulas** — the file is dated. If a reformulation has happened recently, the source document needs to be updated first, then this skill rebuilt.
