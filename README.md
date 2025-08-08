Update! `differentiation.py` is now its own project. This one is paused until I'm ready to put `differentiation.py` into it.
***
# Roadmap
1. Finish `differentiation.py`
   1. `class MathLaw`
      1. `class IndexLaw(MathLaw)`
      2. `class MultiInstance(MathLaw)`
   2. Every class gets their own `.simplify()` command, just to make it easier on me.
   3. Catch all edge cases.
   4. N-ary for `Multiplication`/`Addition`/`Subtraction`.
   5. `Power` rework, change from just doing $b^a = b*b*b...$ to doing $b^a = e^{aln(b)}$
   6. Add in comments for everything. I suck at comments. This will help document it.
   7. Don't start work on the query->Math objects yet.
2. Rework ALL my old plugins. And switch from PyCharm to VS Code (for when I make this closed source).
   1. `quotes.py` is in desperate need of a rework.
   2. `resume.py` needs to be fixed to stop crashing & to export it as a .pdf instead of .md (with correct formatting)
   3. `calculator.py` needs to be merged into `differentiation.py`.
   4. `pluginBase.py` is probably due for a rework too, but I might hold off until I've finished the next step.
3. Make my own tokeniser
   1. I don't like relying on imported modules.
   2. If I want to be able to call this a Chatbot, I need to be able to parse tokens and understand what it means.
   3. This will probably use my `differentiation.py` plugin for this (I'll probably call it `math.py` when I get to this step).
   4. It'll make sure I have a proper math module that I understand completely for calculating what the best response is.
4. Incorporate this into `differentiation.py` and `pluginBase.py` for:
   1. `differentiation.py`: So it can parse user text into Math objects (i.e., $3x^2$ into `Power(Variable(coefficient=Constant(3), value="x"), Constant(2))`)
   2. `pluginBase.py`: So it's easier to use context AND user input to make decisions on what gets done.
5. At this point, I'll probably close source the project and consider switching from Python. What can I say? I like money. I'll leave whatever the latest open source version there is out (just without my BIG plugins like `differentiation.py`).
***
# Documentation
I'll add in a lot of it when I get around to it. Not sure right now, all of it exists currently in `pluginBase.py`.