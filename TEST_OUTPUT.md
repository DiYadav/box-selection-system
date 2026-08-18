(venv) PS D:\box-selection-system> pytest -v                                                
============================================== test session starts ===============================================
platform win32 -- Python 3.12.5, pytest-9.1.1, pluggy-1.6.0 -- D:\box-selection-system\venv\Scripts\python.exe
cachedir: .pytest_cache
django: version: 6.1, settings: config.settings (from ini)
rootdir: D:\box-selection-system
configfile: pytest.ini
plugins: django-4.14.0
collected 30 items                                                                                                

tests/test_api.py::test_product_list PASSED                                                                 [  3%]
tests/test_api.py::test_box_list PASSED                                                                     [  6%]
tests/test_api.py::test_create_order_returns_recommendation_and_persists_it PASSED                          [ 10%]
tests/test_api.py::test_create_order_rejects_empty_items PASSED                                             [ 13%]
tests/test_api.py::test_create_order_rejects_unknown_product PASSED                                         [ 16%]
tests/test_api.py::test_create_order_without_feasible_box_still_creates_order PASSED                        [ 20%]
tests/test_api.py::test_stateless_recommendation_does_not_create_order PASSED                               [ 23%]
tests/test_api.py::test_existing_order_recommend_box PASSED                                                 [ 26%]
tests/test_api.py::test_recommend_box_missing_order_returns_404 PASSED                                      [ 30%]
tests/test_orders.py::test_order_items_are_expanded_by_quantity PASSED                                      [ 33%]
tests/test_orders.py::test_multiple_order_items_are_expanded_correctly PASSED                               [ 36%]
tests/test_orders.py::test_order_flow_selects_cheapest_feasible_box PASSED                                  [ 40%]
tests/test_orders.py::test_quantity_can_force_larger_box PASSED                                             [ 43%]
tests/test_orders.py::test_order_flow_raises_when_no_box_is_feasible PASSED                                 [ 46%]
tests/test_orders.py::test_order_flow_accepts_rotated_product PASSED                                        [ 50%]
tests/test_orders.py::test_order_flow_combined_volume_requires_larger_box PASSED                            [ 53%]
tests/test_services.py::test_smaller_item_fits PASSED                                                       [ 56%]
tests/test_services.py::test_item_exactly_equal_to_box_fits PASSED                                          [ 60%]
tests/test_services.py::test_item_bigger_than_box_does_not_fit PASSED                                       [ 63%]
tests/test_services.py::test_item_fits_after_rotation PASSED                                                [ 66%]
tests/test_services.py::test_item_does_not_fit_in_any_rotation PASSED                                       [ 70%]
tests/test_services.py::test_cheapest_feasible_box_wins PASSED                                              [ 73%]
tests/test_services.py::test_heavy_item_bumps_to_next_box PASSED                                            [ 76%]
tests/test_services.py::test_weight_exceeding_every_box_raises_error PASSED                                 [ 80%]
tests/test_services.py::test_item_too_large_for_every_box_raises_error PASSED                               [ 83%]
tests/test_services.py::test_rotated_item_is_accepted PASSED                                                [ 86%]
tests/test_services.py::test_combined_volume_bumps_to_bigger_box PASSED                                     [ 90%]
tests/test_services.py::test_equal_cost_prefers_smaller_volume PASSED                                       [ 93%]
tests/test_services.py::test_empty_items_raise_error PASSED                                                 [ 96%]
tests/test_services.py::test_utilization_percentages_are_correct PASSED                                     [100%]

=============================================== 30 passed in 0.75s ===============================================




(venv) PS D:\box-selection-system> pytest -v -W error                                       
============================================== test session starts ===============================================
platform win32 -- Python 3.12.5, pytest-9.1.1, pluggy-1.6.0 -- D:\box-selection-system\venv\Scripts\python.exe
cachedir: .pytest_cache
django: version: 6.1, settings: config.settings (from ini)
rootdir: D:\box-selection-system
configfile: pytest.ini
plugins: django-4.14.0
collected 30 items                                                                                                

tests/test_api.py::test_product_list PASSED                                                                 [  3%]
tests/test_api.py::test_box_list PASSED                                                                     [  6%]
tests/test_api.py::test_create_order_returns_recommendation_and_persists_it PASSED                          [ 10%]
tests/test_api.py::test_create_order_rejects_empty_items PASSED                                             [ 13%]
tests/test_api.py::test_create_order_rejects_unknown_product PASSED                                         [ 16%]
tests/test_api.py::test_create_order_without_feasible_box_still_creates_order PASSED                        [ 20%]
tests/test_api.py::test_stateless_recommendation_does_not_create_order PASSED                               [ 23%]
tests/test_api.py::test_existing_order_recommend_box PASSED                                                 [ 26%]
tests/test_api.py::test_recommend_box_missing_order_returns_404 PASSED                                      [ 30%]
tests/test_orders.py::test_order_items_are_expanded_by_quantity PASSED                                      [ 33%]
tests/test_orders.py::test_multiple_order_items_are_expanded_correctly PASSED                               [ 36%]
tests/test_orders.py::test_order_flow_selects_cheapest_feasible_box PASSED                                  [ 40%]
tests/test_orders.py::test_quantity_can_force_larger_box PASSED                                             [ 43%]
tests/test_orders.py::test_order_flow_raises_when_no_box_is_feasible PASSED                                 [ 46%]
tests/test_orders.py::test_order_flow_accepts_rotated_product PASSED                                        [ 50%]
tests/test_orders.py::test_order_flow_combined_volume_requires_larger_box PASSED                            [ 53%]
tests/test_services.py::test_smaller_item_fits PASSED                                                       [ 56%]
tests/test_services.py::test_item_exactly_equal_to_box_fits PASSED                                          [ 60%]
tests/test_services.py::test_item_bigger_than_box_does_not_fit PASSED                                       [ 63%]
tests/test_services.py::test_item_fits_after_rotation PASSED                                                [ 66%]
tests/test_services.py::test_item_does_not_fit_in_any_rotation PASSED                                       [ 70%]
tests/test_services.py::test_cheapest_feasible_box_wins PASSED                                              [ 73%]
tests/test_services.py::test_heavy_item_bumps_to_next_box PASSED                                            [ 76%]
tests/test_services.py::test_weight_exceeding_every_box_raises_error PASSED                                 [ 80%]
tests/test_services.py::test_item_too_large_for_every_box_raises_error PASSED                               [ 83%]
tests/test_services.py::test_rotated_item_is_accepted PASSED                                                [ 86%]
tests/test_services.py::test_combined_volume_bumps_to_bigger_box PASSED                                     [ 90%]
tests/test_services.py::test_equal_cost_prefers_smaller_volume PASSED                                       [ 93%]
tests/test_services.py::test_empty_items_raise_error PASSED                                                 [ 96%]
tests/test_services.py::test_utilization_percentages_are_correct PASSED                                     [100%]

=============================================== 30 passed in 1.59s ===============================================