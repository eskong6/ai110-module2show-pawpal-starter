# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

There needs to be an Owner class, Pet class, Task Class, and Schedule class. The user should be able to add a pet and add tasks to their schedule. The user should also be able to see today's tasks. 
**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

One change I made was ensuring Owner had a pets field and Pet had an owner_id to ensure the two were connected.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

The scheduler considers: owner availability windows, task priority (high to low), task duration, earliest/latest time bounds, and pet species preferences. It also skips completed tasks and respects daily scheduling windows.

- How did you decide which constraints mattered most?

I prioritized hard constraints first (owner availability, task completion status) because they're non-negotiable. Then I used priority and duration to sort remaining tasks, since higher priority tasks should go first and longer tasks need earlier slots. Pet preferences act as sensible defaults but can be overridden. This keeps the logic simple and practical for a small pet-care planner.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff is that the scheduler only checks for exact start-time conflicts instead of full overlap windows. This keeps the logic lightweight and easier to understand for a small pet-care planner, while still catching obvious scheduling collisions that would otherwise create confusing plans.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
