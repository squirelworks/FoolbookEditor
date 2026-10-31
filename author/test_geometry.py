"""Stage geometry, in page coordinates."""

from __future__ import annotations

import unittest

from author import geometry


class HitTests(unittest.TestCase):
    def test_the_topmost_shape_wins(self):
        shapes = [
            {"kind": "rect", "x": 0, "y": 0, "w": 100, "h": 100},
            {"kind": "button", "x": 10, "y": 10, "w": 20, "h": 20},
        ]
        self.assertEqual(geometry.hit(shapes, 12, 12), 1)
        self.assertEqual(geometry.hit(shapes, 80, 80), 0)
        self.assertIsNone(geometry.hit(shapes, 200, 200))

    def test_background_is_hit_only_when_it_is_the_target(self):
        shapes = [
            {"kind": "rect", "x": 0, "y": 0, "w": 100, "h": 100, "layer": "background"},
            {"kind": "rect", "x": 50, "y": 50, "w": 10, "h": 10},
        ]
        self.assertIsNone(geometry.hit(shapes, 5, 5, "page"))
        self.assertEqual(geometry.hit(shapes, 5, 5, "background"), 0)
        self.assertEqual(geometry.hit(shapes, 55, 55, "background"), 0)
        self.assertEqual(geometry.hit(shapes, 55, 55, "page"), 1)

    def test_a_shape_stored_as_points_is_hit(self):
        triangle = {"kind": "polygon", "points": [[10, 10], [60, 10], [60, 40]]}
        self.assertEqual(geometry.hit([triangle], 30, 20), 0)

    def test_a_line_is_hit_near_its_stroke_not_its_box(self):
        line = {"kind": "line", "x": 0, "y": 0, "w": 100, "h": 100, "points": [[0, 0], [100, 100]]}
        self.assertEqual(geometry.hit([line], 50, 52), 0)
        self.assertIsNone(geometry.hit([line], 90, 10))

    def test_a_flat_line_is_hit(self):
        line = {"kind": "line", "points": [[10, 50], [90, 50]]}
        self.assertEqual(geometry.hit([line], 40, 51), 0)


class MarqueeTests(unittest.TestCase):
    shapes = [
        {"kind": "rect", "x": 0, "y": 0, "w": 20, "h": 20},
        {"kind": "rect", "x": 100, "y": 100, "w": 20, "h": 20},
        {"kind": "line", "points": [[30, 40], [60, 40]]},
        {"kind": "rect", "x": 15, "y": 15, "w": 10, "h": 10, "layer": "background"},
    ]

    def test_every_shape_the_box_meets_is_chosen(self):
        self.assertEqual(geometry.marquee(self.shapes, 10, 10, 50, 50), [0, 2, 3])

    def test_a_backwards_drag_is_the_same_box(self):
        self.assertEqual(geometry.marquee(self.shapes, 50, 50, 10, 10), [0, 2, 3])

    def test_a_flat_line_is_caught_by_its_points(self):
        self.assertEqual(geometry.marquee(self.shapes, 40, 35, 45, 45), [2])

    def test_the_layer_filters(self):
        self.assertEqual(geometry.marquee(self.shapes, 10, 10, 50, 50, "page"), [0, 2])
        self.assertEqual(geometry.marquee(self.shapes, 10, 10, 50, 50, "background"), [3])

    def test_an_empty_box_far_away_chooses_nothing(self):
        self.assertEqual(geometry.marquee(self.shapes, 300, 300, 400, 400), [])


