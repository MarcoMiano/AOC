# Shoelace algorithm implementation test


def shoelace(vertices: list) -> float:
    area = 0
    if len(vertices) < 2:
        return area

    d_area = abs(
        (vertices[-1][0] * vertices[0][1]) - (vertices[-1][1] * vertices[0][0])
    )

    current_point = vertices.pop()
    while vertices:
        next_point = vertices.pop()
        d_area += abs(
            (current_point[0] * next_point[1]) - (current_point[1] * next_point[0])
        )
        current_point = next_point

    area = d_area / 2.0

    return area
