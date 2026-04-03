from mcp.server.fastmcp import FastMCP

# content in the docstring """"Content"""" is not for the system python usualy ignore these, they are for the humans and llms to understand the context of the tool, resource, and prompt.

# create a server

mcp = FastMCP("Notes Server", json_response=True)

# to store notes
notes = {}

# define tools to be called by LLM

@mcp.tool()
def add_note(title, content):
    """
    Save a new note with a title and content.
    Use this when the user wants to remember something.
    """

    if title not in notes:
        notes[title] = content
        return f"Note {title} saved successfully!"
    
    return "A note with similar title already exist"

@mcp.tool()
def del_note(title):

    """
    Delete a note by its title.
    """

    if title not in notes:
        return "Error! title not found"
    
    del notes[title]

    return f"Note {title} deleted successfully!"

@mcp.tool()
def search_notes(query):

    """
    Search all notes for a keyword.
    Returns matching note titles and their content.
    """

    res = []

    if not notes:
        return "No notes saved yet"
    
    for title, content in notes.items():
        if query.lower() in title or query.lower() in content:
            res.append(f"{title}: {content}")

    if not res:
        return "No notes found matching"
    
    return "\n".join(res)


# define resources to be read by LLM


@mcp.resource("notes://list")
def list_all_notes():

    """
    Returns a list of all saved note titles.
    The LLM reads this to know what notes exist.
    """
    
    if not notes:
        return "No notes saved yet."
    
    titles = "\n".join(f"- {title}" for title in notes.keys())
    return f"Saved notes:\n{titles}"


@mcp.resource("notes://note/{title}")
def get_note(title):

    """
    Returns the full content of a specific note.
    URI example: notes://note/My Meeting Notes
    """
    
    if title not in notes:
        return f"Note {title} does not exist."
    
    return f"Title: {title}\n\nContent:\n{notes[title]}"



# define prompts to be used by LLM (goto templates)


@mcp.prompt()
def summarise_notes():

    """
    Instructs the LLM to summarise all current notes.
    """
    
    if not notes:
        return "There are no notes to summarise yet."

    all_content = "\n\n".join(
        f"[{title}]\n{content}" for title, content in notes.items()
    )

    return (
        f"Here are all my saved notes:\n\n{all_content}\n\n"
        "Please give me a clear, concise summary of the key points."
    )


@mcp.prompt()
def brainstorm(topic: str):

    """
    Instructs the LLM to brainstorm ideas on a topic,
    taking existing notes into account as context.
    """
    context = ""
    if notes:
        context = "\n".join(f"- {t}: {c}" for t, c in notes.items())
        context = f"\nI already have these related notes:\n{context}\n"

    return (
        f"I want to brainstorm ideas about: {topic}\n"
        f"{context}\n"
        "Please suggest 5 creative ideas, building on what I already know."
    )


# run server ocally using stdio

if __name__ == "__main__":
    mcp.run(transport="stdio")