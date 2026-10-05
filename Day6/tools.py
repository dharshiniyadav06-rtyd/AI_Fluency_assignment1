# Day 6 - Reliable Tool Calling
# Scenario: Movie Information Assistant

MOVIES = {
    "Inception": {
        "genre": "Science Fiction",
        "director": "Christopher Nolan",
        "year": 2010,
        "rating": 8.8
    },
    "Interstellar": {
        "genre": "Science Fiction",
        "director": "Christopher Nolan",
        "year": 2014,
        "rating": 8.7
    },
    "The Dark Knight": {
        "genre": "Action",
        "director": "Christopher Nolan",
        "year": 2008,
        "rating": 9.0
    }
}


def get_movie_info(movie):
    if movie not in MOVIES:
        return f"Movie '{movie}' was not found."

    data = MOVIES[movie]

    return {
        "movie": movie,
        "genre": data["genre"],
        "director": data["director"],
        "year": data["year"]
    }


def get_movie_rating(movie):
    if movie not in MOVIES:
        return f"Movie '{movie}' was not found."

    return {
        "movie": movie,
        "rating": MOVIES[movie]["rating"]
    }


# Single source of truth:
# The same schemas will later be used by the model and validator.

SCHEMAS = {
    "get_movie_info": {
        "type": "function",
        "function": {
            "name": "get_movie_info",
            "description": "Get basic information about a movie.",
            "parameters": {
                "type": "object",
                "properties": {
                    "movie": {
                        "type": "string",
                        "enum": [
                            "Inception",
                            "Interstellar",
                            "The Dark Knight"
                        ],
                        "description": "The movie name."
                    }
                },
                "required": ["movie"],
                "additionalProperties": False
            },
            "strict": True
        }
    },

    "get_movie_rating": {
        "type": "function",
        "function": {
            "name": "get_movie_rating",
            "description": "Get the rating of a movie.",
            "parameters": {
                "type": "object",
                "properties": {
                    "movie": {
                        "type": "string",
                        "enum": [
                            "Inception",
                            "Interstellar",
                            "The Dark Knight"
                        ],
                        "description": "The movie name."
                    }
                },
                "required": ["movie"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
}


TOOLS = {
    "get_movie_info": get_movie_info,
    "get_movie_rating": get_movie_rating
}