class NudgeTests(unittest.TestCase):
    def test_the_steps_are_one_and_eight(self):
        self.assertEqual((geometry.NUDGE, geometry.NUDGE_BIG), (1, 8))
        self.assertEqual(geometry.arrow_step("Left", False), (-1, 0))
        self.assertEqual(geometry.arrow_step("Down", False), (0, 1))
        self.assertEqual(geometry.arrow_step("Right", True), (8, 0))
        self.assertEqual(geometry.arrow_step("Up", True), (0, -8))

    def test_every_selected_shape_moves_and_keeps_its_size(self):
        shapes = [
            {"kind": "rect", "x": 10, "y": 20, "w": 30, "h": 40},
            {"kind": "line", "points": [[0, 0], [10, 10]]},
            {"kind": "rect", "x": 0, "y": 0, "w": 5, "h": 5},
        ]
        geometry.nudge(shapes, [0, 1], *geometry.arrow_step("Right", True))
        self.assertEqual((shapes[0]["x"], shapes[0]["y"], shapes[0]["w"], shapes[0]["h"]), (18, 20, 30, 40))
        self.assertEqual(shapes[1]["points"], [[8, 0], [18, 10]])
        self.assertNotIn("x", shapes[1])
        self.assertEqual((shapes[2]["x"], shapes[2]["y"]), (0, 0))

    def test_a_shape_named_twice_moves_once(self):
        shapes = [{"x": 0, "y": 0, "w": 5, "h": 5}]
        geometry.nudge(shapes, [0, 0], 1, 0)
        self.assertEqual(shapes[0]["x"], 1)


class ResizeTests(unittest.TestCase):
    def box(self):
        return {"kind": "rect", "x": 10, "y": 20, "w": 100, "h": 50}

    def test_a_box_has_eight_handles(self):
        found = geometry.handles(self.box())
        self.assertEqual(set(found), {"nw", "n", "ne", "e", "se", "s", "sw", "w"})
        self.assertEqual(found["n"], (60, 20))
        self.assertEqual(found["e"], (110, 45))

    def test_a_line_has_its_two_ends(self):
        line = {"kind": "line", "points": [[0, 0], [50, 10]]}
        self.assertEqual(geometry.handles(line), {"p0": (0.0, 0.0), "p1": (50.0, 10.0)})

    def test_a_side_handle_pulls_only_its_side(self):
        shape = self.box()
        geometry.resize(shape, dict(shape), "e", 150, 999)
        self.assertEqual((shape["x"], shape["y"], shape["w"], shape["h"]), (10, 20, 140, 50))
        shape = self.box()
        geometry.resize(shape, dict(shape), "n", -5, 0)
        self.assertEqual((shape["x"], shape["y"], shape["w"], shape["h"]), (10, 0, 100, 70))

    def test_a_corner_keeps_the_opposite_corner(self):
        shape = self.box()
        geometry.resize(shape, dict(shape), "nw", 0, 0)
        self.assertEqual((shape["x"], shape["y"], shape["w"], shape["h"]), (0, 0, 110, 70))

    def test_nothing_gets_smaller_than_four_by_four(self):
        self.assertEqual(geometry.MIN_SIZE, 4)
        shape = self.box()
        geometry.resize(shape, dict(shape), "se", 10, 20)
        self.assertEqual((shape["w"], shape["h"]), (4, 4))
        shape = self.box()
        geometry.resize(shape, dict(shape), "w", 500, 0)
        self.assertEqual((shape["x"], shape["w"]), (106, 4))

    def test_dragging_a_line_end_moves_only_that_end(self):
        line = {"kind": "line", "x": 0, "y": 0, "w": 50, "h": 10, "points": [[0, 0], [50, 10]]}
        geometry.resize(line, {**line}, "p1", 80, 40)
        self.assertEqual(line["points"], [[0, 0], [80, 40]])
        self.assertEqual((line["w"], line["h"]), (80, 40))

    def test_a_line_end_cannot_land_on_the_other_end(self):
        line = {"kind": "line", "points": [[0, 0], [50, 10]]}
        geometry.resize(line, {**line}, "p1", 1, 1)
        self.assertEqual(line["points"], [[0, 0], [50, 10]])

    def test_points_inside_a_box_scale_with_it(self):
        poly = {"kind": "polygon", "x": 0, "y": 0, "w": 10, "h": 10, "points": [[0, 0], [10, 0], [10, 10]]}
        geometry.resize(poly, {**poly}, "se", 20, 30)
        self.assertEqual(poly["points"], [[0, 0], [20, 0], [20, 30]])


