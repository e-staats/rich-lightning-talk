Why use rich?

Let's say you have a dictionary of information about ducks and you want to print it out. Here's what it would like with the standard python print:


And here's what it would look like with rich.print():

Can rich print json nicely? It sure can.

What if this was a dataclass? Yep.

For some of you, I think I could end this talk here. Super easy, pretty printing of Python objects alone was enough to get me using Rich day to day.

You can also get nicer tracebacks. For instance, here's the default log.exception() for an exception:

And here's what that looks like with Rich:

Pretty nice, right?

If you're looking to spruce up your own command line apps, you can get fancier with the formatting. You can use BBCode style tags to style text:

And you can go really wild; some of you who are familiar with old school Runescape might find this familiar:

Modern terminals have very wide color ranges, so you can pick your color with RGB or hex codes and print in whatever colors you want:

And of course, the medium of the future is emoji.

So now, getting into more specific uses of Rich, you can create panels. I mentioned at the start that everything here was rendered with Rich. So those nice comparison slides I had earlier? Let's see how those work:

You start by creating a Layout, then creating Layouts, Panels, or other renderables for each component. Then, you arrange them all with split_column() or split_row(), using "ratio" to control their relative sizes. There are other options as well, but this works pretty well for a quick and dirty slide:

So let's put it all together. We'll create a status message to display at the end of some job. We want 
* Green for good, red for bad
* Bold the important stuff
* Use some panels
* And emojis, why not

(walk through the code)

And so let's run our job. Terminals also refresh at 60+ FPS, so you can do nice animations in the terminal with Rich too.

And here we go! We've got our success message, and I created a failure message as well.

That's a quick overview of Rich; it's super flexible, very deep, and a lot of fun to play around with!





