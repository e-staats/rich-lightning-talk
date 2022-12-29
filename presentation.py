import logging
import shutil
from contextlib import redirect_stdout
from dataclasses import dataclass
from io import StringIO
from textwrap import dedent

import rich
from rich.console import Console, RenderableType
from rich.layout import Layout
from rich.markdown import Markdown
from rich.padding import Padding
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text

SPIEL = "[Spiel](https://github.com/JoshKarpel/spiel)"
GITHUB = "[GitHub](https://github.com/e-staats/rich-lightning-talk)"
console = Console()


def pad_markdown(markup: str) -> RenderableType:
    return Padding(Markdown(dedent(markup), justify="center"), pad=(0, 5))


@dataclass
class Bird:
    name: str
    genus: str
    species: str
    flight: bool
    wingspan: int
    habitats: list[str]


def get_goose():
    return Bird(
        name="Canada Goose",
        genus="Branta",
        species="B. canadensis",
        flight=True,
        wingspan=60,
        habitats=["lakes", "ponds", "bays", "marshes", "fields"],
    )


def get_code_output(function, *args):
    output = StringIO()
    with redirect_stdout(output):
        function(*args)
    return Syntax(output.getvalue(), "python", word_wrap=True)


class Slide:
    def __init__(self):
        self.console = console
        _width, _height = shutil.get_terminal_size()
        self.console.size = (_width - 1, _height - 1)

    def prepare(self):
        self.root = Layout()

    def render(self):
        self.prepare()
        self.console.clear()
        self.console.screen().update(self.root)


class CustomSlide(Slide):
    def __init__(self, layout: RenderableType):
        super().__init__()
        self.root = layout

    def prepare(self):
        pass


class OneCaseSlide(Slide):
    def __init__(self, top, bottom, title):
        super().__init__()
        self.top = top
        self.bottom = bottom
        self.title = title

    def prepare(self):
        self.root = Layout(name="root")
        top = Layout(self.top)
        bottom = Layout(self.bottom, ratio=3)
        self.root.split_column(top, bottom)


class SplitSlide(Slide):
    def __init__(self, top, left_side, right_side):
        super().__init__()
        self.top = top
        self.left_side = left_side
        self.right_side = right_side

    def prepare(self):
        self.root = Layout(name="root")
        top = Layout(self.top)
        l = Panel(self.left_side, title="Default")
        r = Panel(self.right_side, title="Rich")

        lower = Layout(ratio=3)
        lower.split_row(Layout(l), Layout(r))
        self.root.split_column(top, lower)


def main():
    """
    Because I'm messing around with all sorts of Rich features, I didn't want to
    get stuck in the meta-task of making various Rich features work inside of
    other Rich features. For the most part, it should be possible to modularly
    compose output with most Rich features, but for the purposes of this demo, I
    didn't want to go through the troubleshooting for all that. All that to say,
    this is a little messier than it has to be for the sake of putting something
    together quickly.
    """
    slides = [
        title(),
        dict_comp(),
        object_comp(),
    ]
    for slide in slides:
        slide.render()
        input()

    panels_and_layouts()
    input()
    pretty_text()
    input()
    traceback_printing(use_rich=False)
    input()
    traceback_printing(use_rich=True)
    input()
    conclusion().render()
    input()


def title() -> Slide:
    content = pad_markdown(
        f"""
        # If I Were a Rich Man

        [A Tour of the Rich, the library for rich text and beautiful formatting in the terminal]

        [[Everything you see here is rendered with Rich]]

        """
    )

    root = Layout()
    top_pad = Layout(
        Syntax("", "python", theme="ansi_dark")
    )  # Need a non-printing thing for this
    bottom_content = Layout(content)
    root.split_column(top_pad, bottom_content)
    return CustomSlide(root)


def dict_comp() -> SplitSlide:
    goose_dict = {
        "genus": "branta",
        "species": "b. canadensis",
        "flight": True,
        "average wingspan (inches)": 60,
        "habitats": ["lakes", "ponds", "bays", "marshes", "fields"],
    }

    top_content = pad_markdown(
        """\
        ## Printing a dictionary:
        
        print(goose_dict)
    
        """
    )
    l = get_code_output(print, goose_dict)
    r = get_code_output(rich.print, goose_dict)
    return SplitSlide(top_content, l, r)


def object_comp() -> SplitSlide:
    goose = get_goose()
    top_content = pad_markdown(
        """\
        ## Printing an object:

        goose = Bird(...)

        print(goose)
    
        """
    )
    l = get_code_output(print, goose)
    r = get_code_output(rich.print, goose)
    return SplitSlide(top_content, l, r)


def pretty_text():
    console.clear()
    top_content = pad_markdown(
        f"""
        ## Getting Crazy with Formatting
        """
    )
    console.print(top_content)
    input()

    print("[bold]Bold[italic] bold and italic [/bold]italic[/italic]")
    input()
    console.print("[bold]Bold[italic] bold and italic [/bold]italic[/italic]")
    input()

    print(
        "[bold italic yellow on red blink]WILL TRIM ADDY ARMOR FOR FREE - ONE MINUTE TURNAROUND"
    )
    input()
    console.print(
        "[bold italic yellow on red blink]WILL TRIM ADDY ARMOR FOR FREE - ONE MINUTE TURNAROUND"
    )
    input()

    print('Text("Print in your official brand colors!", style="#1DA1F2")')
    input()
    t = Text("Print in your official brand colors!", style="#1DA1F2")
    console.print(t)
    input()

    print(
        "Built-in emoji support (see rich/_emoji_codes.py): :star-struck: :100: :stuck_out_tongue_winking_eye: :triumph: :floppy_disk:"
    )
    input()
    console.print(
        "Built-in emoji support (see rich/_emoji_codes.py): :star-struck: :100: :stuck_out_tongue_winking_eye: :triumph: :floppy_disk:"
    )


def panels_and_layouts():
    console.clear()
    top_content = pad_markdown(
        f"""
        ## Layouts and Panels
        """
    )
    console.print(top_content)
    code = """
    root = Layout(name="root")
    top = Layout(top)
    left = Panel(left_side, title="Default")
    right = Panel(right_side, title="Rich")

    lower = Layout(ratio=3)
    lower.split_row(Layout(left), Layout(right))
    root.split_column(top, lower)
    
    """
    console.print(Syntax(code, "python"))

    demo_slide = SplitSlide("", "", "")
    input()
    demo_slide.render()


def traceback_printing(use_rich: bool = False):
    goose = get_goose()
    console.clear()
    if use_rich:
        code = "console.print_exception(show_locals=True)"
    else:
        code = """logging.exception(e)"""
    top_content = pad_markdown(
        f"""
        ## Printing an exception:

        except Exception as e:

        {code}

        .
        """
    )
    console.print(top_content)
    try:
        print(goose.weight)
    except Exception as e:
        if use_rich:
            console.print_exception(show_locals=True)
        else:
            logging.exception(e)


def conclusion() -> Slide:
    content = pad_markdown(
        f"""
        ## The End

        This presentation is on my {GITHUB}!

        Several components of this talk were borrowed in part or whole from Josh Karpel's excellent {SPIEL} library.

        """
    )

    root = Layout()
    top_pad = Layout(
        Syntax("", "python", theme="ansi_dark")
    )  # Need a non-printing thing for this
    bottom_content = Layout(content)
    root.split_column(top_pad, bottom_content)
    return CustomSlide(root)


if __name__ == "__main__":
    main()