class ConstrainTests(unittest.TestCase):
    def test_shift_makes_a_box_a_square_in_the_drag_direction(self):
        self.assertEqual(geometry.constrain_box(10, 10, 50, 30), (50, 50))
        self.assertEqual(geometry.constrain_box(10, 10, -20, 0), (-20, -20))
        self.assertEqual(geometry.constrain_box(10, 10, 15, 60), (60, 60))

    def test_shift_snaps_a_line_to_flat(self):
        self.assertEqual(geometry.constrain_line(0, 0, 100, 10), (100, 0))
        self.assertEqual(geometry.constrain_line(0, 0, -100, 10), (-100, 0))

    def test_shift_snaps_a_line_to_upright(self):
        self.assertEqual(geometry.constrain_line(0, 0, 5, -80), (0, -80))

    def test_shift_snaps_a_line_to_45_degrees(self):
        self.assertEqual(geometry.constrain_line(0, 0, 60, 50), (60, 60))
        self.assertEqual(geometry.constrain_line(0, 0, -40, 50), (-50, 50))

    def test_a_click_is_left_alone(self):
        self.assertEqual(geometry.constrain_line(3, 3, 3, 3), (3, 3))


class GridTests(unittest.TestCase):
    def test_five_snaps_to_eight_on_an_eight_grid(self):
        self.assertEqual(geometry.GRID, 8)
        self.assertEqual(geometry.snap(5, 8), 8)
        self.assertEqual(geometry.snap(3, 8), 0)
        self.assertEqual(geometry.snap(4, 8), 8)
        self.assertEqual(geometry.snap(-5, 8), -8)
        self.assertEqual(geometry.snap_point(5, 13), (8, 16))

    def test_a_moved_selection_lands_on_the_grid_and_keeps_its_spacing(self):
        shapes = [
            {"x": 5, "y": 21, "w": 10, "h": 10},
            {"x": 30, "y": 50, "w": 10, "h": 10},
            {"kind": "line", "points": [[5, 5], [9, 9]]},
        ]
        geometry.snap_move(shapes, [0, 1])
        self.assertEqual((shapes[0]["x"], shapes[0]["y"]), (8, 24))
        self.assertEqual((shapes[1]["x"], shapes[1]["y"]), (33, 53))
        self.assertEqual(shapes[2]["points"], [[5, 5], [9, 9]])


class AlignTests(unittest.TestCase):
    def shapes(self):
        return [
            {"x": 100, "y": 100, "w": 40, "h": 20},
            {"x": 10, "y": 50, "w": 20, "h": 10},
            {"kind": "line", "points": [[0, 0], [10, 30]]},
        ]

    def boxes(self, shapes):
        return [geometry.bounds(s) for s in shapes]

    def test_the_first_selected_shape_is_the_reference_and_stays(self):
        shapes = self.shapes()
        geometry.align(shapes, [0, 1, 2], "left")
        self.assertEqual([b[0] for b in self.boxes(shapes)], [100, 100, 100])
        self.assertEqual(geometry.bounds(shapes[0]), (100, 100, 40, 20))

    def test_the_reference_is_selection_order_not_array_order(self):
        shapes = self.shapes()
        geometry.align(shapes, [1, 0], "top")
        self.assertEqual(shapes[0]["y"], 50)
        self.assertEqual(shapes[1]["y"], 50)

    def test_right_bottom_and_centres(self):
        shapes = self.shapes()
        geometry.align(shapes, [0, 1], "right")
        self.assertEqual(shapes[1]["x"] + shapes[1]["w"], 140)
        geometry.align(shapes, [0, 1], "bottom")
        self.assertEqual(shapes[1]["y"] + shapes[1]["h"], 120)
        geometry.align(shapes, [0, 1], "center horizontal")
        self.assertEqual(shapes[1]["x"] + shapes[1]["w"] / 2, 120)
        geometry.align(shapes, [0, 1], "center vertical")
        self.assertEqual(shapes[1]["y"] + shapes[1]["h"] / 2, 110)

    def test_one_shape_is_nothing_to_align(self):
        shapes = self.shapes()
        geometry.align(shapes, [1], "left")
        self.assertEqual(shapes[1]["x"], 10)


