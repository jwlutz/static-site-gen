import sys
from copy_static import copy_static_to_public
from generate_page import generate_pages_recursive

def main():
    # Get basepath from CLI argument, default to "/"
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    copy_static_to_public("static", "docs")

    generate_pages_recursive(
        "content",
        "template.html",
        "docs",
        basepath
    )

if __name__ == "__main__":
    main()