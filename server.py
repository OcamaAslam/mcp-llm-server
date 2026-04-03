from mcp.server.fastmcp import FastMCP


# create a server

mcp = FastMCP("Notes Server", version="1.0.0")

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


@mcp.resource("notes//list")
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
