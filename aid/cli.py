"""aid CLI — dispatch to commands.journal/plan/recipe/translate/summarize."""
import sys
import click

from . import __version__
from .commands import journal, plan, recipe, translate, summarize


@click.group(help="aid — small Python utilities powered by LLMs for everyday life.")
@click.version_option(__version__, prog_name="aid")
def cli():
    pass


@cli.command()
def journal_cmd():
    """Interactive daily journal with AI follow-up question."""
    journal.run()
cli.add_command(journal_cmd, name="journal")


@cli.command()
@click.argument("tasks", nargs=-1)
def plan_cmd(tasks):
    """Turn a brain dump into a structured day plan."""
    plan.run(" ".join(tasks))
cli.add_command(plan_cmd, name="plan")


@cli.command()
@click.argument("ingredients", nargs=-1)
def recipe_cmd(ingredients):
    """Suggest 3 quick recipes from your ingredients."""
    recipe.run(" ".join(ingredients))
cli.add_command(recipe_cmd, name="recipe")


@cli.command()
@click.argument("text", nargs=-1)
def translate_cmd(text):
    """Quick translate (auto-detect source language)."""
    translate.run(" ".join(text))
cli.add_command(translate_cmd, name="translate")


@cli.command()
@click.argument("source", nargs=-1)
def summarize_cmd(source):
    """Summarize a URL or piped text to 5 bullets."""
    summarize.run(" ".join(source) if source else "")
cli.add_command(summarize_cmd, name="summarize")


def main():
    cli()


if __name__ == "__main__":
    main()
