#!/usr/bin/python3
"""Generate invitation files from a template."""


def generate_invitations(template, attendees):
    """Generate personalized invitations for attendees."""

    if not isinstance(template, str):
        print("Invalid template type: expected a string.")
        return

    if not isinstance(attendees, list) or not all(
        isinstance(attendee, dict) for attendee in attendees
    ):
        print("Invalid attendees type: expected a list of dictionaries.")
        return

    if not template:
        print("Template is empty, no output files generated.")
        return

    if not attendees:
        print("No data provided, no output files generated.")
        return

    fields = ("name", "event_title", "event_date", "event_location")

    for index, attendee in enumerate(attendees, start=1):
        invitation = template

        for field in fields:
            value = attendee.get(field)

            if value is None:
                value = "N/A"

            invitation = invitation.replace(
                "{" + field + "}", str(value)
            )

        filename = f"output_{index}.txt"

        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(invitation)
        except OSError as error:
            print(f"Error writing {filename}: {error}")
