from pytermgui import tim

tim.alias("my-tag1", "@surface primary+1")

# Recursive tags also work!
tim.alias("my-tag2", "my-tag1 italic")


