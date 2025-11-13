"""Determine themes for hymns using data-driven approach."""

import validators

from . import get_photo_info
from .hymn_themes_data import FALLBACK_THEME, HYMN_THEMES


def determine_themes(hymn_number: int) -> tuple[str, str, str, str]:
    """
    Determine theme information for a given hymn number.

    Args:
        hymn_number: The hymn number (1-613)

    Returns:
        Tuple of (super_theme_icon, sub_theme_image, super_theme, sub_theme)
    """
    # Find the matching super theme
    for theme_group in HYMN_THEMES:
        min_hymn, max_hymn = theme_group["range"]
        if min_hymn <= hymn_number <= max_hymn:
            super_theme = theme_group["super_theme"]
            hymn_supertheme = theme_group["super_icon"]

            # Find the matching sub theme
            for sub_theme_data in theme_group["sub_themes"]:
                sub_min, sub_max, sub_theme, image_ref, image_type = (  # noqa: E501
                    sub_theme_data
                )

                if sub_min <= hymn_number <= sub_max:
                    # Get the image based on type
                    if image_type == "unsplash":
                        hymn_subtheme = get_photo_info.get_photo_data(  # noqa: E501
                            image_ref
                        )
                    else:  # image_type == "url"
                        hymn_subtheme = image_ref

                    # Validate URLs and return
                    if validators.url(hymn_supertheme) and validators.url(
                        hymn_subtheme
                    ):
                        return (
                            hymn_supertheme,
                            hymn_subtheme,
                            super_theme,
                            sub_theme,
                        )
                    else:
                        # Return with fallback images
                        return (
                            FALLBACK_THEME["super_icon"],
                            FALLBACK_THEME["sub_image"],
                            super_theme,
                            sub_theme,
                        )

    # If no match found, return fallback (shouldn't happen for valid hymns)
    return (
        FALLBACK_THEME["super_icon"],
        FALLBACK_THEME["sub_image"],
        "Unknown",
        "Unknown",
    )