class DistributeTests(unittest.TestCase):
    def test_equal_gaps_across(self):
        shapes = [
            {"x": 0, "y": 0, "w": 10, "h": 10},
            {"x": 100, "y": 5, "w": 20, "h": 10},
            {"x": 15, "y": 9, "w": 30, "h": 10},
        ]
        geometry.distribute(shapes, [0, 1, 2], "horizontal")
        # span 0..120, filled 60, two gaps of 30: middle box starts at 40.
        self.assertEqual(shapes[2]["x"], 40)
        self.assertEqual((shapes[0]["x"], shapes[1]["x"]), (0, 100))
        self.assertEqual(shapes[2]["y"], 9)

    def test_equal_gaps_down(self):
        shapes = [
            {"x": 0, "y": 0, "w": 10, "h": 10},
            {"x": 0, "y": 12, "w": 10, "h": 10},
            {"x": 0, "y": 30, "w": 10, "h": 10},
            {"x": 0, "y": 90, "w": 10, "h": 10},
        ]
        geometry.distribute(shapes, [3, 1, 0, 2], "vertical")
        tops = [s["y"] for s in shapes]
        self.assertEqual(tops, [0, 30, 60, 90])

    def test_fewer_than_three_is_a_no_op(self):
        shapes = [{"x": 0, "y": 0, "w": 10, "h": 10}, {"x": 50, "y": 0, "w": 10, "h": 10}]
        geometry.distribute(shapes, [0, 1], "horizontal")
        self.assertEqual([s["x"] for s in shapes], [0, 50])


class GroupTests(unittest.TestCase):
    def shapes(self):
        return [
            {"kind": "rect", "name": "paper", "x": 0, "y": 0, "w": 640, "h": 480},
            {"kind": "button", "name": "A", "x": 10, "y": 10, "w": 90, "h": 28},
            {"kind": "text", "name": "between", "x": 300, "y": 300, "w": 10, "h": 10},
            {"kind": "line", "name": "L", "points": [[20, 60], [120, 90]]},
        ]

    def test_a_group_holds_the_children_in_order_with_their_bounds(self):
        shapes = self.shapes()
        at = geometry.group(shapes, [3, 1])
        self.assertEqual(at, 2)
        self.assertEqual([s["name"] for s in shapes], ["paper", "between", "Group"])
        made = shapes[2]
        self.assertEqual(made["kind"], "group")
        self.assertEqual([c["name"] for c in made["children"]], ["A", "L"])
        self.assertEqual((made["x"], made["y"], made["w"], made["h"]), (10, 10, 110, 80))
        self.assertEqual(made["children"][0]["x"], 10)

    def test_fewer_than_two_or_two_layers_is_not_a_group(self):
        shapes = self.shapes()
        self.assertIsNone(geometry.group(shapes, [1]))
        shapes[3]["layer"] = "background"
        self.assertIsNone(geometry.group(shapes, [1, 3]))
        self.assertEqual(len(shapes), 4)

    def test_moving_a_group_moves_its_children(self):
        shapes = self.shapes()
        at = geometry.group(shapes, [1, 3])
        geometry.nudge(shapes, [at], 8, 0)
        made = shapes[at]
        self.assertEqual(made["x"], 18)
        self.assertEqual(made["children"][0]["x"], 18)
        self.assertEqual(made["children"][1]["points"][0], [28, 60])

    def test_the_stage_paints_the_children(self):
        shapes = self.shapes()
        geometry.group(shapes, [1, 3])
        self.assertEqual([s["name"] for s in geometry.flatten(shapes)], ["paper", "between", "A", "L"])

    def test_a_group_can_be_picked_inside_its_bounds(self):
        shapes = self.shapes()
        at = geometry.group(shapes, [1, 3])
        self.assertEqual(geometry.hit(shapes, 50, 50, "page"), at)


if __name__ == "__main__":
    unittest.main()
