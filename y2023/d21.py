from grid import GridV2, V2, DirectionEnum, is_inbounds, read_grid_v2


def get_possible_locations(
    grid: GridV2[str],
    start_ps: set[V2],
    n_steps: int,
) -> set[V2]:
    if n_steps == 0:
        return start_ps
    next_start_ps = set()
    for p in start_ps:
        for direction in DirectionEnum:
            next_p = p + direction.to_v2()
            if grid.is_inbounds(next_p) and grid.at(next_p) in [".", "S"]:
                next_start_ps.add(next_p)
    return get_possible_locations(grid, next_start_ps, n_steps - 1)


if __name__ == "__main__":
    grid = read_grid_v2("./y2023/data/d21.txt", lambda x: x)
    final_ps = get_possible_locations(grid, set(grid.find("S")), n_steps=64)
