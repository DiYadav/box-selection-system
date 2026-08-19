# AI Usage

## 1. AI Tool Used

I used ChatGPT during the development of this assignment.

I used AI mainly for:

- understanding the assignment requirements
- reviewing my implementation
- identifying missing test scenarios
- debugging test failures
- reviewing API behavior
- checking edge cases
- improving documentation

AI-generated suggestions were reviewed and verified before being used in the project.

---

## 2. How I Used AI

My development approach was:

1. I created the basic Django project structure myself.
2. I implemented and changed the project based on the assignment requirements.
3. I used ChatGPT to review specific parts of the implementation.
4. I ran the code and tests locally.
5. When something failed, I shared the actual error with ChatGPT.
6. I investigated and modified the code based on the actual project behavior.
7. I ran the tests again to verify the changes.

AI output was treated as guidance, not as the final source of truth.

---

## 3. Prompts Used

### Prompt 1 - Requirement Review

**Prompt:**

```text
### Prompt 5
**prompt**
I have already created the basic Django project and app structure myself.
I am building an e-commerce box selection system where customers place orders containing products, and the system recommends the most suitable shipping box.
I want to start with the database design. I need Product, Box, Order, and OrderItem models.
product should contain SKU/name, length, width, height, and weight.
box should contain a unique code, internal length/width/height, maximum supported weight, and cost.
order should contain order information and a cached recommended_box foreign key.
orderItem should connect products to orders and support quantity.
Please design the models.py with proper Django field types, decimal constraints, relationships, validators, related_name values, and useful properties for dimensions and volume.
Also explain the important design decisions briefly instead of adding unnecessary fields.



### Prompt 2
**Prompt:**
Now that the basic models are defined help me design the box-selection algorithm.
jhe service should accept an Order read its OrderItems and quantities. Calculate the total weight. Check whether available boxes satisfy the weight constraint. Check whether the products can physically fit based on their dimensions. Select the most appropriate box according to the defined selection strategy.
I don't want to implement the API yet.
First reason through the algorithm and explain:
1 How total order weight should be calculated.
2 How product dimensions should be compared with box dimensions.
3 Whether volume alone is sufficient.
4 How multiple products in the same order should be handled.
5 How to choose the best box when multiple boxes are suitable.
6 What should happen when no box can contain the order.
Please suggest a clean service-layer design rather than putting all business logic inside the Django model or serializer.



### Prompt 3
**Prompt:**
based on the box-selection algorithm we discussed, implement a clean Django service for calculating the recommended box.
jhe service should accept an Order read its OrderItems and quantities. Calculate the total weight. Check whether available boxes satisfy the weight constraint. Check whether the products can physically fit based on their dimensions. Select the most appropriate box according to the defined selection strategy.
save the selected box into order.recommended_box.
Handle the case where no suitable box exists.
Keep the business logic separate from views and serializers.
Please provide the implementation nd explain the important parts so I can understand why each step is need



### Prompt 4
**Prompt:**
review the current box-selection implementation as a senior Django backend developer.
I want to make sure the algorithm is not only working for simple cases.
analyze these edge cases:
one product with quantity greater than 1.
Multiple different products.
Product dimensions larger than the box in one orientation but fitting after rotation.
Product weight exactly equal to box max_weight.
kroduct dimensions exactly equal to the box internal dimensions.
no available boxes.
Empty order.
Zero or invalid quantities.
Multiple boxes that can contain the order.
Existing recommended_box becoming unavailable or deleted.
Identify any problems in the current approach and suggest practical improvements without over doing inside.



### Prompt 5
**Prompt:**
Now I want to expose this functionality through Django REST Framework APIs.
design apis for:
Creating/listing products.
creating/listing boxes.
creating an order with its order items.
retrieving an order with its items and recommended box.
Triggering or calculating the recommended box for an order.
Use serializers and ViewSets/APIViews appropriately.
The order creation flow should validate the products and quantities and should not allow invalid order items.
Please keep the API structure clean and suitable for a real backend project.
Show the serializers, views, URLs, and explain how the connect.



### Prompt 6
**Prompt:**
give me some scenarios to i can understand the pytest how we can use as a new user for pytest give me the test cases for this project which we discussed
step by step give me the actual struvture



### Prompt 7 debug 
**Prompt:**
tests\test_services.py:269: AssertionError ============================================ short test summary info =============================================
FAILED tests/test_services.py::test_rotated_item_is_accepted - core.services.NoSuitableBoxError: No suitable box found. BOX-R: total item volume 6000 cm3 exceeds usable volu...
FAILED tests/test_services.py::test_combined_volume_bumps_to_bigger_box - AssertionError: assert 'BOX-S' == 'BOX-L'
2 failed, 12 passed in 0.41s



### Prompt 8 debug 
**Prompt:**
my api tests are failing. check this error and tell me what is wrong
FAILED tests/test_api.py::test_product_list - assert 404 == 200
FAILED tests/test_api.py::test_box_list - assert 404 == 200
FAILED tests/test_api.py::test_create_order_returns_recommendation_and_persists_it - assert 404 == 201



### Prompt 9 debug 
**Prompt:**
the api tests are mostly passing but i am getting this serializer warning. check the actual problem
UserWarning: min_value should be an integer or Decimal instance.
