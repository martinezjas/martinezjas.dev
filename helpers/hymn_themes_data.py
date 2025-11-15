"""
Hymn theme data for the Himnario Adventista.
Maps hymn number ranges to their theme information.
"""

# Theme data structure: each entry contains a range and theme information
# Format: (min, max, super_theme, super_icon, sub_theme, sub_image, image_type)
# image_type can be "url" or "unsplash"

HYMN_THEMES = [
    # El Culto (1-52)
    {
        "range": (1, 52),
        "super_theme": "El Culto",
        "super_icon": "https://cdn-icons-png.flaticon.com/512/1769/1769039.png",  # noqa: E501
        "sub_themes": [
            (
                1,
                21,
                "Adoración y Alabanza",
                "2zHGVCrdxHw",
                "unsplash",
            ),
            (22, 34, "Inicio del Culto", "_86u_Y0oAaM", "unsplash"),
            (35, 45, "Cierre del Culto", "yhEgkxZqkkk", "unsplash"),
            (46, 47, "Culto Matutino", "sYffw0LNr7s", "unsplash"),
            (48, 52, "Culto Vespertino", "GPPAjJicemU", "unsplash"),
        ],
    },
    # Dios el Padre (53-77)
    {
        "range": (53, 77),
        "super_theme": "Dios el Padre",
        "super_icon": "https://cdn-icons-png.flaticon.com/512/2883/2883130.png",  # noqa: E501
        "sub_themes": [
            (53, 59, "Amor y Fidelidad de Dios", "Twvvfgeh-f8", "unsplash"),
            (60, 77, "Majestad y Poder de Dios", "H3giJcTw__w", "unsplash"),
        ],
    },
    # Jesucristo (78-189)
    {
        "range": (78, 189),
        "super_theme": "Jesucristo",
        "super_icon": "https://cdn-icons-png.flaticon.com/512/1051/1051474.png",  # noqa: E501
        "sub_themes": [
            (
                78,
                92,
                "Nacimiento de Cristo",
                "https://www.care-net.org/hubfs/iStock-1290099165.jpg",
                "url",
            ),
            (
                93,
                102,
                "Muerte de Cristo",
                "https://images.pexels.com/photos/415571/pexels-photo-415571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",  # noqa: E501
                "url",
            ),
            (
                103,
                106,
                "Resurrección de Cristo",
                "https://assets.answersingenesis.org/img/cms/content/contentnode/og_image/empty-tomb-easter.jpg",  # noqa: E501
                "url",
            ),
            (
                107,
                126,
                "Amor de Cristo",
                "https://images.pexels.com/photos/217893/pexels-photo-217893.jpeg",  # noqa: E501
                "url",
            ),
            (127, 157, "Alabanza a Cristo", "iuNiHYUHXjA", "unsplash"),
            (
                158,
                189,
                "Segunda Venida de Cristo",
                "https://record.adventistchurch.com/wp-content/uploads/2019/07/Greater-works.jpg",  # noqa: E501
                "url",
            ),
        ],
    },
    # El Espíritu Santo (190-203)
    {
        "range": (190, 203),
        "super_theme": "El Espíritu Santo",
        "super_icon": "https://cdn-icons-png.flaticon.com/512/9844/9844643.png",  # noqa: E501
        "sub_themes": [
            (190, 203, "El Espíritu Santo", "yZu0dWSplXM", "unsplash"),
        ],
    },
    # Las Sagradas Escrituras (204-208)
    {
        "range": (204, 208),
        "super_theme": "Las Sagradas Escrituras",
        "super_icon": "https://cdn-icons-png.flaticon.com/512/3389/3389381.png",  # noqa: E501
        "sub_themes": [
            (204, 208, "Las Sagradas Escrituras", "TNlHf4m4gpI", "unsplash"),
        ],
    },
    # El Evangelio (209-344)
    {
        "range": (209, 344),
        "super_theme": "El Evangelio",
        "super_icon": "https://cdn-icons-png.flaticon.com/512/75/75574.png",
        "sub_themes": [
            (
                209,
                237,
                "Invitación",
                "https://antrimbic.org/wp-content/uploads/2015/01/welcome.jpg",
                "url",
            ),
            (238, 244, "Arrepentimiento", "NWu79O4kekw", "unsplash"),
            (
                245,
                283,
                "Consagración",
                "https://thepreachersword.files.wordpress.com/2018/08/prayer-bible-hands.jpg",  # noqa: E501
                "url",
            ),
            (284, 310, "Salvación y Redención", "UTY4N-NU6Wg", "unsplash"),
            (
                311,
                315,
                "Juicio",
                "https://i0.wp.com/ebcelkhorn.com/wp-content/uploads/2014/11/wooden-judges-gavel.jpg?resize=930%2C620&ssl=1",  # noqa: E501
                "url",
            ),
            (316, 344, "Hogar Celestial", "FIKD9t5_5zQ", "unsplash"),
        ],
    },
    # La Vida Cristiana (345-527)
    {
        "range": (345, 527),
        "super_theme": "La Vida Cristiana",
        "super_icon": "https://cdn-icons-png.flaticon.com/512/4212/4212802.png",  # noqa: E501
        "sub_themes": [
            (345, 364, "Gozo y Paz", "RbbdzZBKRDY", "unsplash"),
            (365, 372, "Gratitud", "EAvS-4KnGrk", "unsplash"),
            (373, 390, "Oración y Comunión", "y4kMCLR7LBo", "unsplash"),
            (
                391,
                438,
                "Confianza y Seguridad",
                "https://live.staticflickr.com/453/32580378846_0598dc35fa_b.jpg",  # noqa: E501
                "url",
            ),
            (439, 465, "Petición y Anhelo", "doOCoW955NQ", "unsplash"),
            (466, 473, "Dirección Divina", "3Dtu6_XfqIk", "unsplash"),
            (474, 486, "Peregrinación", "iXU_zV0S62o", "unsplash"),
            (
                487,
                490,
                "Obediencia",
                "https://windows10spotlight.com/wp-content/uploads/2019/09/b51276f3ed3353fd4d6d581f79619a68.jpg",  # noqa: E501
                "url",
            ),
            (
                491,
                504,
                "Servicio Cristiano",
                "https://oakridgebiblechapel.org/wp-content/uploads/2021/09/Sharing-the-Gospel-in-Huaraz.jpg",  # noqa: E501
                "url",
            ),
            (505, 520, "Lucha Contra el Mal", "s0PD-FogBjo", "unsplash"),
            (521, 525, "Mayordomía", "1dGMs4hhcVA", "unsplash"),
            (526, 527, "Amor a la Patria", "AnGx1n-gtw8", "unsplash"),
        ],
    },
    # La Iglesia (528-588)
    {
        "range": (528, 588),
        "super_theme": "La Iglesia",
        "super_icon": "https://cdn-icons-png.flaticon.com/512/9742/9742773.png",  # noqa: E501
        "sub_themes": [
            (528, 533, "Iglesia", "hKKJnp-nWdQ", "unsplash"),
            (534, 534, "Escuela Sabática", "UIib0bAvWfs", "unsplash"),
            (535, 550, "Sábado", "rT6EmOueb3s", "unsplash"),
            (
                551,
                578,
                "Misión de la Iglesia",
                "https://pewtopractice.files.wordpress.com/2011/09/outreach-image.jpg",  # noqa: E501
                "url",
            ),
            (579, 580, "Bautismo", "klk3Lt75K_o", "unsplash"),
            (
                581,
                586,
                "Cena del Señor",
                "https://files.adventistas.org/noticias/es/2022/05/23144357/shutterstock_600525530.jpg",  # noqa: E501
                "url",
            ),
            (587, 587, "Dedicación de un Templo", "sgdyBq6kheQ", "unsplash"),
            (588, 588, "Funeral", "q6e4zwgtUcM", "unsplash"),
        ],
    },
    # El Hogar Cristiano (589-613)
    {
        "range": (589, 613),
        "super_theme": "El Hogar Cristiano",
        "super_icon": "https://cdn.pixabay.com/photo/2014/04/02/10/38/house-304072_1280.png",  # noqa: E501
        "sub_themes": [
            (589, 589, "Boda", "p0vZplFhKYI", "unsplash"),
            (
                590,
                596,
                "Hogar Cristiano",
                "https://www.focusonthefamily.com/wp-content/uploads/2019/07/87F04C59F20A4BBF96906F6DFA4B221D.jpeg",  # noqa: E501
                "url",
            ),
            (597, 597, "Dedicación de un Niño", "oOnJWBMlb5A", "unsplash"),
            (598, 607, "Niños", "DqgMHzeio7g", "unsplash"),
            (608, 613, "Jóvenes", "PGnqT0rXWLs", "unsplash"),
        ],
    },
]

# Fallback theme data
FALLBACK_THEME = {
    "super_icon": "https://cdn-icons-png.flaticon.com/512/1769/1769039.png",
    "sub_image": "https://i.pinimg.com/originals/6d/6f/0e/6d6f0e4099b30c8993d460e5e565144d.jpg",  # noqa: E501
}
