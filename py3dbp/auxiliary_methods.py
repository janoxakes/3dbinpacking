

def rect_intersect_generic(position1, dimensions1, position2, dimensions2, x, y):
    d1 = dimensions1
    d2 = dimensions2

    cx1 = position1[x] + d1[x]/2
    cy1 = position1[y] + d1[y]/2
    cx2 = position2[x] + d2[x]/2
    cy2 = position2[y] + d2[y]/2

    ix = max(cx1, cx2) - min(cx1, cx2)
    iy = max(cy1, cy2) - min(cy1, cy2)

    return ix < (d1[x]+d2[x])/2 and iy < (d1[y]+d2[y])/2


def item_to_positions(item):
    position = item.position
    dimensions = item.get_dimension()
    return set(
        [(position[0] + dimensions[0], position[1], position[2]),
        (position[0], position[1] + dimensions[1], position[2]),
        (position[0], position[1], position[2] + dimensions[2])],
    )

