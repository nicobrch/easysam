"""
ShadCN UI-inspired components for Dash applications
"""

# Card components
from .card import (
    card,
    card_header,
    card_content,
    card_footer,
    card_title,
    card_description,
    text_card,
    image_card,
    action_card
)

# Button components
from .button import (
    button,
    primary_button,
    secondary_button,
    destructive_button,
    outline_button,
    ghost_button,
    link_button,
    icon_button
)

# Input components
from .input import (
    input_field,
    text_input,
    email_input,
    password_input,
    number_input,
    search_input,
    textarea
)

# Dropdown components
from .dropdown import (
    dropdown,
    select,
    multi_select,
    searchable_dropdown,
    create_options
)

# Dropzone components
from .dropzone import (
    dropzone,
    video_dropzone,
    image_dropzone
)

# Navigation components
from .navbar import (
    navbar,
    create_navbar
)


__all__ = [
    # Card
    'card', 'card_header', 'card_content', 'card_footer', 'card_title', 'card_description',
    'text_card', 'image_card', 'action_card',

    # Button
    'button', 'primary_button', 'secondary_button', 'destructive_button',
    'outline_button', 'ghost_button', 'link_button', 'icon_button',

    # Input
    'input_field', 'text_input', 'email_input', 'password_input',
    'number_input', 'search_input', 'textarea',

    # Dropdown
    'dropdown', 'select', 'multi_select', 'searchable_dropdown', 'create_options',

    # Dropzone
    'dropzone', 'video_dropzone', 'image_dropzone',

    # Navigation
    'navbar', 'create_navbar',
]
